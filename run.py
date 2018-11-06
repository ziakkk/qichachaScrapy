#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/9/4'
# qq:2456056533

佛祖保佑  永无bug!

"""


def run_spider():
    from scrapy import cmdline
    from qichacha.spiders.qccUrl import qiurl_spider
    from qichacha.spiders.qccDetail import qcdetail_spider

    cmdline.execute('scrapy crawl {}'.format(qiurl_spider).split())



def run_all():
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings
    from twisted.internet import reactor, defer
    from scrapy.utils.log import configure_logging

    from qichacha.spiders.qccUrl import QccurlSpider
    from qichacha.spiders.qccDetail import QccdetailSpider

    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(QccurlSpider)
        yield runner.crawl(QccdetailSpider)
        reactor.stop()

    crawl()
    reactor.run()


if __name__ == '__main__':
    # run_spider()
    run_all()
