# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：    spider_of_moji.py
   Description：  实战（一）
-------------------------------------------------
__author__ = 'ZH'
"""

import requests,re,os,json,time
from bs4 import BeautifulSoup as bs

class get_moji_weather(object):

    base_url="https://tianqi.moji.com/weather/china"

    weather_predict={
                     "province_en":"",
                     "city":"",
                     "daily_weather_tips":"",
                     "life_tips":"",
                     "day":[],
                     "tianqi":[],
                     "temperate":[],
                      "wind":[],
                      "air":[],
                     "update_time":""
                     }

    def html_parser(self,url):
        '''
        传入指定的url，返回一个解释器是“html.parser”的beautifulsoap的对象，可用来直接解析网页数据
        :param url:
        :return:
        '''
        content=requests.get(url).text
        return bs(content,"html.parser")

    @staticmethod
    def a_not_has_http(href):
        '''
        筛选出具有href属性的标签，但个这个属性中不包含http和https
        :param href:
        :return:
        '''
        return href and not re.compile(r"http|https").search(href)

    def get_province_href(self):
        '''
        获取省区名和对应的包含cities信息的页面，用生成器返回第一级页面抓取信息
        :return:
        '''
        html_con=self.html_parser(self.base_url)
        for a in html_con.find_all(href=self.a_not_has_http):
            province=a.get_text()
            province_href="".join([self.base_url,"/",a["href"].split("/")[-1]])
            yield (province,province_href)

    @staticmethod
    def a_has_province(href):
        '''
        筛选出具有href属性的标签，但个这个属性必须包含省级英文名，不包含r"m.moji.com|today"
        :param href:
        :return:
        '''
        pattern=get_moji_weather().weather_predict["province_en"]
        return href and re.compile(pattern).search(href) \
               and not re.compile(r"m.moji.com|today").search(href)

    def get_city_and_href(self):
        '''
        获取第二级页面信息，插入省级英文名，返回一个包含省级名/城市名/城市天气信息的生成器
        :return:
        '''
        for province_name,province_href in self.get_province_href():
            html_con=self.html_parser(province_href)
            self.weather_predict["province_en"]=province_href.split("/")[-1]
            for a in html_con.find_all(href=self.a_has_province):
                yield (province_name,a.get_text(),a["href"])

    def get_city_weather(self,city, city_href ):
        '''
        通过城市名和城市url抓取第三级页面信息
        :param city:
        :param city_href:
        :return:
        '''
        self.weather_predict["city"] = city
        city_con = self.html_parser(city_href)
        wea_tips = city_con.find("div", "wea_tips clearfix").find("em").string
        self.weather_predict["daily_weather_tips"] = wea_tips

        live_index_grid = city_con.find("div", "live_index_grid")
        temp = list(live_index_grid.stripped_strings)
        for i in range(len(temp)):
            if i % 2:
                temp[i], temp[i - 1] = "".join([temp[i - 1], ";"]), "".join([temp[i], ","])
        self.weather_predict["life_tips"] = "".join(temp)

        ul_list = city_con.find_all("ul", "days clearfix")

        for ul in ul_list:
            try:
                temp2 = list(ul.stripped_strings)
                self.weather_predict["day"].append(temp2[0])
                self.weather_predict["tianqi"].append(temp2[1])
                self.weather_predict["temperate"].append(temp2[2])
                self.weather_predict["wind"].append(":".join([temp2[3], temp2[4]]))
                self.weather_predict["air"].append(temp2[5])
            except Exception as e:
                pass

        self.weather_predict["update_time"] = city_con.find("strong", "info_uptime").string


    def save_as_json(self,province,city):
        '''
        保存为json文件
        :param self:
        :param province:
        :param city:
        :return:
        '''
        path = os.path.join(os.path.abspath(os.path.dirname("__file__")), province)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(os.path.join(path, city) + ".json", "w") as f:
            f.write(json.dumps(self.weather_predict))

        print("city(%s) of province(%s) is loaded!"%(city,province))

    def main(self):
        '''
        启动函数,抓取数据，保存数据，保存后清空字典
        :param self:
        :return:
        '''
        for province, city, city_href in self.get_city_and_href():
            print("current city_href(%s) is loaded!"%city_href)
            self.get_city_weather(city,city_href)
            self.save_as_json(province,city)
            for v in self.weather_predict.values():
                if isinstance(v,str):
                    v =""
                elif isinstance(v,list):
                    v.clear()
        else:
            time.sleep(2)

if __name__=="__main__":
   get_moji_weather().main()
