
from .models import Topic, Entry  # 确保正确导入模型
from .models import Habit
from django import forms
from .models import HabitLog

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['completed', 'notes']
        labels = {
            'completed': '是否完成',
            'notes': '日志内容',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': '记录你今天关于这个习惯的点滴...'}),
        }



class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name']
        labels = {'name': '习惯名称'}

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': '话题内容'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': '条目内容'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


