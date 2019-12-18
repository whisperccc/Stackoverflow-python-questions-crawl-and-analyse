import scrapy
from stackoverflow.items import StackoverflowItem
import pymongo
class StackoverflowPythonSpider(scrapy.Spider):

    name = "stackoverflow-python"

    def start_requests(self):
        urls = []
        _url = 'https://stackoverflow.com/questions/tagged/python?tab=votes&page={}&pagesize=15'

        self.connection = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.connection.scrapy
        self.collection = self.db.stackoverflow

        for page in range(1, 87157):
            urls.append(_url.format(page))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        question_list = response.xpath('//*[@id="questions"]')

        for question in question_list.xpath('./div'):
            item = StackoverflowItem()
            item['_id'] = question.attrib['id']
            #print(item['_id'])
            item['questions'] = question.xpath('div[2]/h3/a/text()').extract()
            #print(item['questions'])
            item['votes'] = question.xpath(
                    'div[1]/div[1]/div[1]/div[1]/span/strong/text()').extract()
            item['answers'] = question.xpath(
                    'div[1]/div[1]/div[2]/strong/text()').extract()
            item['views'] = question.xpath('div[1]/div[2]/@title').extract()
            item['links'] = question.xpath('div[2]/h3/a/@href').extract()
            item['questionsbody']= question.xpath('div[2]/div[1]/text()').extract()
            #print(item['questionsbody'])
            item['questionstag'] = question.xpath('div[2]/div[2]/@class').extract()
            #print(item['questionstag'])
            item['questionstime'] = question.xpath('div[2]/div[3]/div[1]/div[1]/span/@title').extract()
            #print(item['questionstime'])
            if not self.connection or not item:
                break
            self.collection.save(item)
            yield