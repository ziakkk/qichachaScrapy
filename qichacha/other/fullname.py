#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/10/8'
# qq:2456056533

佛祖保佑  永无bug!

"""

import os


def get_name():
    '''
    文本供应商名称
    :return: [供应商名称]
    '''
    file = os.path.join(os.path.dirname(__file__), 'fullname.txt')
    with open(file, 'r', encoding='utf-8') as f:
        name = f.readlines()

    return [n.replace('\n', '') for n in name]


if __name__ == '__main__':
    print(get_name())
