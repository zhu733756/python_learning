# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'zhu733756'
"""
# split_keywords={}
# split_keywords.setdefault("tag",set()).add("123")
# print(split_keywords)
#
# split_keywords.setdefault("tag",set()).add("123")
# print(split_keywords)


from __future__ import division
from multiprocessing import Pool,freeze_support
from tqdm import tqdm_gui,tqdm
# class A(object):
#
#     def __init__(self,count):
#         self._count=count
#
#     @classmethod
#     def get_cls(cls):
#         count=1
#         return cls(count=count)
#
#     def get_num(self,num):
#         print(self._count,num)
#
# import sys,time,os
# if __name__=='__main__':
#     # freeze_support()
#     with Pool(5) as pool:
#         pool.map(A.get_cls().get_num,range(1000))

import asyncio
from aiomultiprocess import Pool

def html_parse(self, url):
    '''
    解析网页返回beautifulsoap对象
    :param url: url
    :return: beautifulsoap对象
    '''
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) "
                             "AppleWebKit/537.36 (KHTML, like Gecko)"
                             " Chrome/63.0.3239.132 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
    except RequestException as e:
        print(e.args)
    return None


