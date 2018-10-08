from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .forms import SearchForm
from .tools import SearchTools
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import os

def index(request):
    return render(request, "SearchPage.html")

def search_dir(request):
    idioms_dir = SearchTools.SearchRes.find_searchKey("idiom")
    verb_dir = SearchTools.SearchRes.find_searchKey("verb")
    idioms_dir.extend(verb_dir)
    author_nov_list = {}
    for path in idioms_dir:
        author_nov_list.setdefault(
            os.path.split(os.path.dirname(path))[-1], []) \
            .append(os.path.split(path)[-1].split(".")[0])
    # print(author_nov_list)
    # #{'失落叶-天行': ['idiom', 'verb']}
    return JsonResponse(author_nov_list)

def search(request):
    res={}
    if request.POST.get("author"):
        print(author)
    res.setdefault("words", request.POST["words"])
    idioms = SearchTools.SearchRes(res).search_idioms()
    novels = SearchTools.SearchRes(res).search_novels()
    data={
        "idioms":idioms,
        "novels":novels,
    }
    return JsonResponse(data)

