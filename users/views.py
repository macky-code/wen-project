from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from learning_logs.models import Habit, Topic, Entry
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户已创建，欢迎 {username}！')
            return redirect('users:user_home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request):
    return render(request, 'users/profile.html')


def index(request):
    topics = Topic.objects.order_by('date_added')
    entries = Entry.objects.order_by('date_added')
    context = {'topics': topics, 'entries': entries}
    return render(request, 'learning_logs/index.html', context)


@login_required
def user_home(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    entries = Entry.objects.filter(topic__owner=request.user).order_by('date_added')
    habits = Habit.objects.filter(owner=request.user).order_by('created_at')
    context = {'topics': topics, 'entries': entries, 'habits': habits}
    return render(request, 'users/user_home.html', context)


@login_required
def new_topic(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic_name')
        if topic_name:
            Topic.objects.create(text=topic_name, owner=request.user)
            messages.success(request, '新话题已添加！')
            return redirect('users:user_home')
        else:
            messages.error(request, '话题名称不能为空！')
    return render(request, 'users/new_topic.html')


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    if request.method == 'POST':
        entry_text = request.POST.get('entry_text')
        if entry_text:
            Entry.objects.create(text=entry_text, topic=topic)
            messages.success(request, '新条目已添加！')
            return redirect('users:user_home')
        else:
            messages.error(request, '条目内容不能为空！')
    return render(request, 'users/new_entry.html', {'topic': topic})
