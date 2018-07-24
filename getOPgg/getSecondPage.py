# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description：
-------------------------------------------------
__author__ = 'ZH'
"""

import json
import time
from datetime import datetime
from multiprocessing import Pool
import pandas
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from pyquery import PyQuery as pq


t = str(datetime.now().date()).replace("-", "")#当日日期，用来区分不同日期数据

#headers伪装
dcap=dict(DesiredCapabilities.CHROME)
dcap["chrome.page.setting.useragent"]=\
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
dcap["chrome.page.setting.referer"]=\
    "http://www.op.gg/ranking/ladder/"

#指定无头界面，也就是不开启chrome浏览器界面
opt = webdriver.ChromeOptions()
opt.set_headless()
# opt.add_argument('--headless')如果上面失效，用下面这个

#初始化浏览器
driver = webdriver.Chrome(executable_path=r"C:\Users\hr\AppData\Local\Google\Chrome\Application\chromedriver",
                          options=opt,
                          desired_capabilities=dcap
                          )
driver.set_window_size(1280, 2400)
time.sleep(2)

ChampionName = {
    "name": "",
    "champions": [],
    "kda": [],
    "win_rate": [],
    "Win": [],
    "lose": [],
}

def parse_SecondPage_by_selenium(son_url):
    '''
    解析从第一级界面得到的info_url页面数据
    :param son_url: 第一级界面得到的info_url
    :return: 返回可迭代的字典数据ChampionName
    '''
    ChampionName["name"] = son_url.split("=")[-1]
    try:
        driver.get(son_url)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[1]/div[2]/div/div[1]/div/ul/li[2]/a').click()
        time.sleep(10)
    except Exception as e:
        print("valid url",son_url,"because",e)
    else:
        doc = pq(driver.page_source)
        pageContent = doc("td.MostChampion ul")
        for x in pageContent.items("li"):
            ChampionName["champions"].append(x.find(".Name").text())
            ChampionName["win_rate"].append(x.find("div.WonLose b").text())
            ChampionName["kda"].append(x.find(".KDA").text().split()[0])
            ChampionName["Win"].append(x.find("div.WonLose span.win").text())
            ChampionName["lose"].append(x.find("div.WonLose span.lose").text())
        else:
            print(ChampionName)
            yield ChampionName
            for v in ChampionName.values():
                if isinstance(v, list):
                    v.clear()

def saved_as_json(item):
    '''
    保存为json数据
    :param item:
    :return:
    '''
    with open("rank_500_info_%s.txt" % t, "a+", encoding="utf-8") as file:
        file.write(json.dumps(item, ensure_ascii=False) + "\n")

def main(href):
    '''
    call saved_as_json
    :param href:
    :return:
    '''
    print("load url:", href)
    for item in parse_SecondPage_by_selenium(href):
        if item:
            saved_as_json(item)

if __name__ == "__main__":

    #读取json文件返回第二级页面的url列表
    # df = pandas.read_json('hanfu_rank_500_%s.txt'%t, lines=True, encoding="utf-8")
    # urls=["http:" + i for i in list(df["info_href"])]

    #如果下载失败或者没下载完全可以用以下方式“断点重连”

    #pandas读取第一级页面保存数据以及第二级保存数据
    df = pandas.read_json(r'D:\fluent_python\load_loler\hanfu_rank_500_20180724.txt', lines=True, encoding="utf-8")
    df_500_info = pandas.read_json(r'D:\fluent_python\load_loler\rank_500_info_20180724.txt', lines=True,encoding="utf-8")

    #读取所有第一级页面的info_href，提取name生成totalname列表，没有出现在第二级页面保存数据中的标记为unloaded，生成列表
    totalName=[name.split("=")[-1] for name in list(df["info_href"])]
    unloaded_url=["http://www.op.gg/summoner/userName="+ts for ts in totalName if ts not in list(df_500_info["name"])]

    #筛选出champions数据缺失或者为空列表的数据，合并起来，组成valid_urls
    df_lose = df_500_info.name[df_500_info[df_500_info.champions.str.get(-1)==""]]
    df_empty=df_500_info.name[df_500_info.champions.str.len()<3]
    df_2=list(df_lose).extend(list(df_empty))
    valid_urls = ["http://www.op.gg/summoner/userName=" + i for i in df_2]

    #合并数据在unloaded_url列表中
    unloaded_url.extend(valid_urls)
    print("total unloaded urls:",len(unloaded_url))

    with Pool(5) as pool:
        pool.map(main, unloaded_url)

    driver.close()


