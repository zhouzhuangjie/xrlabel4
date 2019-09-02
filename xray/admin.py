# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from xray import models


# Register your models here.

class DiagnoseParamAdmin(admin.ModelAdmin):
  list_display = '__all__'


admin.site.register(models.XrayDiagnose)
