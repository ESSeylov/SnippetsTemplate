from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserReistrationForm


def index_page(request):
    context = {"pagename": "PythonBin"}
    return render(request, "pages/index.html", context)

@login_required
def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {"pagename": "Добавление нового сниппета", "form": form}
        return render(request, "pages/add_snippet.html", context)
    elif request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            form.save()
            return redirect("snippets_page")
        return render(request, "pages/add_snippet.html", {"form": form})


def snippets_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            q = Snippet.objects.all()
        else:
            q = Snippet.objects.filter(Q(user=request.user) | Q(public=True)).distinct()
    else:
        q = Snippet.objects.filter(public=True).all()
    len_q = len(q)
    count_all = len(Snippet.objects.all())
    context = {"q": q, "pagename": "Список сниппетов", "len_q": len_q, "count_all": count_all}
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
    if request.user.is_authenticated:
        if request.user == snippet.user or request.user.is_superuser:
            snippet.delete()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
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
        if request.user.is_authenticated:
            if request.user == snippet.user or request.user.is_superuser:
                form_data = request.POST
                snippet.name = form_data["name"]
                snippet.code = form_data["code"]
                snippet.public = form_data.get("public", False)
                snippet.save()
                return redirect("snippets_page")
            else:
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["Неверный логин или пароль"],
            }
            return render(request, "pages/index.html", context)
    return redirect("home")


def logout(request):
    auth.logout(request)
    return redirect(request.META.get("HTTP_REFERER", "/"))


def register(request):
    context = {"pagename": "Регистрация"}
    if request.method == "GET":
        form = UserReistrationForm()
        context["form"] = form
        return render(request, "pages/register.html", context)
    if request.method == "POST":
        form = UserReistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context["form"] = form
        return render(request, "pages/register.html", context)