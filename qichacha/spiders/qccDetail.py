# -*- coding: utf-8 -*-
import scrapy

from redis import Redis
# from scrapy_redis.spiders import RedisSpider
# from scrapy_redis.utils import bytes_to_str

from scrapy_redis_bloomfilter.spiders import RedisSpider
from scrapy_redis_bloomfilter.utils import bytes_to_str

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

        # sadd qcc:request https://www.qichacha.com/firm_91253782d4f5a5f0afa82554fc94c8a0.html

        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):

        self.cookies = string_to_dict()
        return scrapy.Request(url, callback=self.detail_parse, cookies=self.cookies, dont_filter=True)

    # 对比直接使用 Redis
    # def start_requests(self):
    #     self.cookies = string_to_dict()
    #     self.redis = Redis(host='10.0.0.146')
    #     while True:
    #         url = self.redis.lpop(self.redis_key)
    #         if not url:
    #             print('redis url 为空')
    #             break
    #         yield scrapy.Request(url.decode(), callback=self.detail_parse, cookies=cookies)
    #
    #         # url = 'https://www.qichacha.com/firm_91253782d4f5a5f0afa82554fc94c8a0.html'
    #         # yield scrapy.Request(url, callback=self.detail_parse, cookies=cookies)

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
        item['centent_title'] = centent_title

        item['centent_mobile'] = response.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[1]/span[2]/span/text()').extract_first()
        item['centent_index'] = response.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[3]/a/text()').extract_first()
        item['centent_email'] = response.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[1]/span[2]/a/text()').extract_first()
        item['centent_address'] = response.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[3]/a[1]/text()').extract_first()

        # 工商信息
        info = response.xpath('//section[@id="Cominfo"]')

        item['faren'] = response.xpath('//h2[@class="seo font-20"]/text()').extract_first()

        table = info.xpath('table[2]')


        # detail = tr.xpath('string(.)').extract_first()
        # item['detail'] = self.clear_data(detail)

        # 避免后期更改解析规则_采用单个字段解析
        d1 = table.xpath('tr[1]/td[2]/text()').extract_first()
        d2 = table.xpath('tr[1]/td[4]/text()').extract_first()

        d3 = table.xpath('tr[2]/td[2]/text()').extract_first()
        d4 = table.xpath('tr[2]/td[4]/text()').extract_first()

        d5 = table.xpath('tr[3]/td[2]/text()').extract_first()
        d6 = table.xpath('tr[3]/td[4]/text()').extract_first()

        d7 = table.xpath('tr[4]/td[2]/text()').extract_first()
        d8 = table.xpath('tr[4]/td[4]/text()').extract_first()

        d9 = table.xpath('tr[5]/td[2]/text()').extract_first()
        d10 = table.xpath('tr[5]/td[4]/text()').extract_first()

        d11 = table.xpath('tr[6]/td[2]/text()').extract_first()
        d12 = table.xpath('tr[6]/td[4]/text()').extract_first()

        d13 = table.xpath('tr[7]/td[2]/text()').extract_first()
        d14 = table.xpath('tr[7]/td[4]/text()').extract_first()

        d15 = table.xpath('tr[8]/td[2]/span/text()').extract_first()
        d16 = table.xpath('tr[8]/td[4]/text()').extract_first()

        d17 = table.xpath('tr[9]/td[2]/text()').extract_first()
        d18 = table.xpath('tr[9]/td[4]/text()').extract_first()

        d19 = table.xpath('tr[10]/td[2]/text()').extract_first()

        d20 = table.xpath('tr[11]/td[2]/text()').extract_first()

        detail = {'注册资本': d1, '实缴资本': d2, '经营状态': d3, '成立日期': d4, '统一社会信用代码': d5, '纳税人识别号': d6, '注册号': d7, '组织机构代码': d8,
                  '公司类型': d9, '所属行业': d10, '核准日期': d11, '登记机关': d12, '所属地区': d13, '英文名': d14, '曾用名': d15, '参保人数': d16,
                  '人员规模': d17, '营业期限': d18, '企业地址': d19, '经营范围': d20}

        detail_data ={}
        for k,v in detail.items():
            if v:
                detail_data[k] = v.replace('\n','').replace(' ','')
            else:
                detail_data[k] = ''

        item['detail'] = detail_data

        item['license'] = ''

        info_img_url = info.xpath('div/a/@href').extract_first()  # 营业执照

        if info_img_url:
            yield scrapy.Request(self.base_url + info_img_url, callback=self.detail_parse2, cookies=self.cookies,
                                 meta={'item': item}, dont_filter=True)

        else:
            yield item

    def detail_parse2(self, response):

        item = response.meta['item']
        license_url = response.xpath('/html/body/div[1]/div/div/img/@src').extract_first()
        item['license'] = license_url

        return item


        # def clear_data(self, data):
        #     ''' 清洗数据: 英文名split 存在问题 '''
        #     if data:
        #         data = data.replace('\n', '').split(' ')
        #         data2 = [x.replace('：', '') for x in data if x != '']
        #         dlt = len(data2)
        #         keys = [data2[i] for i in range(0, dlt, 2)]
        #         valuse = [data2[j] for j in range(1, dlt, 2)]
        #         data_dict = dict(zip(keys, valuse))
        #
        #         return data_dict
        #     return {}


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(QccdetailSpider)
    process.start()
