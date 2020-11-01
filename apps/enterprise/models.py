from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Enterprises(models.Model):
    """ 企业 """

    user = models.OneToOneField(User, default='', on_delete=models.CASCADE, verbose_name="名称",
                                limit_choices_to={'user_type': 'enterprise'})
    address = models.CharField(max_length=200, default='', verbose_name="地址")

    class Meta:
        verbose_name = "企业信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class Jobs(models.Model):
    """ 岗位信息 """

    # 这里不使用外键管理企业的原因是 可以发布未在此系统中注册的企业的岗位信息
    # 已注册的企业发布岗位信息，默认使用本企业名称，应不允许修改
    company = models.CharField(max_length=100, default='', verbose_name='企业名称',
                               help_text="管理员可以发布任意企业的岗位信息，即使未在此系统注册")
    position_name = models.CharField(max_length=50, verbose_name="职位名称")
    salary = models.CharField(max_length=50, verbose_name="薪资")
    detail = models.TextField(default='', verbose_name="职位详情")

    class Meta:
        verbose_name = "岗位信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.position_name

    def detail_short(self):
        count = 50
        if len(self.detail) > count:
            return self.detail[0:count] + '...'
        return self.detail

    detail_short.short_description = '详情'
    detail_short.allow_tags = True
