from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Topic views
    path('', views.topic_list, name='topic_list'),
    path('topic/create/', views.topic_create, name='create_topic'),
    path('topic/<slug:slug>/', views.topic_detail, name='topic_detail'),
    
    # Discussion views
    path('discussion/create/', views.discussion_create, name='discussion_create'),
    path('discussion/<slug:slug>/', views.discussion_detail, name='discussion_detail'),
    path('discussion/<slug:slug>/edit/', views.discussion_edit, name='discussion_edit'),
    path('discussion/<slug:slug>/delete/', views.discussion_delete, name='discussion_delete'),
    path('discussion/<slug:slug>/close/', views.discussion_close, name='discussion_close'),
    path('discussion/<slug:slug>/pin/', views.discussion_pin, name='discussion_pin'),
    
    # Reply views
    path('reply/<int:pk>/edit/', views.reply_edit, name='reply_edit'),
    path('reply/<int:pk>/delete/', views.reply_delete, name='reply_delete'),
    path('reply/<int:pk>/mark-solution/', views.reply_mark_solution, name='reply_mark_solution'),
    
    # User views
    path('user/<str:username>/discussions/', views.user_discussions, name='user_discussions'),
    path('user/<str:username>/replies/', views.user_replies, name='user_replies'),
    
    # Notification views
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark-all-read/', views.notification_mark_all_read, name='notification_mark_all_read'),
    
    # Search
    path('search/', views.discussion_search, name='discussion_search'),
] 