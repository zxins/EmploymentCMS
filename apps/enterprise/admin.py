from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'title', 'salary', 'education', 'work_area',  'detail_short']
    search_fields = ['company_name', 'title', 'detail']
    ordering = ('id',)

    # 自定义按钮(动作/操作)
    actions = ['edu', 'area', 'sal']

    def edu(self, request, queryset):
        """ 学历分分布 """
        pass

    edu.short_description = '学历分布'
    edu.action_type = 1
    edu.action_url = '/edu_als/'

    # analysis.action_url = 'https://jobs.51job.com/beijing/125472717.html?s=01&t=0'

    def area(self, request, queryset):
        """ 学历分分布 """
        pass

    area.short_description = '工作区域'
    area.action_type = 1
    area.action_url = '/area_als/'

    def sal(self, request, queryset):
        """ 学历分分布 """
        pass

    sal.short_description = '薪资情况'
    sal.action_type = 1
    sal.action_url = '/salary_als/'

    def get_actions(self, request):
        """ 返回一个字典, 内容为这个ModelAdmin的所有'动作'的名称映射 """

        # 对企业用户隐藏岗位分析按钮
        actions = super(JobsAdmin, self).get_actions(request)
        if request.user.user_type == 'enterprise':
            actions.pop('edu')
            actions.pop('area')
            actions.pop('sal')
        return actions

    def get_queryset(self, request):
        """ 返回可编辑的所有模型实例的查询集 """

        # 企业用户只允许查看自己发布的岗位信息
        qs = super(JobsAdmin, self).get_queryset(request)
        user = request.user
        if user.user_type == 'enterprise':
            qs = qs.filter(company_name=user.username)
            self.search_fields = ['title']
        return qs

    def get_form(self, request, obj=None, change=False, **kwargs):
        """ 返回添加页面和修改页面的表单类 """
        self.exclude = ['company_size',]

        # 非管理员用户隐藏部分字段
        if not request.user.is_superuser:
            # 在表单中去除company字段
            self.exclude.append('company_name')
        return super(JobsAdmin, self).get_form(request, obj, change, **kwargs)

    def save_model(self, request, obj, form, change):
        """ 给定一个模型实例，保存到数据库中 """

        # 非管理员用户只能为自己添加岗位信息
        if not request.user.is_superuser:
            obj.company_name = request.user.username
        super(JobsAdmin, self).save_model(request, obj, form, change)


@admin.register(Enterprises)
class EnterprisesAdmin(admin.ModelAdmin):
    list_display = ['user', 'address']
