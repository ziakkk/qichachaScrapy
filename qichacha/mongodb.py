#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2019/2/14'
# qq:2456056533

"""
import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
from scrapy import Item
import logging

class MongoHandler:
    def __init__(self, conn_uri=None, db='spider', collection_name='default'):
        if not conn_uri:
            conn_uri = 'localhost'
        self.client = AsyncIOMotorClient(conn_uri)
        self.db = self.client[db]
        self.collection = self.db[collection_name]

        # self.loop = asyncio.new_event_loop()
        self.loop = asyncio.get_event_loop()

    async def process(self, item, ):
        if isinstance(item, Item):
            item_data = item.__dict__

        elif isinstance(item, dict):
            item_data = item
        else:
            try:
                item_data = json.loads(item)
            except:
                raise ('******item must dict ')

        re_data = await self.collection.find_one({'_values.url': item['url']},\
                                                 {'_id':0,'_values.url': 1})

        if not re_data:
            if await self.collection.insert_one(item_data):
                logging.info('*******save to mongodb success')
            else:
                raise ('*******save to mongodb fail')
        else:
            logging.info('********* repeat item')

    def run(self, item):
        # asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.process(item))

    def close(self):
        self.loop.close()