from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 登录路由
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # 注册路由
    path('register/', views.register, name='register'),
    # 登出路由
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # 用户主页路由
    path('user_home/', views.user_home, name='user_home'),
    path('profile/', views.profile, name='profile'),  # 用户资料页
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # path('habits/', views.habits, name='habits'),  # 新加的打卡页面路由
    # path('add_habit/', views.add_habit, name='add_habit'),
    # path('habit_log/<int:habit_id>/', views.habit_log_view, name='habit_log'),
]


