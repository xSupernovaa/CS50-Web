from turtle import title
from unittest import result
from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, title):
    # If user navigates to article via clicking on main page or adding /article_name
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/notfound.html", {
        "title" : title  
        })
    else:
        html_content = util.markdown_to_html(entry)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "html_content" : html_content
        })


def search(request):
    key = request.POST['q']
    results = util.get_search_results(key)
    return render(request, "encyclopedia/search.html", {
        "results" : results
    })


def new_page(request):
    # GET
    if request.method == 'GET':
        return render(request, "encyclopedia/newpage.html")
    # POST
    else:
        title = request.POST['title']
        title = title.replace(" ", "_")
        if util.get_entry(title) == None:
            md_content = request.POST['content']
            util.save_entry(title, md_content)
            return redirect(f"/wiki/{title}")
        else:
            return HttpResponse("Naw dawg, entry already exists.")
        


def random_page(request):
    entry = util.get_random_entry()
    return redirect(f"/wiki/{entry}")

def edit_page(request):
    if request.method == 'GET':
        # Get title by examining referer
        referer = request.META['HTTP_REFERER']
        title = referer.split('/')[-1]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title" : title, 
        "content" : content})

    else:
        md_content = request.POST['content']
        title = request.POST['title']
        util.save_entry(title, md_content)
        return redirect(f"/wiki/{title}")