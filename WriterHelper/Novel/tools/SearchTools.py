# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'zhu733756'
"""
import pandas as pd
import os,json

class SearchRes(object):

    def search_idioms(self, data):
        if len(data["words"]) < 4:
            print("不符合规则！")
        idioms=pd.read_json(r'H:\python_list\python_learning\WriterHelper\Novel\idiom.json',encoding="utf-8")
        if any(idioms.loc[:,"word"].str.contains(data["words"])):
            result=idioms[idioms.word==data["words"]].to_dict()
            for k, v in result.items():
                for vi in v.values():
                    print({k :vi})
        else:
             print("no such idioms!")

    def search_novels(self, data):

        if len(data["words"]) <= 2:
            searchJsonKey="verb.json"
        else:
            searchJsonKey="idiom.json"

        searchlis=[]

        for path in self.find_searchKey(searchJsonKey):
            with open(path,"r",encoding="utf-8") as f:
                for lines in f:
                    lines=lines.strip()
                    if data["words"] in json.loads(lines):
                        searchlis.append(lines)

        if searchlis:
            return searchlis
        else:
            return "没有找到匹配结果！"

    def find_searchKey(self,searchKey):

        res=[]
        for dirname in os.listdir(r"D:\gitdata\gitdataRes\python_learning\python_learning\
                                                    SentenceMaking\SentenceMaking\Sentencekey"):
            if os.path.isdir(dirname):
                for file in os.listdir(dirname):
                    if file ==searchKey:
                        res.append(os.path.realpath(file))
        return res



SearchRes().search_idioms(data={"key":"idioms","words":"见异思迁"})
