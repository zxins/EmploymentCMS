from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from .models import UserProfile
from django.contrib.auth.models import Group

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名称", max_length=18)
    password = forms.CharField(label="用户密码", widget=forms.PasswordInput)
    password_auth = forms.CharField(label="密码确认", widget=forms.PasswordInput)

    topic_choice = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('enterprise', '企业'),
    )
    user_type = forms.ChoiceField(label="身份", choices=topic_choice)

    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password_auth')
        if pwd1 == pwd2:
            pass
        else:
            from django.core.exceptions import ValidationError
            raise ValidationError('密码输入不一致')

# Create your views here.
def register(request):
    if request.method == 'GET':
        form = RegisterForm()

        context = {
            "app_path": request.path,
            "form": form
        }
        return render(request, 'admin/register.html', context=context)

    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = UserProfile(
                username=data['username'],
                user_type=data['user_type']
            )
            user.set_password(data['password'])
            user.save()

            group = {
                'student': '学生',
                'teacher': '教师',
                'enterprise': '企业'
            }
            group = Group.objects.get(name=group.get(data['user_type']))
            group.user_set.add(user)
            return HttpResponse("注册成功")
        else:
            errors = form.errors
            return render(request, 'admin/register.html', {'errors': errors, 'form': form})
