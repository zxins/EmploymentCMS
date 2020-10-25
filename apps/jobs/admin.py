from django.contrib import admin
from .models import *

admin.site.site_title = "毕业生就业管理系统"
admin.site.site_header = "毕业生就业管理系统"

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['company', 'position_name', 'salary', 'detail_short']

    actions = ['custom_button']

    def custom_button(self, request, queryset):
        pass
    custom_button.short_description = '岗位分析'
    custom_button.action_type = 0
    custom_button.action_url = 'http://www.baidu.com'