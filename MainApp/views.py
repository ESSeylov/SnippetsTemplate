from django.http import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'GET':
        
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                   'form': form
                   }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snippets_page')
        return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    q = Snippet.objects.all()
    len_q = len(q)
    context = {'q': q, 'pagename': 'Список сниппетов', 'len_q': len_q}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404("Snippet does not exist")
    context = {'snippet': snippet, 'pagename': 'Просмотр сниппета'}
    return render(request, 'pages/view_snippet.html', context)


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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))