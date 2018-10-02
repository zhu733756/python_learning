from django.shortcuts import render
from django.http import JsonResponse
from .tools import SearchTools
import os

def index(request):
    return render(request, "menu.html")

def search_dir(request):

    req=request.POST.get("author_s")
    info={}
    idioms_path = SearchTools.SearchRes.find_searchKey("idiom")
    novels_path = SearchTools.SearchRes.find_searchKey("verb")
    idioms_path.extend(novels_path)
    for path in idioms_path:
        if req in path:
            author,book=os.path.split(os.path.dirname(path))[-1].split("-")[:]
            if author in info:
                if book in info[author]:
                    continue
            info.setdefault(author,[]).append(book)
    if info:
        print(info)
        return JsonResponse(info)
    else:
        return JsonResponse("没有检测到可用数据！",safe=False)

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

