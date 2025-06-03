from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='邮箱',
        help_text='请输入有效的邮箱地址。'
    )

    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        help_text='密码必须包含至少 8 个字符，不能太简单，也不能全部是数字。'
    )

    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
        help_text='请再次输入相同的密码以确认。'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': '用户名',
        }
        help_texts = {
            'username': '必填。150 个字符以内，仅可包含字母、数字和 @/./+/-/_ 符号。',
        }






