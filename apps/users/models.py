from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', '学生'),
        ('teacher', '教师'),
        ('enterprise', '企业'),
        ('other', '其他')
    )
    is_staff = models.BooleanField(default=True, verbose_name="允许登录此系统")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="other", verbose_name="用户类型")

    class Meta:
        verbose_name = "账户信息"
        verbose_name_plural = verbose_name
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username
