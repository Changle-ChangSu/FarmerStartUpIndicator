# 开发者：苏畅
# 2023/5/8 16:51 于上海财经大学
from app1 import models
from django.db.models import Q


class Search(object):
    def __init__(self, request,
                 depart_param='depart', name_param='name', tel_param='tel', email_param='email', position_param='position',):
        # 获取GET请求中的四个筛选条件
        depart = request.GET.get(depart_param, '')
        name = request.GET.get(name_param, '')
        tel = request.GET.get(tel_param, '')
        email = request.GET.get(email_param, '')
        position = request.GET.get(position_param, '')

        self.depart = depart
        self.name = name
        self.tel = tel
        self.email = email
        self.position = position

    def after_search(self):
        conditions_dict = {}
        if self.depart == "无筛选" or not self.depart:
            pass
        else:
            id = models.Department.objects.filter(title=self.depart).first()
            conditions_dict['department_id__exact'] = id

        if self.name:
            conditions_dict['name__contains'] = self.name

        if self.tel:
            conditions_dict['tel__contains'] = self.tel

        if self.email:
            conditions_dict['email__contains'] = self.email

        if self.position:
            conditions_dict['position__contains'] = self.position

        # 根据条件查询用户,默认没有查询条件,展示所有的数据
        queryset = models.EmpInfo.objects.filter(**conditions_dict)

        # 回显列表
        filt = [self.depart, self.name, self.tel, self.email, self.position]
        filt_string = "&depart={}&name={}&tel={}&email={}&position={}"\
            .format(self.depart, self.name, self.tel, self.email, self.position)
        return queryset, filt, filt_string
