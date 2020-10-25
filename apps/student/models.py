from django.db import models


# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=30, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=(("man", "男"), ("female", "女")), default="man", verbose_name="性别")
    major = models.CharField(max_length=30, default="软件工程", verbose_name="专业")

    class Meta:
        verbose_name = "毕业生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
