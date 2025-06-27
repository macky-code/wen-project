from django.contrib.auth import views as auth_views
from django.urls import path, include
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

    # 密码重置相关路由
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             success_url='/users/password_reset/done/'
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/users/reset/done/'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]





