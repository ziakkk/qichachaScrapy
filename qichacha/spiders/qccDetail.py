# -*- coding: utf-8 -*-
import scrapy

from redis import Redis
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

from qichacha.spiders.qccUrl import string_to_dict  # cookies

from qichacha.items import QichachaItem


qcdetail_spider = 'qcc_detail'

class QccdetailSpider(RedisSpider):
    name = qcdetail_spider

    allowed_domains = ['qichacha.com']
    base_url = 'https://www.qichacha.com/'
    cookies = {}

    custom_settings = {'ITEM_PIPELINES': {'qichacha.pipelines.QichachaPipeline': 300, },
                       'DOWNLOADER_MIDDLEWARES': {'qichacha.middlewares.QccUrlAgentDownloaderMiddleware': 543, }}

    redis_key = 'qcc:request'


    def make_request_from_data(self, data):

        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):

        self.cookies = string_to_dict()
        return scrapy.Request(url,callback=self.detail_parse, cookies=self.cookies, dont_filter=True)

    def detail_parse(self, response):
        item = QichachaItem()
        item['url'] = response.url
        c_top = response.xpath('//div[@id="company-top"]/div')
        logo_ico = c_top.xpath('div[@class="logo"]/div[2]/img/@src').extract_first()
        if not logo_ico:
            logo_ico = c_top.xpath('div[@class="logo"]/div[1]/img/@src').extract_first()
        item['logo_ico'] = logo_ico


        centent_title = c_top.xpath('div[@class="content"]/div/h1/text()').extract_first()
        if not centent_title:
            centent_title = c_top.xpath('div[@class="content"]/div/text()').extract_first()
        item['centent_title']=centent_title


        centent_mobile = c_top.xpath('div[@class="content"]/div[2]/span/span[2]/span/text()').extract_first()
        if not centent_mobile:
            centent_mobile = c_top.xpath('div[@class="content"]/div[2]/span[2]/span/text()').extract_first()
        item['centent_mobile'] = centent_mobile

        item['centent_index'] = c_top.xpath('div[@class="content"]/div[2]/span[3]/a/@href').extract_first()
        item['centent_email'] = c_top.xpath('div[@class="content"]/div[3]/span[1]/span[2]/a/text()').extract_first()

        centent_address = c_top.xpath('div[2]/div[3]/span[3]/a[1]/text()').extract_first()
        if not centent_address:
            centent_address = c_top.xpath('div[2]/div[4]/span[2]/a[1]/text()').extract_first()
        item['centent_address'] = centent_address

            # 工商信息
        info = response.xpath('//section[@id="Cominfo"]')

        item['faren'] = response.xpath('//h2[@class="seo font-20"]/text()').extract_first()

        tr = info.xpath('table[2]')
        detail = tr.xpath('string(.)').extract_first()
        item['detail'] = self.clear_data(detail)

        item['license'] = ''

        info_img_url = info.xpath('div/a/@href').extract_first()  # 营业执照

        if info_img_url:
            yield scrapy.Request(self.base_url + info_img_url, callback=self.detail_parse2, cookies=self.cookies,meta={'item': item},dont_filter=True)

        else:
            yield item


    def detail_parse2(self, response):

        item = response.meta['item']
        license_url = response.xpath('/html/body/div[1]/div/div/img/@src').extract_first()
        item['license'] = license_url

        return item

    # 清洗数据
    def clear_data(self, data):
        if data:
            data = data.replace('\n', '').split(' ')
            data2 = [x.replace('：', '') for x in data if x != '']
            dlt = len(data2)
            keys = [data2[i] for i in range(0, dlt, 2)]
            valuse = [data2[j] for j in range(1, dlt, 2)]
            data_dict = dict(zip(keys, valuse))

            return data_dict
        return {}
