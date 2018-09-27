from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .forms import SearchForm
from .tools import SearchTools
import json

def search(request):
    if request.is_ajax():
        js_data=json.load(request.body.decode())
        data = {
            "key": js_data.get("key"),
            "words": js_data.get("words"),
        }
        print(data)
        res = SearchTools.SearchRes(data).search()
        return HttpResponse(res, content_type='application/json')
    else:
        return render(request,"SearchPage.html")




