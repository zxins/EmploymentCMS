from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = ['company', 'position_name', 'salary', 'detail_short']
    search_fields = ['company', 'position_name']

    # 自定义按钮(动作/操作)
    actions = ['analysis']

    def analysis(self, request, queryset):
        """ 岗位分析 """
        pass

    analysis.short_description = '岗位分析'
    analysis.action_type = 0
    analysis.action_url = 'http://www.baidu.com'

    def get_actions(self, request):
        """ 返回一个字典, 内容为这个ModelAdmin的所有'动作'的名称映射 """

        # 对企业用户隐藏岗位分析按钮
        actions = super(JobsAdmin, self).get_actions(request)
        if request.user.user_type == 'enterprise':
            actions.pop('analysis')
        return actions

    def get_queryset(self, request):
        """ 返回可编辑的所有模型实例的查询集 """

        # 企业用户只允许查看自己发布的岗位信息
        qs = super(JobsAdmin, self).get_queryset(request)
        user = request.user
        if user.user_type == 'enterprise':
            qs = qs.filter(company=user.username)
            self.search_fields = ['position_name']
        return qs

    def get_form(self, request, obj=None, change=False, **kwargs):
        """ 返回添加页面和修改页面的表单类 """

        # 非管理员用户隐藏部分字段
        if not request.user.is_superuser:
            # 在表单中去除company字段
            self.exclude = ('company',)
        return super(JobsAdmin, self).get_form(request, obj, change, **kwargs)

    def save_model(self, request, obj, form, change):
        """ 给定一个模型实例，保存到数据库中 """

        # 非管理员用户只能为自己添加岗位信息
        if not request.user.is_superuser:
            obj.company = request.user.username
        super(JobsAdmin, self).save_model(request, obj, form, change)


@admin.register(Enterprises)
class EnterprisesAdmin(admin.ModelAdmin):
    list_display = ['user', 'address']
