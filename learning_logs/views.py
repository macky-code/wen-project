# learning_logs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.utils import timezone
from datetime import timedelta

from .models import Topic, Entry, Habit, HabitCheckin, HabitLog
from .forms import TopicForm, EntryForm, HabitForm, HabitLogForm


# ==================== 基础页面 ====================
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')


def user_home(request):
    return render(request, 'user_home.html')


def profile(request):
    # 用户资料页面的逻辑
    return render(request, 'learning_logs/profile.html')


# ==================== Topic相关视图 ====================
@login_required
def topics(request):
    """显示当前用户的所有主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """显示单个话题及其所有条目"""
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def topic_detail(request, id):
    topic = get_object_or_404(Topic, id=id)
    return render(request, 'learning_logs/topic_detail.html', {'topic': topic})


@login_required
def new_topic(request):
    """添加新话题"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    else:
        form = TopicForm()

    return render(request, 'learning_logs/new_topic.html', {'form': form})


@login_required
def edit_topic(request, topic_id):
    """编辑话题"""
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, '话题更新成功！')
            return redirect('learning_logs:topic_detail', id=topic.id)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'learning_logs/edit_topic.html', {'form': form, 'topic': topic})


# ==================== Entry相关视图 ====================
def entry_detail(request, id):
    entry = get_object_or_404(Entry, id=id)
    return render(request, 'learning_logs/entry_detail.html', {'entry': entry})


@login_required
def new_entry(request, topic_id):
    """为特定话题添加新条目"""
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    else:
        form = EntryForm()

    return render(request, 'learning_logs/new_entry.html', {'form': form, 'topic': topic})


@login_required
def edit_entry(request, entry_id):
    """编辑条目"""
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    topic = entry.topic

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, '条目更新成功！')
            return redirect('learning_logs:topic_detail', id=topic.id)
    else:
        form = EntryForm(instance=entry)

    return render(request, 'learning_logs/edit_entry.html', {'form': form, 'entry': entry, 'topic': topic})


# ==================== Habit相关视图 ====================
@login_required
def habits(request):
    """显示当前用户的所有习惯及打卡状态"""
    today = timezone.now().date()
    habits = Habit.objects.filter(owner=request.user)

    # 优化查询，避免N+1问题
    checked_habits = set(
        HabitCheckin.objects.filter(
            habit__in=habits,
            date=today
        ).values_list('habit_id', flat=True)
    )

    habit_status = {}
    for habit in habits:
        habit_status[habit] = habit.id in checked_habits

    context = {'habit_status': habit_status}
    return render(request, 'learning_logs/habits.html', context)


@login_required
def add_habit(request):
    """添加新习惯"""
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            new_habit = form.save(commit=False)
            new_habit.owner = request.user
            new_habit.save()
            return redirect('learning_logs:habits')
    else:
        form = HabitForm()

    context = {'form': form}
    return render(request, 'learning_logs/add_habit.html', context)


@login_required
def checkin(request, habit_id):
    """执行打卡动作"""
    habit = get_object_or_404(Habit, id=habit_id, owner=request.user)
    today = timezone.now().date()

    # 如果今天还没打卡，则添加一条记录
    HabitCheckin.objects.get_or_create(habit=habit, date=today)

    return redirect('learning_logs:habits')


@login_required
def habit_history(request, habit_id):
    """显示特定习惯的打卡历史记录"""
    habit = get_object_or_404(Habit, id=habit_id, owner=request.user)
    checkins = HabitCheckin.objects.filter(habit=habit).order_by('-date')

    context = {
        'habit': habit,
        'checkins': checkins,
    }
    return render(request, 'learning_logs/habit_history.html', context)


# ==================== HabitLog相关视图 ====================
@login_required
def habit_log_view(request, habit_id):
    """显示习惯的所有日志记录"""
    habit = get_object_or_404(Habit, id=habit_id, owner=request.user)
    logs = HabitLog.objects.filter(habit=habit).order_by('-date')

    context = {
        'habit': habit,
        'logs': logs,
    }
    return render(request, 'learning_logs/habit_logs.html', context)


@login_required
def habit_log_weekly_view(request, habit_id):
    """显示习惯的周视图"""
    habit = get_object_or_404(Habit, id=habit_id, owner=request.user)
    today = timezone.now().date()
    week_start = today - timedelta(days=6)

    logs = HabitLog.objects.filter(
        habit=habit,
        date__range=[week_start, today]
    )
    log_dates = {log.date for log in logs}
    date_range = [week_start + timedelta(days=i) for i in range(7)]

    context = {
        'habit': habit,
        'date_range': date_range,
        'log_dates': log_dates,
        'logs': logs,
    }
    return render(request, 'learning_logs/habit_logs_weekly.html', context)


@login_required
def add_habit_log(request, habit_id):
    """添加习惯日志"""
    habit = get_object_or_404(Habit, id=habit_id, owner=request.user)

    if request.method == 'POST':
        form = HabitLogForm(request.POST)
        if form.is_valid():
            habit_log = form.save(commit=False)
            habit_log.habit = habit
            habit_log.owner = request.user
            habit_log.date = timezone.now().date()
            habit_log.save()

            messages.success(request, f'日志提交成功！习惯"{habit.name}"的记录已保存。')
            return redirect('learning_logs:habit_log', habit_id=habit.id)
    else:
        form = HabitLogForm()

    return render(request, 'learning_logs/add_habit_log.html', {
        'form': form,
        'habit': habit
    })


@login_required
def all_habit_logs(request):
    """显示用户的所有习惯日志"""
    logs = HabitLog.objects.filter(owner=request.user).order_by('-date')
    context = {'logs': logs}
    return render(request, 'learning_logs/all_habit_logs.html', context)


# ==================== 删除相关的类视图 ====================
class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = "learning_logs/topic_confirm_delete.html"
    success_url = reverse_lazy("learning_logs:index")

    def get_queryset(self):
        """确保用户只能删除自己的话题"""
        return Topic.objects.filter(owner=self.request.user)


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'learning_logs/entry_confirm_delete.html'

    def test_func(self):
        entry = self.get_object()
        return entry.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy('learning_logs:topic', kwargs={'topic_id': self.object.topic.id})

    def delete(self, request, *args, **kwargs):
        messages.success(request, '条目删除成功！')
        return super().delete(request, *args, **kwargs)