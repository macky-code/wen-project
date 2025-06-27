# learning_logs/urls.py - 修复版本
from django.urls import path
from . import views
from .views import TopicDeleteView, EntryDeleteView

app_name = 'learning_logs'

urlpatterns = [
    # 首页
    path('', views.index, name='index'),

    # 话题相关 - 统一参数命名
    path('topics/', views.topics, name='topics'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),  # ✅ 修正参数名
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('delete_topic/<int:pk>/', TopicDeleteView.as_view(), name='delete_topic'),

    # 条目相关
    path('topic/<int:topic_id>/new_entry/', views.new_entry, name='new_entry'),  # ✅ 修正路径结构
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete_entry/<int:pk>/', EntryDeleteView.as_view(), name='delete_entry'),

    # 习惯相关
    path('habits/', views.habits, name='habits'),
    path('add_habit/', views.add_habit, name='add_habit'),
    path('checkin/<int:habit_id>/', views.checkin, name='checkin'),
    path('habit/<int:habit_id>/log/', views.habit_log_view, name='habit_log'),
    path('habit/<int:habit_id>/weekly/', views.habit_log_weekly_view, name='habit_weekly'),
    path('habit/<int:habit_id>/add_log/', views.add_habit_log, name='add_habit_log'),
    path('all_habit_logs/', views.all_habit_logs, name='all_habit_logs'),
    path('habit_history/<int:habit_id>/', views.habit_history, name='habit_history'),  # 添加这一行



    # 用户相关
    path('profile/', views.profile, name='profile'),
]

