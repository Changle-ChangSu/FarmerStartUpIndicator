# 开发者：苏畅
# 2023/6/15 15:40 于上海财经大学

from django.shortcuts import render, redirect
from app1 import models
from app1.utils.ModelForms import MessageModelForm
from app1.utils.pagination import Pagination
from app1.utils.table_search import Search


def user_list(request):
    return render(request, 'user_list.html')
