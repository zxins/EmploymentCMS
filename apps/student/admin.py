from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'major']

    # 内部用来获取某个用户有权限访问的数据行
    def get_model_objs(self, request, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'change', 'delete']
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions],
                                    klass=klass, any_perm=True)