# -*- coding: utf-8 -*-
"""
@author: zh
"""

import requests,re
from requests import RequestException

class CrawlerSpider(object):

    def __init__(self):pass

class BookSpider(object):

    def __init__(self,*args,**kwargs):
        if args:
            pass

    def get_search_key(self,search_key):pass


    def html_parser(self,search_key):
        search_url='https://www.biquge5200.cc/modules/article/search.php?searchkey=%s'%search_key
        pattern=re.compile(
            r'.*?<tr>.*?'
            r'<td class="odd">.*?<a href="(.*?)">(.*?)</a>.*?</td>.*?'
            r'<td class="odd">(.*?)</td>.*?'
            r'<td class="odd" align=".*?">(.*?)</td>.*?'
            r'</tr>.*?',re.S)
        try:
            page_content=requests.get(search_url).text
            result=re.findall(pattern,page_content)
            for res in result:
                yield {
                    "href":res[0],
                    "book":res[1],
                    "author":res[2],
                    "update_time":res[3]
                }
        except RequestException as e:
            print(e.args)
            return None
