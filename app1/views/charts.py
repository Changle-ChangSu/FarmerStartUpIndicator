# 开发者：苏畅
# 2023/5/15 0:17 于上海财经大学


from app1.utils.table_search import Search
from django.db.models import Count, Case, When, Value, CharField  # 用来执行代码
from django.http import JsonResponse
from django.db.models.functions import ExtractYear


# chart1
def chart_1(request):
    """构造第一张图：饼状图"""
    queryset, filt, _ = Search(request).after_search()

    # 范围条件
    income_ranges = [
        (0, 0.5),
        (0.5, 1),
        (1, 2),
        (2, 5),
        (5, 10),
        (10, 20),
        (20, 10000)
    ]

    # 构建 Case-When 语句
    case_conditions = [
        When(income__range=(start, end), then=Value(range_label))
        for start, end in income_ranges
        for range_label in [f'{start}万~{end}万']
    ]

    result = queryset.annotate(
        income_range=Case(*case_conditions, default=None, output_field=CharField())
    ).values('income_range').annotate(count=Count('id')).order_by('income_range')

    result = [{'value': item['count'], 'name': item['income_range']} for item in list(result)]
    for item in result:
        if item['name'] == '20万~10000万':
            item['name'] = "20万以上"
        if item['name'] == '0万~0.5万':
            item['name'] = "5千以下"
        if item['name'] == '0.5万~1万':
            item['name'] = "5千~1万"

    legend = [item['name'] for item in result]
    res = {
        'status': True,
        'legend': legend,
        'db_data_list': result
    }
    return JsonResponse(res)


def chart_2(request):
    """构造第二张图表：创业人数与时间折线图"""
    # 查询出数据，准备可视化
    queryset, filt, _ = Search(request).after_search()

    # 统计符合条件的条目个数
    result = (queryset.filter(entrepre=1).annotate(year=ExtractYear('recptime')).values('year')
              .annotate(count=Count('id')).order_by('year'))
    # print(result)

    data = [item['count'] for item in list(result)]
    # print(data)

    legend = ['创业人数']
    x_axis = ['2017', '2018', '2019', '2020', '2021', '2022', '2023']

    res = {
        "status": True,
        'legend': legend,
        'x_axis': x_axis,
        'data': data
    }
    return JsonResponse(res)


def chart_3(request):
    """构造第三张图表：横向堆叠条形图"""
    # 查询出数据，准备可视化
    queryset, filt, _ = Search(request).after_search()

    # 按照 hmnCapital 的范围进行分类，统计每个范围内的条目数和 entrepre=1 的条目数

    hmnCapital_ranges = [
        (0, 5),
        (5, 10),
        (10, 15),
        (15, 20),
    ]

    case_conditions = [
        When(hmnCapital__range=(start, end), then=Value(range_label))
        for start, end in hmnCapital_ranges
        for range_label in [f'{start}~{end}年']
    ]

    result = queryset.annotate(
        hmnCapital_range=Case(*case_conditions, default=None, output_field=CharField()),
        count=Count('id'),
    ).values('hmnCapital_range').annotate(count=Count('id')).order_by('hmnCapital_range')

    entrepre_values = [0, 1]
    outcome = {}

    for entrepre in entrepre_values:
        # 筛选满足条件的数据，并按"entrepre"进行分组统计
        qs = result.filter(entrepre=entrepre)
        outcome[entrepre] = list(qs)

    # 输出统计结果
    # print(result)
    # print(outcome)

    data_1 = [item['count'] for item in outcome[0]]
    data_2 = [item['count'] for item in outcome[1]]
    print(data_1, data_2)

    legend = ["未创业", "创业"]
    y_axis = [item['hmnCapital_range'] for item in outcome[0]]

    series_list = [
        {
            'name': "未创业",
            'type': 'bar',
            'stack': '总量',
            'itemStyle': {'normal': {'label': {'show': False, 'position': 'insideRight'}}},
            'data': data_1,
        },
        {
            'name': "创业",
            'type': 'bar',
            'stack': '总量',
            'itemStyle': {'normal': {'label': {'show': False, 'position': 'insideRight'}}},
            'data': data_2,
        }
    ]

    res = {
        "status": True,
        'legend': legend,
        'y_axis': y_axis,
        'series_list': series_list
    }
    return JsonResponse(res)


# chart4
def chart_4(request):
    """构造第四张图表：纵向柱状图"""
    # 查询出数据，准备可视化
    queryset, filt, _ = Search(request).after_search()

    # 统计符合条件的条目个数
    # famtype_count_data = queryset.values('famtype').annotate(count=Count('famtype')).order_by('famtype')
    famtype_values = [0, 1, 2]
    entrepre_values = [0, 1]
    result = {}

    for famtype in famtype_values:
        # 筛选满足条件的数据，并按"famtype"进行分组统计
        famtype_count_data = queryset.filter(entrepre__in=entrepre_values, famtype=famtype).values('entrepre').annotate(
            count=Count('id')).order_by('entrepre')

        # 将统计结果存储到字典中
        result[famtype] = list(famtype_count_data.values('entrepre', 'count'))

    # print(result)
    data_1 = [item['count'] for item in result[0]]
    data_2 = [item['count'] for item in result[1]]
    data_3 = [item['count'] for item in result[2]]

    legend = ["普通家庭", "人力残缺家庭", "精英家庭"]

    series_list = [
        {
            'name': "普通家庭",
            'type': 'bar',
            'data': data_1,
        },
        {
            'name': "人力残缺家庭",
            'type': 'bar',
            'data': data_2,
        },
        {
            'name': "精英家庭",
            'type': 'bar',
            'data': data_3,
        }
    ]

    x_axis = ["未创业", "创业"]

    res = {
        "status": True,
        'legend': legend,
        'x_axis': x_axis,
        'series_list': series_list
    }
    return JsonResponse(res)
