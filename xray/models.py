# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class DiagnoseParam(models.Model):
#   STATUS_CHOICE = (
#     (0, '14 类其一'),
#     (1, '其他分类'),
#   )
#   name = models.CharField(max_length=50, verbose_name='标签名字')
#   value = models.CharField(max_length=10, verbose_name='标签值')
#   status = models.IntegerField(default=0, choices=STATUS_CHOICE,verbose_name='可选状态')
#
#   def __str__(self):
#     return self.value


class XrayDiagnose(models.Model):
  TYPE_CHOICE = (
    (0, '无肺炎'),
    (1, '肺炎'),
    (2, '不确定')
  )
  TYPE2_CHOICE = (
    (0, '无肺结核'),
    (1, '肺结核'),
    (2, '不确定')
  )

  STATUS_CHOICE = (
    (0, '未标注'),
    (1, '已展示未标注'),
    (2, '已标注')
  )

  imagepath = models.CharField(db_index=True, max_length=200, verbose_name='图片路径')
  ai_p_dx = models.IntegerField(null=True, blank=True, choices=TYPE_CHOICE, verbose_name='AI肺炎标注')
  ai_n_dx = models.IntegerField(null=True, blank=True, choices=TYPE_CHOICE, verbose_name='AI肺结核标注')
  raw_p_dx = models.IntegerField(default=0, choices=TYPE_CHOICE, verbose_name='原始肺炎标注')
  raw_n_dx = models.IntegerField(default=0, choices=TYPE2_CHOICE, verbose_name='原始肺结核标注')
  p_dx = models.IntegerField(null=True, blank=True, choices=TYPE_CHOICE, verbose_name='医生肺炎标注')
  n_dx = models.IntegerField(null=True, blank=True, choices=TYPE2_CHOICE, verbose_name='医生肺结核标注')
  dxDate = models.DateTimeField(auto_now=True, verbose_name='标注日期')
  user = models.ForeignKey(User, related_name='xraw_set', null=True, blank=True, verbose_name='医生用户')
  status = models.IntegerField(default=0, choices=STATUS_CHOICE, verbose_name='是否标注')

  def __str__(self):
    return self.imagepath

  @property
  def dr_name(self):
    return self.user.username

# class XrayProbability(models.Model):
#   image = models.ForeignKey(FundusDiagnose, unique=True, related_name='probext', null=True, blank=True)
#   prob = models.CharField(max_length=100)
