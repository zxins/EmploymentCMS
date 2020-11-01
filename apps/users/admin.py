from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *

# 全局设置，系统名称
admin.site.site_title = "管理系统"
admin.site.site_header = "管理系统"


# admin.site.unregister(Group)


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    # add_form_template = 'admin/auth/user/add_form.html'
    # change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'user_type')}),
        (_('Permissions'), {
            'fields': ('is_superuser', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )

    list_display = ('username', 'email', 'user_type')
    list_filter = ('user_type', 'groups')
    # search_fields = ('username', 'first_name', 'last_name', 'email')
    # ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_queryset(self, request):
        """ 利用查询钩子，动态的控制用户权限 """
        qs = super(UserProfileAdmin, self).get_queryset(request)
        user = request.user
        if user.user_type == 'teacher':
            qs = qs.filter(user_type='student')

            # 设置页面显示内容
            self.fieldsets = (
                (None, {'fields': ('username', 'password', 'email')}),
            )
            self.filter_horizontal = ()
            self.list_filter = ()
            self.search_fields = ('username', 'email')
        return qs
