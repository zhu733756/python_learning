from django.shortcuts import render
from django.http import JsonResponse
from .tools import SearchTools,Crawler
import os

def index(request):
    return render(request, "menu.html")

def search_dir(request):
    req=request.POST.get("author_s")
    idioms_path = SearchTools.SearchRes.find_searchKey("idiom")
    novels_path = SearchTools.SearchRes.find_searchKey("verb")
    idioms_path.extend(novels_path)
    author_info_path=set([os.path.dirname(path) for path in idioms_path])
    info_dir={}
    if req:
        for path in author_info_path:
            author, book = os.path.split(path)[-1].split("-")[:]
            if  req in path:
                info_dir.setdefault(author,[]).append(book)
    else:
        for path in author_info_path:
            author, book = os.path.split(path)[-1].split("-")[:]
            info_dir.setdefault(author,[]).append(book)
    if info_dir:
        return JsonResponse(info_dir)
    else:
        return JsonResponse("没有检测到可用书籍信息！",safe=False)

def search_form(request):
    res={}
    res.setdefault("words",request.POST["words"])
    idioms = SearchTools.SearchRes(res).search_idioms()
    novels = SearchTools.SearchRes(res).search_novels()
    data={
        "idioms":idioms,
        "novels":novels,
    }
    return JsonResponse(data)

def search_booklist(request):
    book_req=request.POST.get("search_key")
    search_spider=Crawler.BookInfoSpider()
    if ";" or ":" not in book_req:
        res=search_spider.split_search_key(book_req)
        if res:
            return JsonResponse(res)
    if ";" in book_req:
        book_req=book_req.replace("；",";").replace("：",":")
        args=[arg for arg in book_req.split(";")[:] if ":" not in arg]
        kwargs=[arg for arg in book_req.split(";")[:] if arg not in args]
        print(args,kwargs)
        if kwargs:
            kwargs={item.split(":")[0]:item.split(":")[1] for item in kwargs}
            all_res=search_spider.split_search_key(*args,**kwargs)
            print("all:",all_res)
            return JsonResponse(all_res,safe=False)
        return JsonResponse(search_spider.split_search_key(*args))



