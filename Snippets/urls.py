from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='add_snippet_page'),
    path('snippets/list', views.snippets_page, name='snippets_page'),
    path('snippet/<int:snippet_id>', views.snippet, name='snippet'),
    path('snippet/<int:snippet_id>/delete', views.snippet_delete, name='snippet_delete'),
    path('snippet/<int:snippet_id>/edit', views.snippet_edit, name='snippet_edit'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    
    # path('snippets/create', views.snippet_create, name='snippet_create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
