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

# import asyncio
# from aiomultiprocess import Pool

# def html_parse(self, url):
#     '''
#     解析网页返回beautifulsoap对象
#     :param url: url
#     :return: beautifulsoap对象
#     '''
#     headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) "
#                              "AppleWebKit/537.36 (KHTML, like Gecko)"
#                              " Chrome/63.0.3239.132 Safari/537.36"}
#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             return BeautifulSoup(response.text, "html.parser")
#     except RequestException as e:
#         print(e.args)
#     return None
#
#
# print(int(1801/9)+1801%9)
# print(1801//9)
# print(1800/9)
# print(1799/9)
#
#

from multiprocessing import Queue,Process,freeze_support
from threading import Thread
import queue,time

def put_q(q):
    for url in range(1,100):
        q.put(url)
        print("put into queue:",url,"\n")

def get_q(q):
    while True:
        if not q.empty():
            if q.qsize() >9:
                url = q.get()
                print("get from queue:", url,"\n")
        else:
            break
#
# if __name__ == '__main__':
#     # freeze_support()
#     # q=Queue()
#     # p1=Process(target=put_q,args=(q,))
#     # p2=Process(target=get_q,args=(q,))
#     # for p in [p1,p2]:
#     #     p.start()
#     # for p  in (p1,p2):
#     #     p.join()
#
#     q=queue.Queue()
#     p1=Thread(target=put_q,args=(q,))
#     p2=Thread(target=get_q,args=(q,))
#     for p in [p1, p2]:
#         p.start()
#     for p  in (p1,p2):
#         p.join()
#
# import os
# print(len([file for file in os.listdir('D:\gitdata\gitdataRes\python_learning\python_learning\SentenceMaking\SentenceMaking\data\天蚕土豆\斗破苍穹')]))
list=[1,2,"3"]
print(list.pop(2))

