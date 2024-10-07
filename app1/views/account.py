# 开发者：苏畅
# 2023/6/25 1:11 于上海财经大学

from django.shortcuts import render, redirect
from django import forms
from app1.utils.encrypt import md5
from app1 import models
from app1.utils.ModelForms import EmpModelForm_personal, EmpModelForm_personal_account


class LoginForm(forms.Form):
    email = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入邮箱"}),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 输入正确：验证是否正确
        print(form.cleaned_data)
        # 如果账户密码错误，则会返回一个空
        emp_object = models.EmpInfo.objects.filter(**form.cleaned_data).first()
        if not emp_object:
            # 主动添加错误
            form.add_error("email", "用户名或密码错误！")
            return render(request, 'login.html', {'form': form})

        request.session["info"] = {'id': emp_object.id, 'name': emp_object.name, 'usertype': emp_object.usertype}

        return redirect("/index/")

    else:
        return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()

    return redirect('/login/')


def personal_data_edit(request):
    """用户个人资料更改"""
    info = request.session["info"]

    row_info = models.EmpInfo.objects.filter(id=info['id']).first()
    if request.method == "GET":
        # 根据ID获取原始数据
        form = EmpModelForm_personal(instance=row_info)
        return render(request, 'personal_data_edit.html', {'form': form})

    # 将用户新提交的数据更新到该行
    form = EmpModelForm_personal(data=request.POST, instance=row_info)
    if form.is_valid():
        form.save()
        return redirect('/index/')

    return render(request, 'personal_data_edit.html', {'form': form})


def personal_edit_all(request):
    """用户个人资料更改，包括账号和密码"""
    info = request.session["info"]

    row_info = models.EmpInfo.objects.filter(id=info['id']).first()
    if request.method == "GET":
        # 根据ID获取原始数据
        form = EmpModelForm_personal_account(instance=row_info)
        return render(request, 'personal_all.html', {'form': form})

    # 将用户新提交的数据更新到该行
    form = EmpModelForm_personal_account(data=request.POST, instance=row_info)
    if form.is_valid():
        form.save()
        return redirect('/index/')

    return render(request, 'personal_all.html', {'form': form})
