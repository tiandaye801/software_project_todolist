# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class CrawlingHotspotsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlingHotspotsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver import ActionChains
import time
f = open('../../../crawling/crawling/spiders/words.txt', 'r')
content = f.read()
f.close()

class BytedanceDownloaderMiddleware(object):
    def process_request(self, request, spider):
        if (request.url == 'http://www.baidu.com/'):
            search_content = content
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            # option.add_argument('--disable-gpu')
            driver = webdriver.Chrome(chrome_options=option)
            driver.get(request.url)
            driver.find_element_by_xpath('//*[@id="kw"]').send_keys(search_content)
            time.sleep(1) 
            driver.find_element_by_xpath('//*[@id="su"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="s_tab"]/div/a[1]').click()
            time.sleep(1)
            action_move = driver.find_element_by_xpath('//*[@id="header_top_bar"]/div[1]/div/span')
            ActionChains(driver).move_to_element(action_move).perform()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="c-tips-container"]/div/div/div/ul/li[3]/a').click()
            time.sleep(1)
            return scrapy.http.HtmlResponse(url = request.url, body = driver.page_source.encode('utf-8'), encoding = 'utf-8', request = request, status = 200)
        else:
            return None
        
    def process_response(self, request, response, spider):
        return response