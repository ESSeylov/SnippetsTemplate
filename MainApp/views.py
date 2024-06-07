from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth

from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {"pagename": "PythonBin"}
    return render(request, "pages/index.html", context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {"pagename": "Добавление нового сниппета", "form": form}
        return render(request, "pages/add_snippet.html", context)
    elif request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets_page")
        return render(request, "pages/add_snippet.html", {"form": form})


def snippets_page(request):
    q = Snippet.objects.all()
    len_q = len(q)
    context = {"q": q, "pagename": "Список сниппетов", "len_q": len_q}
    return render(request, "pages/view_snippets.html", context)


def snippet(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404("Snippet does not exist")
    context = {"snippet": snippet, "pagename": "Просмотр сниппета", "view": True}
    return render(request, "pages/view_snippet.html", context)


# def snippet_create(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         lang = request.POST['lang']
#         code = request.POST['code']
#         snippet = Snippet(name=name, lang=lang, code=code)
#         snippet.save()
#         return redirect('snippets_page')


def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def snippet_edit(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404("Snippet does not exist")
    if request.method == "GET":
        snippet = {
            "pagename": "Редактирование сниппета",
            "snippet": snippet,
            "view": False,  
        }
        return render(request, "pages/view_snippet.html", snippet)
    if request.method == "POST":
        form_data = request.POST
        snippet.name = form_data["name"]
        snippet.code = form_data["code"]
        snippet.save()
        return redirect("snippets_page")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            pass
        return redirect("home")


def logout(request):
    auth.logout(request)
    return redirect(request.META.get("HTTP_REFERER", "/"))
