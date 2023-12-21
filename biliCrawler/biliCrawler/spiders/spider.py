import scrapy
import json
import time


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["books.toscrape.com", "api.bilibili.com"]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    start_urls = ["https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1"]

    def parse(self, response):
        data = json.loads(response.text)
        now_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        for i in range(20):
            title = data["data"]["list"][i]['title']
            bv = data["data"]["list"][i]['bvid']
            duration = data["data"]["list"][i]['duration']
            tname = data["data"]["list"][i]['tname']
            owner = data["data"]["list"][i]['owner']['name']
            like = data["data"]["list"][i]['stat']['like']


            yield {
                'time': now_time,
                'owner': owner,
                'title': title,
                'like': like,
                'bv': bv,
                'duration': duration,
                'now_rank': tname,
            }
            # print(data["data"]["list"][i].keys())

        # for key in data["data"]["list"][i]:
        #     print(key + '\n')


        # for book in all_books:
        #     book_url = self.start_urls[0] + \
        #         book.xpath('./h3/a/@href').extract_first()
        #     yield scrapy.Request(book_url, callback=self.parse_book)

    # def parse_book(self, response):
    #     title = response.xpath('//div/h1/text()').extract_first()
        # print(title)
