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

def get_num(num):
    return num+1

import sys,time,os
if __name__=='__main__':
    # freeze_support()
    with Pool(5) as pool:
        _=[x for x in tqdm(pool.imap(get_num,range(101)),total=100)]




