# -*- coding: utf-8 -*-
"""
@author: zh
"""

import requests,re
from requests import RequestException

class CrawlSpider(object):

    def __init__(self):pass

class BookInfoSpider(object):

    def split_search_key(self,*args,**kwargs):
        arg_res = []
        kw_res = []
        if args:
            for searchkey in args:
                tmp=self.html_parser(searchkey)
                if tmp:
                    arg_res.extend(tmp)
            arg_res=list(self.remove_duplicate(arg_res))
        if kwargs:
            for k,v in kwargs.items():
                k_search=self.html_parser(k,"accurate")
                v_search=self.html_parser(v,"accurate")
                if k_search and v_search:
                    kw_res.extend(k_search)
                    kw_res.extend(v_search)
                else:
                    return "该作者没有这样的书籍！"
                kw_res=list(self.remove_duplicate(
                         [res for res in kw_res
                                if k in res.values() and v in res.values()]))
        if arg_res and kw_res:
            arg_res.extend(kw_res)
            return arg_res
        else:
            return arg_res if arg_res else kw_res

    @staticmethod
    def remove_duplicate(dup_list):
        seen=set()
        for lis in dup_list:
            author=lis["author"]
            bookname=lis["bookname"]
            if (author,bookname) not in seen:
                yield lis
                seen.add((author,bookname))

    def html_parser(self,search_key,mode="all"):
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
            resList=[]
            for res in result:
                book_info={
                    "href":res[0],
                    "bookname":res[1],
                    "author":res[2],
                    "update_time":res[3]
                    }
                if mode=="accurate":
                    if res[1]==search_key or res[2]==search_key:
                        resList.append(book_info)
                else:
                    if res[1] == search_key or res[2] == search_key:
                        resList.insert(0,book_info)
                    else:
                        resList.append(book_info)
            return resList
        except RequestException as e:
            print(e.args)
            return None
