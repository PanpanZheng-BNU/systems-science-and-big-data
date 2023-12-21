import requests
import json
import time
import pandas as pd
import re
import os


class biliCrawler():
    def __init__(self, url, header):
        self.name = "spider"
        self.url = url
        self.header = header
        self.video_url = "https://www.bilibili.com/video/"
        self.comments_url = "https://api.bilibili.com/x/v2/reply/main?csrf=40a227fcf12c380d7d3c81af2cd8c5e8&mode=3&next={}&oid={}&plat=1&type=1"

        # self.comment_url = ""

    def get_rank(self):
        a = requests.get(self.url, headers=self.header)
        data = json.loads(a.text)
        df = pd.DataFrame(columns=['time', 'pub_location', 'title', 'tname', 'like', 'owner', 'bvid'])
        for item in data["data"]["list"]:
            title = item["title"]
            try:
                pub_location = item["pub_location"]
            except:
                pub_location = ""
            tname = item["tname"]
            like = item["stat"]["like"]
            owner = item["owner"]["name"]
            bvid = item["bvid"]
            # pic = item["pic"]
            df.loc[len(df)] = [time.strftime("%Y-%m-%d %H:%M", time.localtime()), pub_location, title, tname, like,
                               owner, bvid]
        print(df)
        return df
    def get_oids(self):
        df_rank = self.get_rank()
        df_oids = pd.DataFrame(columns=['oid', 'bvid'])
        regex_oid = r'\&oid=(.*?)"'
        for i in df_rank['bvid'].astype(str):
            video_url = self.video_url + i
            re_video = requests.get(video_url, headers=self.header)
            # time.sleep(0.5)                                   # 为了防止被封ip
            df_oids.loc[len(df_oids)] = [re.findall(regex_oid, re_video.text)[0], i]

        print(df_oids)
        # df_oids = pd.concat([df_rank, df_oids], axis=1)
        # print(df_oids)
        return pd.merge(df_rank, df_oids, on="bvid", how="inner")

    def get_comments(self, n):
        df_oids = self.get_oids()
        df_comments = pd.DataFrame(columns=['comments', 'bvid'])
        for i in df_oids.index:
            # print("oid:{}, bvid{}".format(df_oids['oid'][i], df_oids['bvid'][i]))
            df = pd.DataFrame(columns=['comment', 'like'])
            for j in range(n):
                re_comments = requests.get(self.comments_url.format(j, df_oids['oid'][i]), headers=self.header).json()
                comments = []
                for k in re_comments['data']['replies']:
                    comment = k['content']['message']
                    comments.append(comment)
                    like = k['like']
                    df.loc[len(df)] = [comment, like]
                print("搜集到%d条评论" % (len(comments)))
            df.drop_duplicates(inplace=True)
            df.sort_values(by='like', ascending=False, inplace=True)
            df_comments.loc[len(df_comments)] = [df, df_oids['bvid'][i]]
        return pd.merge(df_oids, df_comments, on="bvid", how="inner")



if __name__ == '__main__':
    url = "https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ",
        "cookie": "SESSDATA=31c44b43%2C1718627673%2C379a8%2Ac2CjBMNeCUMBPCtYtGG1RZGhE-cXwJ7J6oa_8dNLpQ2Fyv2zTh3l4gJwzE6PtJ3OQqfwwSVnBtOVNFa2NfWlZJZFctVVVVYjg5SWIzX0ZKb0pNNlVGbEEtcnRZS2o4Sjd6N0F5R1ZNT044SUJWcUpPN0lBUlZ3ZDBOOFR0ODdZWHlUcnJlU3FBenRnIIEC"
    }

    comments_df = biliCrawler(url, header).get_comments(10)
    folder_name = time.strftime("%Y-%m-%d-%H", time.localtime())
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        os.mkdir(folder_name + "/comments")
    for i in comments_df.index:
        filename = folder_name + "/comments/" + comments_df['bvid'][i] + ".csv"
        comments_df['comments'][i].to_csv(filename, index=False, encoding="utf-8-sig")

    comments_df.loc[:, comments_df.columns != 'comments'].to_csv(folder_name + "/rank.csv", index=False,
                                                                 encoding="utf-8-sig")
