from django.db import models
from django.contrib.auth.models import User
#
# class Habit(models.Model):
#     """用户的习惯，例如 '跑步'、'学单词'"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_habits_users')
#     name = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
# class HabitLog(models.Model):
#     """记录某个习惯的打卡情况"""
#     habit = models.ForeignKey('learning_logs.Habit', on_delete=models.CASCADE, related_name='habitlog_users' )  # 可以为用户的 habit 设置不同的 related_name
#     date = models.DateField(auto_now_add=True)  # 记录当天日期
#     completed = models.BooleanField(default=False)  # 是否完成
#     def __str__(self):
#         return f"{self.habit.name} - {self.date}: {'✔' if self.completed else '✘'}"

class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_topics')

    def __str__(self):
        return self.text

class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + "..."

