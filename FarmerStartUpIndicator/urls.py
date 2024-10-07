"""
URL configuration for FarmerStartUpIndicator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from app1.views import account
from app1.views import index
from app1.views import charts
from app1.views import statistics
from app1.views import data
from app1.views import message
from app1.views import depart
# from app1.views import user
from app1.views import report


urlpatterns = [
    # path('admin/', admin.site.urls),

    # 用户登录管理
    path('login/', account.login),
    path('logout/', account.logout),
    path('personal_data_edit/', account.personal_data_edit),
    path('personal_data_edit/account/', account.personal_edit_all),

    # 首页 by sc
    path('index/', index.index),
    # path('index_normal/', index.index_normal),
    path('chart_1/', charts.chart_1),
    path('chart_2/', charts.chart_2),
    path('chart_3/', charts.chart_3),
    path('chart_4/', charts.chart_4),

    # 数据展示(未完成)
    path('static/', statistics.static),

    # 信息录入 by sc gzj
    path('message/', message.message),
    # 单独的excel上传页面被隐藏 by gzj
    # path('upload_excel/', views.upload_excel),

    # 后台管理 by sc
    path('table/', data.table),
    path('table/<int:nid>/<str:filt_string>/edit/', data.table_edit),
    path('table/<int:nid>/<str:filt_string>/delete/', data.table_delete),
    path('table/export/', data.export_to_excel),

    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/<str:title>/<str:filt_string>/', depart.depart_delete),

    path('emp/add/', depart.emp_add),
    path('emp/delete/<int:nid>/<str:filt_string>/', depart.emp_delete),
    path('emp/edit/<int:nid>/<str:filt_string>/', depart.emp_edit),
    path('emp/reset/<int:nid>/<str:filt_string>/', depart.emp_reset),

    # path('user/list/', user.user_list),

    # 调研报告
    path('report/list/', report.report_list),
    path('report/my_report_list/', report.my_report_list),

]
