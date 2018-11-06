# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QichachaItem(scrapy.Item):
    # define the fields for your item here like:

    url = scrapy.Field()
    logo_ico = scrapy.Field()
    centent_title = scrapy.Field()
    centent_mobile = scrapy.Field()
    centent_index = scrapy.Field()
    centent_email = scrapy.Field()
    centent_address = scrapy.Field()

    license = scrapy.Field()
    faren = scrapy.Field()
    detail = scrapy.Field()


