from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required



# 然后添加这个视图函数
@login_required
def habit_history(request, habit_id):
    """显示特定习惯的打卡历史记录。"""
    habit = get_object_or_404(Habit, id=habit_id, owner=request.user)

    # 获取两种类型的打卡记录
    checkins = HabitCheckin.objects.filter(habit=habit).order_by('-date')
    habit_logs = HabitLog.objects.filter(habit=habit, owner=request.user).order_by('-date')

    context = {
        'habit': habit,
        'checkins': checkins,
        'habit_logs': habit_logs,
    }
    return render(request, 'learning_logs/habit_history.html', context)


class Habit(models.Model):
    """用户创建的习惯"""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_habits')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class HabitCheckin(models.Model):
    """用户的某个习惯每日打卡记录"""
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='check_ins')
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('habit', 'date')  # 每个习惯每天只能打卡一次

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

class HabitLog(models.Model):
    """记录某个习惯的打卡情况"""
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE,  related_name='habitlog_learning_logs')  # 修改 related_name，避免与 users 中冲突
    date = models.DateField(auto_now_add=True)  # 记录当天日期
    completed = models.BooleanField(default=False)  # 是否完成
    notes = models.TextField(blank=True)  # 备注，可留空
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        status = "✔" if self.completed else "✘"
        return f"{self.date} - {self.habit.name} - {status}"

class Topic(models.Model):
    """用户的学习主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics", null=True, blank=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    """某个主题下的学习条目"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}..."
