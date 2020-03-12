from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 用户表
class UserProfile(AbstractUser):
    """用户"""
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female","女")), default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 作品
class Works(models.Model):
    title = models.CharField(default="",max_length=60,varbose_name="作品名称")    # 名称
    describe = models.CharField(default="",max_length=200,varbose_name="作品描述")     # 描述
    image = models.ImageField(varbose_name="图片",null=True, blank=True)

    class Meta:
        verbose_name = "作品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
