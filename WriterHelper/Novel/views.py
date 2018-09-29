from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .forms import SearchForm
from .tools import SearchTools
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def index(request):
    # form=SearchForm()
    return render(request, "SearchPage.html")

def search(request):
    res={}
    res.setdefault("words",request.POST["words"])
    idioms = SearchTools.SearchRes(res).search_idioms()
    novels = SearchTools.SearchRes(res).search_novels()
    data={
        "idioms":idioms,
        "novels":novels,
    }
    return JsonResponse(data)

