# 开发者：苏畅
# 2023/5/15 0:19 于上海财经大学

import pandas as pd
# import tempfile
from django.shortcuts import render, redirect, HttpResponse
from app1 import models
from app1.utils.ModelForms import MessageModelForm
from app1.utils.pagination import Pagination
from app1.utils.table_search import Search


# 数据管理主页
def table(request):
    # 调用类
    queryset, filt, filt_string = Search(request).after_search()
    page_object = Pagination(request, queryset, filt_string)

    global gb_queryset
    gb_queryset = queryset

    context = {
        'queryset': page_object.page_queryset,  # 控制显示分完页的数据
        'filt': filt,  # 控制搜索条件回显
        'page_string': page_object.html(),  # 控制页码控件
        'page_size': page_object.page_size,  # 控制页面数据显示数量
        'total_page_count': page_object.total_page_count,  # 控制跳转输入框合法性
        'page': page_object.page,  # 控制执行删除操作后仍能返回到正确的页码上
        'div': page_object.div,  # 控制执行删除操作后仍能返回到正确的页码上
        'filt_string': filt_string,
    }
    # print(filt_string)
    return render(request, 'data_list.html', context)


# 数据管理：编辑单个数据
def table_edit(request, nid, filt_string):
    page_now = request.GET.get('page')
    div = request.GET.get('div')
    page_size = request.GET.get('page_size')

    if div == '1' and page_now > '1':
        page_now = int(page_now) - 1

    row_info = models.ThousandVillageSurvey.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID获取原始数据
        form = MessageModelForm(instance=row_info)
        return render(request, 'data_edit.html', {'form': form, 'nid': nid})

    # 将用户新提交的数据更新到该行
    form = MessageModelForm(data=request.POST, instance=row_info)
    if form.is_valid():
        form.save()

        return redirect('/table/?page={}&page_size={}{}'.format(page_now, page_size, filt_string))

    return render(request, 'data_edit.html', {'form': form})


# 数据管理：删除单个数据
def table_delete(request, nid, filt_string):
    models.ThousandVillageSurvey.objects.filter(id=nid).delete()

    page = request.GET.get('page')
    div = request.GET.get('div')
    page_size = request.GET.get('page_size')

    if div == '1' and page > '1':
        page = int(page) - 1

    return redirect('/table/?page={}&page_size={}{}'.format(page, page_size, filt_string))


def export_to_excel(request):
    # 从数据库中获取数据，这里以获取模型对象为例
    queryset = gb_queryset

    # 创建一个DataFrame对象，用于存储数据
    df = pd.DataFrame(list(queryset.values()))

    # 创建Excel写入器
    writer = pd.ExcelWriter('exported_data.xlsx', engine='xlsxwriter')

    # 将DataFrame写入Excel文件中的工作表
    df.to_excel(writer, index=False)

    # 创建Excel写入器
    # with tempfile.NamedTemporaryFile(delete=False) as tmp:
    filename = "导出数据"

    # 使用pandas的ExcelWriter对象进行写入
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    # 构造HTTP响应，将导出的Excel文件发送给用户
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename='+filename+'.xlsx'

    # 将Excel文件内容写入响应
    with open(filename, 'rb') as file:
        response.write(file.read())

    return response
