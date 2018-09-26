# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'zhu733756'
"""
import  os

path=os.path.dirname(__file__)

for file in os.listdir(path):
    if os.path.isdir(file):
        with open("./author_novel.txt","a+",encoding="utf-8") as f:
            f.write(file+"\n")
else:
    print("done!")