# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'zhu733756'
"""
from __future__ import division,print_function
import os,shelve,re,jieba,shutil
import jieba.posseg as pseg
from collections import Counter
import logging,sys,time,json
import pandas as pd
from multiprocessing import Pool,Process
from tqdm import tqdm
sys.setrecursionlimit(1000000)#防止迭代超过上限报错

# logger=logging.getLogger("spider.sub")
class lazyproperty(object):

    def __init__(self,func):
        self.func=func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value=self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value

class SentenceMaking(object):

    def __init__(self,split_keywords):
        self.split_keywords=split_keywords

    @classmethod
    def open_db(cls,key=None):
        path="./SentenceKey/%s/"%key
        if not os.path.exists(path):
            os.mkdir(path)
        with shelve.open(path+key) as f:
             try:
                 data=f[key]
             except:
                 data={}
        print("Total quantity of last saved(Key:%s):"%key.capitalize(), len(data))
        return cls(split_keywords=data)

    @lazyproperty
    def idioms(self):
        return json.dumps(list(pd.read_json(r'../chinese_xinhua/data/idiom.json',\
                            encoding="utf-8").loc[:, "word"]))
    @lazyproperty
    def stopwords(self):
        return  "".join(map(str.strip,
                        open("./config/stopwords.txt","r",
                             encoding="utf-8").readlines()))

    def transfer_to_string(self,mode):
        fiter_files=[filename \
                        for filename in os.listdir(mode) \
                        if re.search("(^第.*章.*)", filename)]
        for filename in fiter_files:
            yield os.path.join(mode, filename)

    def get_total(self,mode):
        return len([file for file in os.listdir(mode)])

    @staticmethod
    def get_strings(path):
        return filter(lambda x: x,
                         map(str.strip, open(path,\
                        "r", encoding="utf-8").readlines()))

    def make_idioms(self,path):
        for sentence in self.get_strings(path):
            if sentence[0] in ('“', '”', '"', '"') or \
                            sentence[-1] in ('“', '”', '"', '"'):
                continue
            for tag in jieba.cut(sentence, cut_all=False):
                if len(tag)<4:
                    continue
                if tag.isdigit():
                    continue
                if tag in json.loads(self.idioms):
                    self.split_keywords.setdefault(tag, set()).add(sentence)
        else:
            todir=os.path,join(os.path.split(path)[0],finished)
            if not os.path.exists(path):
                os.mkdir(todir)
            shutil.move(path,todir+"/"+os.path.split(path)[-1])
            self.save_db(self.split_keywords,"idiom")

    def make_verbs(self,path):
        for sentence in self.get_strings(path):
            if sentence[0] in ('“', '”', '"', '"') or \
                     sentence[-1] in ('“', '”', '"', '"'):
                continue
            for tag,flag in pseg.cut("".join(sentence)):
                tag=tag.strip()
                if not tag:
                    continue
                if tag.isdigit():
                    continue
                if flag =="v":
                    if tag[0] in "不无了" :
                        continue
                    if len(tag)>=2 and tag[1] in "不上下":
                        continue
                    if tag in self.stopwords:
                        continue
                    self.split_keywords.setdefault(tag,set()).add(sentence)
        else:
            self.save_db(self.split_keywords,"verb")

    @staticmethod
    def save_db(info,key):
        s = shelve.open("./SentenceKey/%s/%s" % (key,key))
        try:
            s[key] = info
        finally:
            s.close()

def generate_key(key,mode):
    if key not in ("verb","idiom"):
        raise ValueError("Cannot find such key(%s)"%key)
    instance = SentenceMaking.open_db(key)
    total = instance.get_total(mode)
    func_name="make_"+key+"s"
    if hasattr(instance,func_name):
        func=getattr(instance,func_name)
    with Pool(5) as pool:
        _ = [x for x in tqdm(
                pool.imap(func=func,
                          iterable=instance.transfer_to_string(mode)),
                          total=total,
                          desc="Extract Key(%s|%s)"% (os.path.split(mode)[-1],key))]

if __name__ == "__main__":

    generate_key("verb","./data/天行")
    generate_key("idiom","./data/天行")




