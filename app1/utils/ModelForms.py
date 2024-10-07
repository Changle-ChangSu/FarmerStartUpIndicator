# 开发者：苏畅
# 2023/5/11 21:59 于上海财经大学
from django import forms
from app1 import models
from django.core.exceptions import ValidationError
from app1.utils.encrypt import md5


class MessageModelForm(forms.ModelForm):
    class Meta:
        model = models.ThousandVillageSurvey
        fields = [
            # 个人信息
            "name", "tel", "age", "hmnCapital", "network", "expectation", "gender", "marriage", "religion",
            "handicraft",
            # 家庭信息
            "faminum", "maler", "farmland", "income", "socistatu", "famtype",
            # 环境信息
            "relation", "mkt",
            # 反馈信息
            "entrepre", "entretype", "recpplace", "recptime", "remark"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "message_input"}


class EmpModelForm(forms.ModelForm):
    class Meta:
        model = models.EmpInfo
        fields = ["name", "tel", "email", "position", "department", "usertype"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "message_input"}


class EmpModelForm_personal(forms.ModelForm):
    class Meta:
        model = models.EmpInfo
        fields = ["name", "tel", "position", "department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "message_input"}


class EmpModelForm_personal_account(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.EmpInfo
        fields = ["name", "tel", "position", "department", "email", "password", "confirm_password"]
        labels = {
            "email": "账号（邮箱）",
            "password": "新密码",
            "confirm_password": "确认新密码",
        }
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if len(pwd) < 6 or len(pwd) > 64:
            raise ValidationError("密码长度至少6位，至多64位")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，保存到数据库就是什么
        return confirm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "message_input"}


class EmpModelForm_with_pwd(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.EmpInfo
        fields = ["name", "tel", "email", "position", "department", "password", "confirm_password", "usertype"]
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if len(pwd) < 6 or len(pwd) > 64:
            raise ValidationError("密码长度至少6位，至多64位")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，保存到数据库就是什么
        return confirm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # if name != "password":
            field.widget.attrs = {"class": "message_input"}
