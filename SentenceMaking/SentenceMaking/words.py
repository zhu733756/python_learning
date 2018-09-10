# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'zhu733756'
"""
import os,shelve,re,jieba
import jieba.posseg as pseg
from collections import Counter
import logging,sys
import pandas as pd
from multiprocessing import Pool
sys.setrecursionlimit(1000000)#防止迭代超过上限报错

# logger=logging.getLogger("spider.sub")
idoims=pd.read_json(r'D:\gitdata\gitdataRes\SentenceMaking\chinese_xinhua\data\idiom.json',encoding="utf-8").loc[:,"word"]
stopwords = "".join(map(str.strip,
                        open(os.path.abspath("./config/stopwords.txt"),
                        "r", encoding="utf-8").readlines()))

class SentenceMaking(object):

    def __init__(self,split_keywords):
        self.split_keywords=split_keywords

    @classmethod
    def open_db(cls,key=None):
        if key is None:
            raise ValueError("Cannot find a key!")
        with shelve.open("./data/SentenceKey/info") as f:
             try:
                 data=f[key]
             except:
                 data={}
             print("last saved:", data)
             return cls(split_keywords=data)


    def get_filter_files(self,path):
        return [filename \
                for filename in os.listdir(path) \
                if re.search("(^第.*章.*)", filename)]

    def transfer_to_string(self,path="./data/天行"):
        for filename in self.get_filter_files(path):
            yield os.path.join(path, filename)

    def make_idioms(self,path):
        for sentence in self.get_strings(path):
            for tag in jieba.cut("".join(sentences), cut_all=False):
                if tag not in list(idoims):
                    continue
                elif tag in sentence:
                    self.split_keywords.setdefault(tag,[]).append(sentence)

    def db_close(self,key):
        with shelve.open("./data/SentenceKey/info") as f:
            try:
                f[key]=self.split_keywords
            finally:
                f.close()

    def get_total(self):
        return len([file for file in os.listdir("./data/天行")])

    @staticmethod
    def get_strings(path):
        return filter(lambda x: x,
                         map(str.strip, open(path,\
                        "r", encoding="utf-8").readlines()))

    def make_verb(self,path):
        filename=os.path.split(path)[-1]
        print("正在处理文件:%s" % filename)
        for sentence in self.get_strings(path):
            if sentence[0] in ('“', '”', '"', '"') or \
                                    sentence[-1] in ('“', '”', '"', '"'):
                continue
            for tag,flag in pseg.cut("".join(sentence)):
                tag=tag.strip()
                if flag =="v":
                    if not tag:
                        continue
                    if tag.isdigit():
                        continue
                    if tag[0] in "不无" :
                        continue
                    if len(tag)>=2 and tag[1] in "不上下":
                        continue
                    if tag in stopwords:
                        continue
                    if tag in self.split_keywords and\
                        sentence in self.split_keywords[tag]:
                            continue
                    self.split_keywords.setdefault(tag, []).append(sentence)
        else:
            print("文件(%s)处理完毕"%filename)

if __name__ == "__main__":

    # with Pool(5) as pool:
    #     instance = SentenceMaking.open_db(key="verb")
    #     pool.map(func=instance.make_verb,iterable=instance.transfer_to_string())
    #     instance.db_close(key="verb")

    with Pool(5) as pool:
        instance = SentenceMaking.open_db(key="idiom")
        pool.map(func=instance.make_idioms,iterable=instance.transfer_to_string())
        instance.db_close(key="idiom")



