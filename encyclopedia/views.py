from django.shortcuts import render, redirect

from markdown2 import Markdown
import secrets
from . import util


lowcase_entries = [x.lower() for x in util.list_entries()]
md = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, article):
    entry = None
    title = None
    for i in util.list_entries():
        if article.lower() == i.lower():
            entry = md.convert(util.get_entry(i))
            title = i

    return render(request, "encyclopedia/article.html", {
        "entries": [x.lower() for x in util.list_entries()],
        "entry": entry,
        "title": title,
        "entry_title": article.lower()
    })

def search(request):
    query = request.GET.get("q").strip()

    if query.lower() in [x.lower() for x in util.list_entries()]:
        return redirect("article", query)
    
    else:
        sub_entries = []
        for i in util.list_entries():
            if query.lower() in i.lower():
                sub_entries.append(i)
        return render(request, "encyclopedia/index.html", {
            "entries": sub_entries,
            "query": query,
            "search": True
        })

def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        entry = request.POST.get("entry").strip()

        if any(entry.lower() == title.lower() for entry in util.list_entries()):
            return render(request, "encyclopedia/newpage.html", {
                "title": title.lower().capitalize(),
                "exists": True
            })
        
        with open(f"entries/{title}.md", "w") as new:
            print(f"#{title}\n", file=new)
            print(entry, file=new)
        return redirect("article", title)
    
    return render(request, "encyclopedia/newpage.html")

def edit(request, article):
    if request.method=="POST":
        with open(f"entries/{article}.md", "w") as edited:
            title = request.POST.get("title").strip()
            entry = request.POST.get("entry").strip()
            print(f"#{title}\n", file=edited)
            print(entry, file=edited)
        return redirect("article", article)
    
    with open(f"entries/{article}.md") as entry:
        title = entry.readline()
        content = ""
        for line in entry:
            content += line

    return render(request, "encyclopedia/edit.html", {
        "title": title.strip("#"),
        "content": content.strip()
    })

def random(request):
    entries = util.list_entries()
    random_entry = secrets.choice(entries)
    return redirect("article", random_entry)
