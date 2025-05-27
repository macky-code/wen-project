
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry

from django.contrib import admin
# from .models import Habit
# from .models import Habit, HabitLog

# admin.site.register(Habit)
# admin.site.register(HabitLog)


admin.site.register(Topic)
admin.site.register(Entry)



@login_required
def user_home(request):
    """用户登录后的主页"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'users/user_home.html', context)





