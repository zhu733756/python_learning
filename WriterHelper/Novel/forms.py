# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     
   Description：
-------------------------------------------------
__author__ = 'zhu733756'
"""
from django import forms
import os
# author_novel_choices=[(lines.strip().split("-")[0],lines.strip().split("-")[1])
#                             for lines in open(r'D:\gitdata\gitdataRes\python_learning\python_learning'
#                                   r'\SentenceMaking\SentenceMaking\Sentencekey\author_novel.txt',
#                                         "r",encoding="utf-8")]
#
# author_choices=[(author,author) for author,novel in author_novel_choices]
# novel_choices=[(novel,novel) for author,novel in author_novel_choices]

class SearchForm(forms.Form):
    words=forms.CharField(max_length=100,required=True)
    # author=forms.ChoiceField(widget=forms.RadioSelect,choices=author_choices,required=False)
    # novel_name=forms.ChoiceField(widget=forms.RadioSelect,choices=novel_choices,required=False)