# 开发者：苏畅
# 2023/5/15 0:03 于上海财经大学

from django.shortcuts import render, redirect
from app1.utils.pagination import Pagination
from app1.utils.table_search import Search
from django.db.models import Count, Max  # 用来执行代码


# 首页
def index(request):
    queryset, filt, _ = Search(request).after_search()
    page_object = Pagination(request, queryset)

    # 在库样本数
    num_of_statistics = page_object.total_count
    # 创业人数
    entrepre_count = queryset.filter(entrepre=1).aggregate(Count('id'))['id__count']
    # 贫困样本数
    poor_count = queryset.filter(income__lte=0.5).aggregate(Count('id'))['id__count']
    # 富裕样本数
    rich_count = queryset.filter(income__gte=20).aggregate(Count('id'))['id__count']
    # 当前算法
    algorithm_name = "LR Alpha"
    # 数据截止至
    end_date = queryset.aggregate(Max('recptime'))['recptime__max']

    queryset_income = queryset.filter(entrepre=1).order_by("-income")[:5]
    names = [item.name for item in queryset_income]
    incomes = [item.income for item in queryset_income]
    # print(names, incomes)

    queryset_p = queryset.filter(entrepre=0).order_by("-possibility")[:5]
    names_p = [item.name for item in queryset_p]
    p = [round(item.possibility, 5) for item in queryset_p]

    context = {
        'num_of_statistics': num_of_statistics,
        'entrepre_count': entrepre_count,
        'poor_count': poor_count,
        'rich_count': rich_count,
        'algorithm_name': algorithm_name,
        'end_date': end_date,
        'names': names,
        'incomes': incomes,
        'names_p': names_p,
        'p': p
    }

    return render(request, 'index.html', context)

# def index_normal(request):

