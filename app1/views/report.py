# 开发者：苏畅
# 2023/6/26 23:18 于上海财经大学

from django.shortcuts import render, redirect


def report_list(request):
    """报告列表：可查看所有报告"""
    return render(request, 'report_list.html')


def my_report_list(request):
    """报告列表：只可查看本人的报告并进行管理"""
    return render(request, 'my_report_list.html')
