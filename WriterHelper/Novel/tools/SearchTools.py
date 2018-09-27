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

    idioms_path=r"D:\gitdata\gitdataRes\python_learning\python_learning\SentenceMaking\data\idiom.json"
    novels_path=r"D:\gitdata\gitdataRes\python_learning\python_learning\SentenceMaking\SentenceMaking\Sentencekey"

    def __init__(self,data=None):
        self._data=data

    def search_idioms(self):
        if len(self._data["words"]) < 4:
            return "不符合规则！"
        idioms=pd.read_json(self.idioms_path,encoding="utf-8")
        if any(idioms.loc[:,"word"].str.contains(self._data["words"])):
            result=idioms[idioms.word==self._data["words"]]
            index=list(result.index)[0]
            return json.dumps(result.to_dict("index")[index])
        else:
            return "no such idioms!"

    def search_novels(self):

        if len(self._data["words"]) <= 2:
            searchJsonKey="verb"
        else:
            searchJsonKey="idiom"

        searchLic=[]
        for num,path in enumerate(self.find_searchKey(searchJsonKey)):
            with open(path,"r",encoding="utf-8") as f:
                lines=[line for line in f.read().split("\n") if line]
                for line in lines:
                    line=json.loads(line.strip())
                    if self._data["words"] in line:
                        searchLic.append(
                            {
                                "novel_info":os.path.split(os.path.dirname(path))[-1],
                                "chapter":line["chapter"],
                                self._data["words"]:line[self._data["words"]]
                            }
                        )
        if searchLic:
            return json.dumps(searchLic)
        else:
            return "no such %s"%searchJsonKey

    def find_searchKey(self,searchKey):

        res=[]
        for dirname in os.listdir(self.novels_path):
            dirpath=self.novels_path+"\\"+dirname
            if os.path.isdir(dirpath):
                for file in os.listdir(dirpath):
                    if searchKey in file:
                        res.append(
                            self.novels_path+"\\%s"%dirname+"\\%s"%file
                        )
        return res

    def search(self):
        func_name = "search_{}".format(self._data["key"])
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return func()
        else:
            return "没有此方法！"

# print(json.loads(SearchRes({"key":"novels","words":"不可思议"}).search()))