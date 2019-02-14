# -*- coding: utf-8 -*-
import scrapy

from redis import Redis

from qichacha.settings import REDIS_HOST

qiurl_spider ='qcc_url'

class QccurlSpider(scrapy.Spider):
    name = qiurl_spider
    allowed_domains = ['qichacha.com']
    base_url = 'https://www.qichacha.com/'
    cookies={}

    custom_settings = {'DOWNLOADER_MIDDLEWARES':{'qichacha.middlewares.QccUrlAgentDownloaderMiddleware': 543,},   # 用它需要设置延迟请求20+秒一次
                       #'DOWNLOADER_MIDDLEWARES':{'qichacha.middlewares.QccSeleniumDownloaderMiddleware': 543,}   # 用它需解决图片验证码问题-待解决
                       }

    redis_key = 'qcc:request'
    redis = Redis(host=REDIS_HOST)

    def fuzzy_search(self):
        '''
        模糊搜索
        :return:
        '''
        search_keys = ['软装', '家具', '民用家具', '酒店家具', '办公家具', '户外家具', '软装饰品', '软装灯饰', '软装墙饰', '软装吊饰', '软装画艺', '软装雕塑',
                       '软装酒店用品', '软装花器', '软装窗帘', '软装床品', '软装抱枕靠垫', '软装墙布墙纸', '软装地毯', '软装餐布', '软装布艺', '软装花植花器', '软装鲜花绿植',
                       '软装仿真干花']

        page_num = 2  # 11                   # 普通会员限制10页
        self.cookies = string_to_dict()
        for i in search_keys:
            for j in range(1, page_num):
                url = self.base_url + 'search?key=' + i + '&p={}&'.format(j)
                yield scrapy.Request(url, callback=self.url_parse, cookies=self.cookies)

    def key_search(self):
        '''
        关键字搜索
        :return:
        '''
        from qichacha.other.fullname import get_name
        search_keys = get_name()
        self.cookies = string_to_dict()
        # for i in range(0,3):
        for i in range(0, len(search_keys)):
            yield scrapy.Request(url=self.base_url+'search?key={}'.format(search_keys[i]),
                                 callback=self.url_parse, cookies=self.cookies)


    def start_requests(self):
        # self.fuzzy_search()
        # self.key_search()
        for request in self.fuzzy_search():
            yield request


    def url_parse(self, response):

        # if 'www.qichacha.com/index_verify?' in response.text:  # 滑块认证-pass
        #     auth_url = response.text.split("'")[1]            # https://www.qichacha.com/index_verify?type=companysearch&back=/search?key=%E8%BD%AF%E8%A3%85&p=1&
        #     yield scrapy.Request(auth_url,callback=self.url_parse,cookies=self.cookies)

        count = 0
        trs = response.xpath('//section[@id="searchlist"]/table/tbody/tr')
        if not trs:
            trs = response.xpath('//section[@id="searchlist"]/table/tr')
        for tr in trs:
            u = tr.xpath('td[2]/a/@href').extract_first()
            url = self.base_url + u

            if url:
                # count = self.redis.lpush(self.redis_key,url)
                count = self.redis.sadd(self.redis_key,url)


# 登录态
def string_to_dict():  # for cookies
    cookies ='acw_tc=779346d015359394441466828eddee14c862246dfa92e041a616a00271; _uab_collina=153593944631127383459377; UM_distinctid=1659d20071c538-09b0b929bcb25-9393265-1fa400-1659d20071d3d7; zg_did=%7B%22did%22%3A%20%221659d200731a0-0815d9f37b256-9393265-1fa400-1659d2007321c3%22%7D; PHPSESSID=4tlvnucmd0ontn3eqr0voc1jt0; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535939447,1535979767,1536024189; _umdata=ED82BDCEC1AA6EB9842C48468AD1AD91A9B62757D7DF25F691CBE61689095C140010DCEE878730D8CD43AD3E795C914C2486DBB377653218905E1F6014EEB501; CNZZDATA1254842228=1661324530-1535934951-https%253A%252F%252Fwww.qichacha.com%252F%7C1536025315; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201536024188138%2C%22updated%22%3A%201536029149112%2C%22info%22%3A%201535939446587%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22265d30ecc365058984801223ceaf0330%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1536029149'
    item_dict = {}
    items = cookies.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        item_dict[key] = value

    return item_dict

