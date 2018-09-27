from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .forms import SearchForm
from .tools import SearchTools
import json

def search(request):
    form=SearchForm()
    return render(request,"SearchPage.html",{"form":form})

def searchRes(request):
    key=request.GET["key"]
    words=request.GET["words"]
    data={
        "key":key,
        "words":words
    }
    res=SearchTools.SearchRes(data).search()
    return HttpResponse(res, content_type='application/json')

