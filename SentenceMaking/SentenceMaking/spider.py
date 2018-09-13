# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：    load_biquke.py
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""
from requests import RequestException
from bs4 import BeautifulSoup
import re,os,requests,logging,sys,time
import MainLoggerConfig
import asyncio
from multiprocessing import Pool
from tqdm import tqdm
# import urllib3
import aiohttp
# urllib3.disable_warnings()
sys.setrecursionlimit(1000000)#防止迭代超过上限报错

MainLoggerConfig.setup_logging(default_path="./logs/logs.yaml")
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

class load_biquge(object):

    logger = logging.getLogger(__name__)

    def __init__(self,mother_url):

        self.mother_url=mother_url#文章链接
        self.page_str=[]
        self.path = self.get_path()


    def get_path(self):
        '''
        获取存储目录
        :return:
        '''
        first_page=self.html_parse(self.mother_url)
        path=r"./data/{}/{}". \
            format(first_page.find("p").string.strip().split("：")[-1],
                   first_page.find("div",{"id":"info"}).find("h1").string)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def html_parse(self,url):
        '''
        解析网页返回beautifulsoap对象
        :param url: url
        :return: beautifulsoap对象
        '''
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko)"
                                 " Chrome/63.0.3239.132 Safari/537.36"}
        try:
            response=requests.get(url,headers=headers)
            if response.status_code==200:
                return BeautifulSoup(response.text, "html.parser")
        except RequestException as e:
            print(e.args)
        return None

    def get_page_url(self):
        '''
        解析目标小说链接，返回章节链接
        :return: 返回章节链接
        '''
        mode_page=self.html_parse(self.mother_url)
        ddList = mode_page.find_all("dd")
        for dd in ddList:
            if dd.find("a"):
                yield dd.find("a").get("href")

    def get_one_page(self,page_content):
        '''
        异步获取一个章节链接，保存为txt文件
        :param page_url: 章节链接
        :return:
        '''
        # time.sleep(1)
        text=[]
        if page_content:
            title = re.compile(r"\*").sub("", page_content.find("h1").string).strip()
            txt_content=page_content.find("div",id="content").stripped_strings
            for i in txt_content:
                if re.search(r"52bqg\.com",i):
                    continue
                text.append(i)
            with open(os.path.join(self.path,title)+".txt","w+",encoding="utf-8") as f:
                f.write("\n".join(text))
            self.logger.debug("Successfully downloaded a file:%s.txt" % title)
        else:
            print("err!")

    @staticmethod
    async def async_html_parse(url,res_list):
        '''
        异步获取指定url的response
        :param url:
        :return:
        '''
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko)"
                                 " Chrome/63.0.3239.132 Safari/537.36"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers=headers)as response:
                assert response.status==200
                res_list.append(BeautifulSoup(await response.text(),"html.parser"))
                # yield await response.text()

if "__main__"==__name__:

    m = load_biquge('https://www.biquge5200.cc/0_844')

    res_list=[]
    tasks=[asyncio.ensure_future(m.async_html_parse(url,res_list)) for url in list(m.get_page_url())]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    with Pool(5) as pool:
       _=[x for x in tqdm(pool.map(m.get_one_page,res_list),total=len(res_list))]










