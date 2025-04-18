from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Snippet listing and browsing
    path('', views.snippet_list, name='snippet_list'),
    path('tag/<slug:tag_slug>/', views.snippet_list_by_tag, name='snippet_list_by_tag'),
    path('language/<slug:language_slug>/', views.snippet_list_by_language, name='snippet_list_by_language'),
    path('search/', views.snippet_search, name='snippet_search'),
    
    # Snippet CRUD operations
    path('create/', views.snippet_create, name='snippet_create'),
    path('<slug:slug>/', views.snippet_detail, name='snippet_detail'),
    path('<slug:slug>/edit/', views.snippet_edit, name='snippet_edit'),
    path('<slug:slug>/delete/', views.snippet_delete, name='snippet_delete'),
    
    # Snippet actions
    path('<slug:slug>/like/', views.snippet_like, name='snippet_like'),
    path('<slug:slug>/download/', views.snippet_download, name='snippet_download'),
    path('<slug:slug>/comment/', views.snippet_comment, name='snippet_comment'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
] 