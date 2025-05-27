
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from learning_logs.models import Habit # 从新的位置导入 Habit 模型

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name']
        labels = {'name': '习惯名称'}


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # 添加邮箱字段

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




