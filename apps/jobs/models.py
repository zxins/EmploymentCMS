from django.db import models


# Create your models here.
class Job(models.Model):
    company = models.CharField(max_length=100, default='', verbose_name='企业名称')
    position_name = models.CharField(max_length=50, verbose_name="职位名称")
    salary = models.CharField(max_length=50, verbose_name="薪资")
    detail = models.TextField(default='', verbose_name="职位详情")

    class Meta:
        verbose_name = "招聘信息"
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