# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import platform
import random
from logging import getLogger

import time
from scrapy.http import HtmlResponse
from selenium import webdriver

from scrapy import signals
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from qichacha.agents2 import AGENTS_ALL


class QccUrlAgentDownloaderMiddleware:
    def process_request(self, request, spider):
        agent = random.choice(AGENTS_ALL)
        request.headers['User-Agent'] = agent


class QccSeleniumDownloaderMiddleware:
    def __init__(self, executable_path=None):
        self.timeout = 30
        self.executable_path = executable_path   #  r'D:/develop/seleniumDrivers/chromedriver.exe'

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 去除 --ingor

        if platform.system() == 'Windows':
            self.browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=options)

        else:
            options.add_argument('no-sandbox')  # 针对linux root用户
            self.browser = webdriver.Chrome(chrome_options=options)

        self.browser.maximize_window()
        self.browser.set_page_load_timeout(self.timeout)
        self.browser.implicitly_wait(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def close_spider(self,spider):
        self.browser.quit()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(executable_path=crawler.settings.get('CHROME_DRIVER'), )

    def process_request(self, request, spider):
        """
        用Chrome抓取页面
        """
        try:

            self.browser.get(request.url)
            td_id = self.wait.until(EC.presence_of_element_located(By.ID, 'nc_1_n1z'))
            self.move_gap(td_id,263)
            code = self.browser.find_element_by_xpath('//div[@id="nc_1_scale_text"]/i').text   # 码
            code_image = self.browser.find_element_by_xpath('')  # 图片
            img = code_image.get_attribute('src')   # 验证码
            if img:
                # 打码平台: 没钱-嘤嘤嘤
                raise ('*************打码平台************')


            page_source = self.browser.page_source

            return HtmlResponse(url=request.url, body=page_source, request=request, encoding='utf-8', status=200)

        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)


    def except_request(self, request):
        '''
        请求失败
        '''
        print('err requseet:', request.url)
        return request


    def move_gap(self,slider,distance):
        '''

        :param slider: 滑块
        :param distance: 需要移动的距离
        :return:
        '''
        action = ActionChains(self.browser)
        action.click_and_hold(slider).perform()

        track = self.get_track(distance)  # 获取移动轨迹

        for x in track:
            action.move_by_offset(xoffset=x,yoffset=0).perform()
        time.sleep(0.5)
        action.release().perform()
        time.sleep(0.5)



    def get_track(self, distance):
        '''
        模拟滑动快慢轨迹
        :param distance: 需要移动的距离
        :return: 移动轨迹track[0.2,]
        '''
        track = []  # 移动轨迹
        current = 0  # 当前位置
        mid = distance * 4 / 5  # #减速阀值 4/5加速. 1/5加速
        t = 0.2  # 计算间隔
        v = 0  # 速度v

        while current < distance:
            if current < mid:
                # 加速度
                a = 2
            else:
                a = -3
            v_0 = v
            v = v_0 + a * t  # 当前速度 = 初速度+加速*加速时间
            move = v_0 * t + 1 / 2 * a * t * t  # 移动距离

            current += move  # 当前移动距离
            track.append(round(move))  # 加入轨迹:浮点型

        return track

