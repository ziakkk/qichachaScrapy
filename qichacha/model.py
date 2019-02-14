#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/6/14'
# qq:2456056533

佛祖保佑  永无bug!

"""
import json
from contextlib import contextmanager

from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db_name = 'spider'

HOST = 'localhost'

engine = create_engine(
    'mysql+pymysql://root:2456056533@{host}:3306/{db_name}?charset=utf8'.format(host=HOST, db_name=db_name), echo=False)

table_qcc = 'qichacha'


def create_newtable(engine):
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        raise ('--------------create_all err：创建表失败--------------')


def get_sqlsession(engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as e:
        raise ('--------------engine err: 数据库连接错误--------------')



class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @staticmethod
    def set_attrs(attrs_datas, obj):
        if not isinstance(attrs_datas, dict):
            try:
                attrs_datas = json.loads(attrs_datas)
            except Exception as e:
                raise e

        for k, v in attrs_datas.items():
            if hasattr(obj, k) and k != 'id':
                setattr(obj, k, str(v))

    @classmethod
    def save_mode(cls, session, model, item):
        if item:
            item_data = item.__dict__['_values']
            cls.set_attrs(item_data, model)

            try:
                session.add(model)
                session.commit()
            except Exception as e:
                session.rollback()


            # with auto_commit(session):
            #     session.add(model)

    @staticmethod
    @contextmanager
    def auto_commit(session):
        try:
            yield
            session.commit()
        except Exception as e:
            session.rollback()

    @staticmethod
    def db_distinct(session, dbmodel, item, keywords):
        '''
        Db 通过url去重
        '''

        # sql = 'SELECT url from {db_name}.{table_name} WHERE url ="{keyword}" limit 1'.format(db_name=db_name,table_name=table_name,keyword=keyword)
        # result = session.execute(sql).fetchall()

        result = session.query(dbmodel).filter_by(url=keywords).first()
        if result:
            raise DropItem('丢弃DB已存在的item:\n')  # DropItem 丢弃
            # pass     # 在close_spider()方法里面调用 DropItem 会报一个异常： ERROR: Scraper close failure,  所以直接pass也行
        else:
            return item

class QccModel(BaseModel):
    __tablename__ = table_qcc

    url = Column(String(500))

    logo_ico = Column(String(500))
    centent_title = Column(String(500))
    centent_mobile = Column(String(100))
    centent_index = Column(String(500))
    centent_email = Column(String(100))
    centent_address = Column(String(500))
    license = Column(String(500))
    faren = Column(String(100))
    detail = Column(Text())


