from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

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

    EDUCATION_CHOICES = (
        ("不限", "不限"),
        ("高中", "高中"),
        ("大专", "大专"),
        ("本科", "本科"),
        ("硕士", "硕士"),
        ("硕士", "博士"),
    )

    # 这里不使用外键管理企业的原因是 可以发布未在此系统中注册的企业的岗位信息
    # 已注册的企业发布岗位信息，默认使用本企业名称，应不允许修改
    company_name = models.CharField(max_length=100, default='', verbose_name='企业名称',
                                    help_text="管理员可以发布任意企业的岗位信息，即使未在此系统注册")
    title = models.CharField(max_length=50, default='', verbose_name="职位名称")
    education = models.CharField(max_length=10, default='', choices=EDUCATION_CHOICES, verbose_name="学历")
    min_salary = models.FloatField(max_length=50, default=0, validators=[MinValueValidator(0)], verbose_name="最小薪资",
                                   help_text="单位：K")
    max_salary = models.FloatField(max_length=50, default=0, validators=[MinValueValidator(0)], verbose_name="最小薪资",
                                   help_text="单位：K")
    work_area = models.CharField(max_length=50, default='北京', verbose_name="工作地点")
    detail = models.TextField(default='', verbose_name="职位详情")
    company_type = models.CharField(max_length=10, default='民营公司', verbose_name="企业类型")
    company_size = models.CharField(max_length=20, default='', verbose_name="企业大小")

    class Meta:
        verbose_name = "岗位信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def detail_short(self):
        count = 50
        if len(self.detail) > count:
            return self.detail[0:count] + '...'
        return self.detail

    detail_short.short_description = '详情'
    detail_short.allow_tags = True

    def salary(self):
        return '{:g}-{:g}K'.format(self.min_salary, self.max_salary)

    salary.short_description = "薪资范围"
    detail_short.allow_tags = True

    def clean(self):
        # 防止最大薪资小于最小薪资
        if self.max_salary < self.min_salary:
            raise ValidationError({'max_salary': "最大薪资应大于或等于最小薪资"})
