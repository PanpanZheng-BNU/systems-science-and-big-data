#!/home/zpp/miniconda3/bin/python

import requests
import json
import time
import pandas as pd
import re
import os, pathlib


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
        df = pd.DataFrame(columns=['time', 'pub_location', 'title', 'tname', 'like', 'owner', 'bvid', 'picurl'])
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
            picurl = item["pic"]
            df.loc[len(df)] = [time.strftime("%Y-%m-%d %H:%M", time.localtime()), pub_location, title, tname, like,
                               owner, bvid, picurl]
        print(df)
        return df.head(20)

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

    def get_imgs(self):
        pass

    def get_comments(self, n):
        df_oids = self.get_oids()
        df_comments = pd.DataFrame(columns=['comments', 'bvid'])
        for i in df_oids.index:
            # print("oid:{}, bvid{}".format(df_oids['oid'][i], df_oids['bvid'][i]))
            df = pd.DataFrame(columns=['comment', 'like'])
            for j in range(n):
                re_comments = requests.get(self.comments_url.format(j, df_oids['oid'][i]), headers=self.header).json()
                comments = []
                if 'data' in re_comments.keys():
                    for k in re_comments['data']['replies']:
                        comment = k['content']['message']
                        comments.append(comment)
                        like = k['like']
                        df.loc[len(df)] = [comment, like]
                    print("搜集到%d条评论" % (len(comments)))
                else:
                    print("无评论")


                df.drop_duplicates(inplace=True)
                df.sort_values(by='like', ascending=False, inplace=True)
            df_comments.loc[len(df_comments)] = [df, df_oids['bvid'][i]]
            print("完成第{}个视频评论区爬取，休息1s\n ====================\n".format(i+1))
            time.sleep(1)
        return pd.merge(df_oids, df_comments, on="bvid", how="inner")



if __name__ == '__main__':
    parent_foldername = pathlib.Path(__file__).parent.resolve()
    with open(os.path.join(parent_foldername,'run_time.log'), 'a+') as f:
        f.write('run at {} \n'.format(time.strftime("%Y-%m-%d %H:%M", time.localtime())))
    url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ",
        "cookie": "buvid3=D74A61FE-9E8C-2005-8F9A-66A98C5348F923589infoc; b_nut=1696562923; i-wanna-go-back=-1; b_ut=7; _uuid=34CF738D-3E4B-CEB8-B2EB-6CFDA5BF378223828infoc; buvid4=28167CDE-3D7C-0669-20D3-129D4C9BF78424206-023100611-kTAtAg4Ew5AOCiR7whYGGg%3D%3D; DedeUserID=36611479; DedeUserID__ckMd5=fbde96d72483bd70; rpdid=|(J|~Ju)u~|R0J'uYmYlYkmll; hit-dyn-v2=1; LIVE_BUVID=AUTO5616965911294779; CURRENT_QUALITY=80; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; enable_web_push=DISABLE; header_theme_version=CLOSE; is-2022-channel=1; CURRENT_FNVAL=4048; go-back-dyn=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDM0MTQyMDgsImlhdCI6MTcwMzE1NDk0OCwicGx0IjotMX0.Sb3px8OqRMX3rfSnYs58WNERmsL_1ZLFBXLhQ_MYocM; bili_ticket_expires=1703414148; fingerprint=18fa7f8a0ed8d682e36174ae2a412da3; buvid_fp=18fa7f8a0ed8d682e36174ae2a412da3; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; PVID=1; SESSDATA=3bf76898%2C1718929748%2Cca4de%2Ac2CjCKkZgUn0Uknr3ubVnSlqSe8hWaxpxQuwaCedO3v8Idfu8xVhACYBO5vZxuApnNYocSVmF2NWcxQzRNMWFwX3RwcDNscW5VSFFFMjhZczI0M2RHeDFSUjE0WnRPSG5NMHVNUk02Y1VTb3p6dVhRVGY1RW5LVFRwWlFmRnRaVVJaY0FBY29ub1JRIIEC; bili_jct=8c95e1ca49e425f09e5896538b9c0ff5; sid=6fe7t6df; b_lsid=A10937284_18C99935FBB; innersign=0; bp_video_offset_36611479=878517100659867672; home_feed_column=4; browser_resolution=730-726"
    }

    results_df = biliCrawler(url, header).get_comments(20)
    parent_foldername = pathlib.Path(__file__).parent.resolve()
    child_foldername = time.strftime("%Y-%m-%d-%H", time.localtime())
    folder_name = os.path.join(parent_foldername, child_foldername)    
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        os.mkdir(os.path.join(folder_name, 'comments'))
        os.mkdir(os.path.join(folder_name, 'imgs'))
    for i in results_df.index:
        filename = os.path.join(folder_name, 'comments', results_df['bvid'][i] + ".csv")
        results_df['comments'][i].to_csv(filename, index=False, encoding="utf-8-sig")

        with open(os.path.join(folder_name,'imgs', results_df['bvid'][i] + ".jpg"), 'wb') as f:
            f.write(requests.get(results_df['picurl'][i]).content)

    results_df.loc[:, results_df.columns != 'comments'].to_csv(os.path.join(folder_name, "rank.csv"), index=False,
                                                                 encoding="utf-8-sig")
