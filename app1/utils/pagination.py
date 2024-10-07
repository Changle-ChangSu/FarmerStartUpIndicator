# 开发者：苏畅
# 2023/5/8 11:45 于上海财经大学
"""
自定义分页组件
"""

from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, filt_string="", page_size_param='page_size', page_param='page', plus=5):
        page = request.GET.get(page_param, "1")
        page_size = request.GET.get(page_size_param, "10")
        self.filt_string = filt_string

        # 如果页码是数字,则转化为整型
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page

        # 如果每页显示数量是数字,则转化为整型
        if page_size.isdecimal():
            page_size = int(page_size)
        else:
            page_size = 10
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        self.total_count = total_count
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.div = div
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 显示当前页的前五页和后五页
        if self.total_page_count <= 2 * self.plus + 1:
            # 如果总页面的数量不够
            start_page = 1
            end_page = self.total_page_count
        else:
            # 如果总页面的数量够多
            # 当前页比较靠前,小于plus时
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页大于plus,或者当前页+plus>总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 分页按钮
        # 首页
        page_str_list = [
            str('<li><a href="?page={}&page_size={}' + self.filt_string + '">首页</a></li>').format(1, self.page_size)]

        # 上一页
        if self.page > 1:
            prev = str('<li><a href="?page={}&page_size={}' + self.filt_string + '">上一页</a></li>')\
                .format(self.page - 1, self.page_size)
        else:
            prev = str('<li><a href="?page={}&page_size={}' + self.filt_string + '">上一页</a></li>')\
                .format(1, self.page_size)

        page_str_list.append(prev)

        # 每个页面
        for i in range(start_page, end_page + 1):
            if i == self.page:
                ele = str(
                    '<li class="active"><a href="?page={}&page_size={}' + self.filt_string + '">{}</a></li>')\
                    .format(i, self.page_size, i)
            else:
                ele = str('<li><a href="?page={}&page_size={}' + self.filt_string + '">{}</a></li>')\
                    .format(i, self.page_size, i)

            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            nex = str('<li><a href="?page={}&page_size={}' + self.filt_string + '">下一页</a></li>')\
                .format(self.page + 1, self.page_size)
        else:
            nex = str('<li><a href="?page={}&page_size={}' + self.filt_string + '">下一页</a></li>')\
                .format(self.total_page_count, self.page_size)

        page_str_list.append(nex)

        # 尾页
        page_str_list.append(str('<li><a href="?page={}&page_size={}' + self.filt_string + '">尾页</a></li>')
                             .format(self.total_page_count, self.page_size))


        # 自定跳转页面
        # self_page_str = """
        #     <li>
        #         <form method="get" style="float: left; margin-left: -1px">
        #             <input type="text"
        #                    style="position: relative; float: left; display: inline-block; width: 88px; width: 80px; height: 31px; border-radius: 0;"
        #                    name="page" class="form-control" placeholder="跳转到...">
        #             <button style="margin-left: -2px; border-radius: 3px; color: rgb(51, 122, 183);" class="btn btn-default" type="submit">跳转</button>
        #         </form>
        #     </li>
        #     <li>
        #         <form method="get" style="float: left; margin-left: -1px">
        #             <input type="text"
        #                    style="position: relative; float: left; display: inline-block; width: 88px; width: 80px; height: 31px; border-radius: 0;"
        #                    name="page_size" class="form-control" placeholder="每页条数" value="{{ page_size }}">
        #             <button style="margin-left: -2px; border-radius: 3px; color: rgb(51, 122, 183);" class="btn btn-default" type="submit">执行</button>
        #         </form>
        #     </li>
        # """
        # self_page_str = """
        #     <li>
        #         <form method="get">
        #         <div class="input-group" style="width: 100px">
        #             <input type="text" name="page" class="form-control" placeholder="跳转到...">
        #             <span class="input-group-btn">
        #                 <button class="btn btn-default" type="button">跳转</button>
        #             </span>
        #         </div>
        #         </form>
        #     <li>
        # """

        # page_str_list.append(self_page_str)

        # 返回分页内容
        page_string = mark_safe("".join(page_str_list))
        return page_string
