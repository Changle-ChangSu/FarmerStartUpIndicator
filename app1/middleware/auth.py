# 开发者：苏畅
# 2023/6/26 1:30 于上海财经大学

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    """判断登陆状态的中间件"""

    def process_request(self, request):
        # 0. 指定不需要登录就能访问的页面
        if request.path_info == "/login/":
            return

        # 1. 读取当前访问用户的session信息，如果能读到，说明已登录过
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2. 如果没有登陆过……
        return redirect('/login/')
