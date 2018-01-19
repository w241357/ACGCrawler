import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from AcgCrawler.items import AcgcrawlerItem


class AcgSpider(scrapy.Spider):

    name = 'AcgCrawler'
    allowed_domains = ['xxshe.xyz']
    bash_url = 'https://www.xxshe.xyz/page/'

    def start_requests(self):
        for i in range(1, 1601):
            url = self.bash_url + str(i) + '/'
            yield Request(url, self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        main_content = soup.find_all('div', class_='mh-loop-content')

        for content in main_content:
            content_title = content.find('h3', class_='mh-loop-title').find('a').get_text()
            content_update_time = content.find('div', class_='mh-loop-meta').find('span').get_text()
            if not content.find('div', class_='mh-excerpt').find('img') is None:
                content_img_url = content.find('div', class_='mh-excerpt').find('img')['src']
            content_url = content.find('h3', class_='mh-loop-title').find('a')['href']
            content_introduction = content.find('div', class_='mh-excerpt').find_all('p')[-1].get_text()
            print(u'标题：', content_title.strip())
            print(u'更新时间：', content_update_time)
            print(u'图片地址：', content_img_url)
            print(u'内容简介：', content_introduction)
            print(u'内容地址：', content_url)

            yield Request(content_url, callback=self.get_content)

    def get_content(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        content_text = soup.find('div', class_='entry-content').find_all('p')
        for text in content_text:
            data = text.get_text(strip=True).strip()
            if len(data) != 0:
                print(data)



