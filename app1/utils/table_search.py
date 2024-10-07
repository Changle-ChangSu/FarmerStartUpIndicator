# 开发者：苏畅
# 2023/5/8 16:51 于上海财经大学
from app1 import models
from django.db.models import Q


class Search(object):
    def __init__(self, request,
                 name_param='name', tel_param='tel', entrepre_param='entrepre', possibility_param='possibility',
                 famtype_param='famtype', income_param='income', start_date_param='start_date',
                 end_date_param='end_date', db1_param='db1', db2_param='db2', db3_param='db3'):
        # 获取GET请求中的四个筛选条件
        name = request.GET.get(name_param, '')
        tel = request.GET.get(tel_param, '')
        entrepre = request.GET.get(entrepre_param, '')
        possibility = request.GET.get(possibility_param, '')
        famtype = request.GET.get(famtype_param, '')
        income = request.GET.get(income_param, '')
        start_date = request.GET.get(start_date_param, '')
        end_date = request.GET.get(end_date_param, '')
        db1 = request.GET.get(db1_param, '')
        db2 = request.GET.get(db2_param, '')
        db3 = request.GET.get(db3_param, '')

        self.name = name
        self.tel = tel
        self.entrepre = entrepre
        self.possibility = possibility
        self.famtype = famtype
        self.income = income
        self.start_date = start_date
        self.end_date = end_date
        self.db1 = db1
        self.db2 = db2
        self.db3 = db3

    def after_search(self):
        conditions_dict = {}
        if self.name:
            conditions_dict['name__contains'] = self.name

        if self.tel:
            conditions_dict['tel__contains'] = self.tel

        if self.entrepre == "未创业":
            conditions_dict['entrepre__exact'] = 0
        elif self.entrepre == "创业":
            conditions_dict['entrepre__exact'] = 1

        if self.possibility == "低(0-0.2)":
            conditions_dict['possibility__lte'] = 0.2
        elif self.possibility == "中(0.2-0.8)":
            conditions_dict['possibility__lte'] = 0.8
            conditions_dict['possibility__gte'] = 0.2
        elif self.possibility == "高(0.8-1)":
            conditions_dict['possibility__gte'] = 0.8

        if self.famtype == "普通家庭":
            conditions_dict['famtype__exact'] = 0
        elif self.famtype == "人力残缺家庭":
            conditions_dict['famtype__exact'] = 1
        elif self.famtype == "精英家庭":
            conditions_dict['famtype__exact'] = 2

        if self.income == "0~5K":
            conditions_dict['income__gte'] = 0
            conditions_dict['income__lte'] = 0.5
        elif self.income == "5K~10K":
            conditions_dict['income__gte'] = 0.5
            conditions_dict['income__lte'] = 1
        elif self.income == "10K~20K":
            conditions_dict['income__gte'] = 1
            conditions_dict['income__lte'] = 2
        elif self.income == "20K~50K":
            conditions_dict['income__gte'] = 2
            conditions_dict['income__lte'] = 5
        elif self.income == "50K~100K":
            conditions_dict['income__gte'] = 5
            conditions_dict['income__lte'] = 10
        elif self.income == "100K~200K":
            conditions_dict['income__gte'] = 10
            conditions_dict['income__lte'] = 20
        elif self.income == "200K以上":
            conditions_dict['income__gte'] = 20

        if self.start_date:
            conditions_dict['recptime__gte'] = self.start_date

        if self.end_date:
            conditions_dict['recptime__lte'] = self.end_date

        q1 = Q(db=1)
        q2 = Q(db=0)
        q3 = Q(db=0)

        if self.db1 == 'on':
            q1 = Q(db=1)

        if self.db2 == 'on':
            q2 = Q(db=2)

        if self.db3 == 'on':
            q3 = Q(db=3)

        conditions_dict['db__exact'] = q1 | q2 | q3

        # 根据条件查询用户,默认没有查询条件,展示所有的数据
        queryset = models.ThousandVillageSurvey.objects.filter(**conditions_dict).order_by("-recptime")


        # 回显列表
        filt = [self.name, self.tel, self.entrepre, self.possibility, self.famtype, self.income, self.start_date,
                self.end_date, self.db1, self.db2, self.db3]
        filt_string = "&name={}&tel={}&entrepre={}&possibility={}&famtype={}&income={}&start_date={}&end_date={}&db1={}&db2={}&db3={}".format(
            self.name, self.tel, self.entrepre, self.possibility, self.famtype, self.income, self.start_date,
            self.end_date, self.db1, self.db2, self.db3)
        return queryset, filt, filt_string