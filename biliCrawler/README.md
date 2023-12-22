# biliCrawler 介绍
本项目为[bilibili网站](https://www.bilibili.com)的爬虫程序，用于爬取B站排行前20的视频，及其部分评论。
主要程序位于[`biliCrawler.py`](./biliCrawler.py)，其中创建了一个名为`biliCrawler`的对象，其中包含如下方法：
1. `get_rank` 获取当前的b站全站排名（共100名）的上传地址，视频标题，分类，点赞数，up主，视频bv号以及封面图片链接，并将其存储为`pandas.DataFrame`，并返回前20名（通过`df.head(20)`实现，当然若希望爬取更多的可以对其进行更改）
2. `get_oids` 根据 `get_rank` 中获得的 `bvid` 通过访问视频地址来获得视频的 `oid`，以用于评论区的爬取。通过内联表的方式返回基于 `get_rank` 所返回的表新增一行名为 `oid`
3. `get_comments` 根据 `get_oids` 获得的 `oid` 来爬取各视频的评论区，并再次新建一个具有两列的表一列为视频的`bvid`，另一列为视频的评论，该列的每个元素均为表(子表)，每个子表具有两列，一列为评论，另一列为点赞数。并通过 `bvid` 对新表和 `get_oids` 所获的表进行内联，返回内联的结果。


在如下部分执行程序
```python
if __name__ == '__main__':
    # 获取当前文件所在的目录
    parent_foldername = pathlib.Path(__file__).parent.resolve()
    # 在每次执行时，在 run_tim.log 文件中新建一行，记录执行的时间
    ##（用于在服务器中检查自动化 Crontab 脚本是否正常运行）
    with open(os.path.join(parent_foldername,'run_time.log'), 'a+') as f:
        f.write('run at {} \n'.format(time.strftime("%Y-%m-%d %H:%M", time.localtime())))

    # 定义我们希望爬取的排行版，此处爬取的是全站排行，可以讲url换成各个分区的api
    url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"

    # 定义requests中所使用的头
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ",
        # 换成自己的 Cookie 
        "cookie": "buvid3=D74A61FE-9E8C-2005-8F9A-66A98C5348F923589infoc; b_nut=1696562923; i-wanna-go-back=-1; b_ut=7; _uuid=34CF738D-3E4B-CEB8-B2EB-6CFDA5BF378223828infoc; buvid4=28167CDE-3D7C-0669-20D3-129D4C9BF78424206-023100611-kTAtAg4Ew5AOCiR7whYGGg%3D%3D; DedeUserID=36611479; DedeUserID__ckMd5=fbde96d72483bd70; rpdid=|(J|~Ju)u~|R0J'uYmYlYkmll; hit-dyn-v2=1; LIVE_BUVID=AUTO5616965911294779; CURRENT_QUALITY=80; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; enable_web_push=DISABLE; header_theme_version=CLOSE; is-2022-channel=1; CURRENT_FNVAL=4048; go-back-dyn=0; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; SESSDATA=31c44b43%2C1718627673%2C379a8%2Ac2CjBMNeCUMBPCtYtGG1RZGhE-cXwJ7J6oa_8dNLpQ2Fyv2zTh3l4gJwzE6PtJ3OQqfwwSVnBtOVNFa2NfWlZJZFctVVVVYjg5SWIzX0ZKb0pNNlVGbEEtcnRZS2o4Sjd6N0F5R1ZNT044SUJWcUpPN0lBUlZ3ZDBOOFR0ODdZWHlUcnJlU3FBenRnIIEC; bili_jct=482c686432746fd0ef849091694fc9f4; sid=833mnv8u; bsource=search_google; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDM0MTQyMDgsImlhdCI6MTcwMzE1NDk0OCwicGx0IjotMX0.Sb3px8OqRMX3rfSnYs58WNERmsL_1ZLFBXLhQ_MYocM; bili_ticket_expires=1703414148; fingerprint=2ca00601fdddf9333e74c31a2e68cae7; buvid_fp=2ca00601fdddf9333e74c31a2e68cae7; PVID=1; b_lsid=C54C6359_18C8F5828A3; innersign=0; bp_video_offset_36611479=877781273949503529; home_feed_column=4; browser_resolution=730-726"
    }

    # 执行 get_comments 方法
    ## (只遍历api中前20页的评论，若希望爬取更多，可对其进行修改)，
    results_df = biliCrawler(url, header).get_comments(20)
    # 建立一个根据时间命名的文件夹
    child_foldername = time.strftime("%Y-%m-%d-%H", time.localtime())
    folder_name = os.path.join(parent_foldername, child_foldername)    
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        os.mkdir(os.path.join(folder_name, 'comments')) # 建立文件夹下的用于存储评论的子文件夹
        os.mkdir(os.path.join(folder_name, 'imgs')) # 建立文件夹下的用于视频封面的子文件夹

    for i in results_df.index:
        filename = os.path.join(folder_name, 'comments', results_df['bvid'][i] + ".csv")
        # 存储评论，使用视频的bvid进行命名
        results_df['comments'][i].to_csv(filename, index=False, encoding="utf-8-sig") 

        # 存储封面，使用视频的bvid进行命名
        with open(os.path.join(folder_name,'imgs', results_df['bvid'][i] + ".jpg"), 'wb') as f:
            f.write(requests.get(results_df['picurl'][i]).content)

    # 存储当前前20排行存为 .csv 文件
    results_df.loc[:, results_df.columns != 'comments'].to_csv(os.path.join(folder_name, "rank.csv"), index=False,
                                                                 encoding="utf-8-sig")

```

- `rank.csv`

| 列             | 含义             |
|----------------|------------------|
| `time`         | 爬取时间         |
| `pub_location` | 视频发布地址     |
| `title`        | 视频标题         |
| `tname`        | 视频所在分区     |
| `like`         | 视频的点赞数     |
| `owner`        | up主             |
| `bvid`         | 视频bv号         |
| `picurl`       | 视频封面图片链接 |
| `oid`          | 视频oid          |
