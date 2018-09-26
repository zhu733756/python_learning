from django.shortcuts import render
from .forms import SearchForm
from tools import SearchTools

def search(request):
    if request.method =="POST":
        form=SearchForm(request.POST)
        if form.is_valid():
            data=form.clean()
            func_name="search_{}".format(data["key"])
            searchRes=SearchTools.searchRes()
            print(func_name)
            if hasattr(searchRes,func_name):
                func=getattr(searchRes,func_name)
                func(data)
            else:
                print("no such func!")
    else:
        form = SearchForm()
        return render(request, 'SearchBase.html', {'form': form})



