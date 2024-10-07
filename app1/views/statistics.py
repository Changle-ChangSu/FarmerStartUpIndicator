# 开发者：苏畅
# 2023/5/15 0:19 于上海财经大学

from django.shortcuts import render


# 数据展示
def static(request):
    return render(request, 'static.html')
