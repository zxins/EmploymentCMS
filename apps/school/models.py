from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Students(models.Model):
    """ 学生 """

    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, verbose_name="姓名",
                                limit_choices_to={'user_type': 'student'}, help_text="选择/添加用户类型为'student'的账户")
    gender = models.CharField(max_length=10, choices=(("man", "男"), ("female", "女")), default="man", verbose_name="性别")
    major = models.CharField(max_length=30, default="软件工程", verbose_name="专业")
    grade = models.CharField(max_length=10, default="2016", verbose_name="年级")
    class_name = models.CharField(max_length=10, default="1", verbose_name="班级")

    class Meta:
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class Teachers(models.Model):
    """ 教师 """

    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, verbose_name="姓名",
                                limit_choices_to={'user_type': 'teacher'}, help_text="选择/添加用户类型为'teacher'的账户")
    gender = models.CharField(max_length=10, choices=(("man", "男"), ("female", "女")), default="man", verbose_name="性别")
    major = models.CharField(max_length=30, default="软件工程", verbose_name="授课专业")

    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
