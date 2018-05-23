# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
    File Name：    mzitu_load_2018.py
    Description：  love_mzitu
-------------------------------------------------
__author__ = 'ZH'
"""
import requests
from lxml import etree
import os,time
from multiprocessing import Pool,freeze_support
import time
from random import random,choice
class get_mzitu(object):

    #常见的伪装agent列表
    UserAgent_List = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    # 随机选取一个用户代理
    headers={
             "User-Agent":choice(UserAgent_List)
            }


    def html_response(self,url,path=None,headers=None):
        '''
        如果没有header，默认用self.header，如果指定header，则用新构建的header
        如果提供path，则返回解码网页数据，
        如果没有path，则返回一个bytes网页数据
        :param url:
        :param path:
        :param headers:
        :return:
        '''
        if headers is None:
            headers=self.headers
        html_page = requests.get(url, headers=headers)
        if path is None:
            return html_page.content
        return  etree.HTML(html_page.text).xpath(path)

    def get_modeurl(self,base_url,dir):
        '''
        用base_url爬取第一级页面，通过dir/title/month创建的文件夹返回图片保存路径
        用生成器返回保存路径和第一级页面链接
        :param base_url:
        :param dir:
        :return:
        '''

        modeurl=self.html_response(base_url,path='/html/body/div[2]/div[1]/div[2]/ul[1]/li')
        for li in modeurl:
            month=li.xpath("./p[1]/em/text()")[0]
            p=li.xpath("./p[2]/a")
            for a in p:
                title=a.xpath("./text()")[0]
                for tr in ["/", ":", "<", ">", "→", "*","?"]:
                    if tr in title:
                        title= title.replace(tr, "")
                fpath = self.mkdir(dir,title,month)
                page_url = a.xpath(".//@href")[0]
                yield  fpath,page_url

    def mkdir(self,dir,title,month):
        '''
        创建图片保存路径，并返回路径
        :param dir:
        :param title:
        :param month:
        :return:
        '''
        filename=title
        path = os.path.join(dir, month)
        if not os.path.exists(path):
            os.mkdir(path)
            print(month, "has made a dir!")

        if filename not in os.listdir(path):
            os.mkdir(os.path.join(path,filename))
            print(filename, "of current loadpage make a dir!")

        return "/".join([path,filename])

    def get_son_url(self,page_url):
        '''
        获取所有二级页面的链接，用生成器返回
        :param page_url:
        :return:
        '''

        try:
            a_list = self.html_response(page_url, '//div[@class="pagenavi"]')[0]
            max_number = a_list[-2].xpath("./span/text()")[0]
            print("max:", max_number)
            for x in range(1, int(max_number) + 1):
                son_url = "/".join([page_url, str(x)])
                yield son_url
        except:
            # 抓取长图页面，并不是所有的页面都是翻页页面
            try:
                p_list = self.html_response(page_url, '//div[@class="main-image"]')[0]
                for p in p_list:
                    son_url = p.xpath("./a/img//@src")[0]
                    yield son_url
            except Exception as e:
                print("page_url:", page_url, "is valid! Because", e)

    def save_file(self,fpath, page_url):
        '''
        重构headers，访问图片链接地址，并保存在指定文件路径
        :param fpath:
        :param page_url:
        :return:
        '''
        for son_url in self.get_son_url(page_url):

            print("load url:%s" % son_url)
            try:
                item = self.html_response(url=son_url, path="/html/body/div[2]/div[1]/div[3]/p/a/img//@src")[0]
            except:
                item=son_url
            dirsonname = item.split("/")[-1]

            headers = {
                "Host": "i.meizitu.net",
                "Referer": item,
                "User-Agent": self.headers["User-Agent"]
            }

            try:
                with open(os.path.join(fpath, dirsonname), "wb") as f:
                    f.write(self.html_response(url=item,headers=headers))
                print(dirsonname, "is downloaded!")

            except Exception as e:
                print("currenturl(%s) is valid" % son_url,"Because",e)

    def main(self,dir=r"E:/dataformztu/"):
        '''
        启动函数，获取第一级页面的发path和page_url,加入进程池
        :param dir:
        :return:
        '''
        base_url = "http://www.mzitu.com/all/"
        pool=Pool(4)
        for fpath, page_url in self.get_modeurl(base_url,dir):
            pool.apply_async(func=self.save_file,args=(fpath,page_url))
            time.sleep(random()*choice(range(1,3)))
        pool.close()
        pool.join()
        print("all urls are downloaded!")

if __name__ == '__main__':
    t = time.time()
    freeze_support()
    get_mzitu().main()
    print("takes:",time.time() - t)


