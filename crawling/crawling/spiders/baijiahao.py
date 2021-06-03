import scrapy
from scrapy import Request, Spider
from urllib.parse import quote
from ..items import ScrapyuniversalItem


class baijiahao(scrapy.Spider):

    name = 'baijiahao'
    start_urls = ['https://baijiahao.baidu.com/s?id=1701473545312252129&wfr=spider&for=pc']

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


    def parse(self, response):
        for i in range(20):
            item = ScrapyuniversalItem() 
            comment = response.xpath("/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[{}]/div/div[2]/div[2]/span/text()".format(i+1)).extract()
            name = response.xpath("/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[{}]/div/div[2]/div[1]/h5/text()".format(i+1)).extract()
            time = response.xpath("/html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[{}]/div/div[2]/div[3]/div[1]/span[1]/text()".format(i+1)).extract()
            topic = response.xpath("/html/body/div/div/div/div[2]/div[1]/div/h2/text()").extract()
            item['comment'] = comment
            item['time'] = time
            item['topic'] = topic
            item['name'] = name
            yield item