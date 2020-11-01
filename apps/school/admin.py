from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Teachers)
class TeachersAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'major']


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'major', 'grade', 'class_name']
