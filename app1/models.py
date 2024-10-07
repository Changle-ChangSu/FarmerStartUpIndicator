from django.db import models
from django.core.validators import MinLengthValidator
from app1.utils.encrypt import md5


# Create your models here.

class ThousandVillageSurvey(models.Model):
    """千村调查数据集"""
    name = models.CharField(verbose_name='姓名', max_length=33)

    tel = models.CharField(verbose_name='联系电话', max_length=15)

    entrepre_choice = ((0, "未创业"), (1, "创业"))
    entrepre = models.IntegerField(verbose_name='是否创业', choices=entrepre_choice)

    # survival = models.BooleanField(verbose_name='是否是生存型创业', null=True)
    # opp = models.BooleanField(verbose_name='是否是机会型创业', null=True)
    entretype_choice = ((0, "生存型创业"), (1, "机会型创业"), (2, "其他创业"))  # 5.11苏畅改
    entretype = models.IntegerField(verbose_name='创业原因', null=True, blank=True, choices=entretype_choice)

    # elite = models.BooleanField(verbose_name='是否为精英家庭')
    # disinte = models.BooleanField(verbose_name='是否为人力残缺家庭')
    famtype_choice = ((0, "普通家庭"), (1, "人力残缺家庭"), (2, "精英家庭"))
    famtype = models.IntegerField(verbose_name="家庭类型", choices=famtype_choice)

    relation = models.FloatField(verbose_name='关系文化指数', max_length=8)

    gender_choice = ((1, "男"), (0, "女"))
    gender = models.IntegerField(verbose_name='性别', choices=gender_choice)

    age = models.IntegerField(verbose_name='年龄')

    marriage_choice = ((0, "未婚"), (1, "已婚"))
    marriage = models.IntegerField(verbose_name='婚姻状态', choices=marriage_choice)

    religion_choice = ((0, "无宗教信仰"), (1, "有宗教信仰"))
    religion = models.IntegerField(verbose_name='是否信教', choices=religion_choice)

    faminum = models.IntegerField(verbose_name='家庭成员数量')

    maler = models.IntegerField(verbose_name='家庭男性劳动力数量')

    farmland = models.FloatField(verbose_name='人均耕地面积(亩)', max_length=5)

    income = models.FloatField(verbose_name='家庭年收入水平(万元)', max_length=5)

    network = models.IntegerField(verbose_name='手机联系人数量')

    mkt = models.FloatField(verbose_name='当地市场化指数', max_length=4)

    exp_choice = ((1, "无期望"), (2, "低期望"), (3, "中期望"), (4, "高期望"))
    expectation = models.IntegerField(verbose_name='父母期望', choices=exp_choice)

    hc_choice = ((0, "无特殊技能"), (1, "有除务农外其他技能"))
    handicraft = models.IntegerField(verbose_name='是否有一技之长', choices=hc_choice)

    statu_choice = ((1, "无感"), (2, "低"), (3, "较低"), (4, "中"), (5, "较高"), (6, "高"))
    socistatu = models.IntegerField(verbose_name='家庭社会地位自评', choices=statu_choice)

    hmnCapital = models.IntegerField(verbose_name='受教育时长(年)')

    recptime = models.DateField(verbose_name='样本调查时间')

    recpplace = models.CharField(verbose_name='样本调查地点', max_length=150, default="(无数据)")

    remark = models.CharField(verbose_name='备注(选填)', null=True, max_length=500)

    possibility = models.FloatField(verbose_name='创业概率', null=True, max_length=4)  # 5.11 sc

    db_choice = ((1, '上海财经大学“千村调查”'), (2, "上海财经大学支教团调研数据"), (3, "上财马院乡村振兴数据库"))
    db = models.IntegerField(verbose_name='选择数据集', default=1)


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门名称", max_length=60, unique=True)

    def __str__(self):
        return self.title


class EmpInfo(models.Model):
    """职员用户表"""
    name = models.CharField(verbose_name="职员姓名", max_length=30)
    tel = models.CharField(verbose_name='联系电话', max_length=20)
    email = models.CharField(verbose_name="邮箱", max_length=30, unique=True)
    position = models.CharField(verbose_name="职级", max_length=30)
    # 级联删除
    department = models.ForeignKey(verbose_name="所属部门", to="Department", to_field="id", on_delete=models.CASCADE)

    password = models.CharField(verbose_name="密码", max_length=64, default=md5("123456"), validators=[MinLengthValidator(6)])

    usertype_choice = ((0, "超级用户"), (1, "普通用户"))
    usertype = models.IntegerField(verbose_name="用户类型", choices=usertype_choice, default=1)


# class UserInfo(models.Model):
#     """用户表"""
#     name = models.CharField(verbose_name="用户名", max_length=30)
#     password = models.CharField(verbose_name="密码", max_length=64)
#     tel = models.CharField(verbose_name='联系电话', max_length=20)
#     email = models.CharField(verbose_name="邮箱", max_length=30)
#
#     usertype_choice = ((0, "超级用户"), (1, "普通用户"))
#     usertype = models.IntegerField(verbose_name="用户类型", choices=usertype_choice)
#
#     register_time = models.DateTimeField(verbose_name="注册时间")
#     # 级联删除
#     department = models.ForeignKey(verbose_name="部门认证", to="Department", to_field="id", on_delete=models.CASCADE, null=True)
