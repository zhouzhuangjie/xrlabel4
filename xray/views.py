# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

from django.conf import settings
from django.db import transaction
from django.db.transaction import savepoint, savepoint_commit, savepoint_rollback
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from xray import models
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.db.models import Count
import json
import traceback
import numpy as np


# Create your views here.
def login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      auth_login(request, user)
      return HttpResponseRedirect('/xr/main')
    else:
      data = {'message': '登录失败，用户名或密码错误'}
      return render(request, 'login.html', data)
  elif request.method == 'GET':
    return render(request, 'login.html')


def logout(request):
  auth_logout(request)
  return render(request, 'login.html')


@login_required(login_url='/xr/login')
@transaction.atomic
def main(request):
  try:

    pageNum = int(request.GET.get('pageNum', '1'))
    pageSize = int(request.GET.get('pageSize', '8'))
    query = models.XrayDiagnose.objects.filter(status=0)
    obj_list = query[(pageNum - 1) * pageSize:pageNum * pageSize]
    for obj in obj_list:
      obj.status = 1
      obj.save()
    return render(request, 'label.html', {"images": obj_list})
  except Exception as e:
    print(e)
    return HttpResponse('请稍等,请重新刷新')


@login_required(login_url='/xr/login')
def diagnose(request):
  req = {}
  try:
    req = json.loads(request.body.decode())
  except Exception as e:
    traceback.print_exc()
    pass

  ids = req.get('ids', [])
  p_values = req.get('p_values', [])
  n_values = req.get('n_values', [])
  for idx, p_value,n_value in zip(ids, p_values,n_values):
    try:
      qd = models.XrayDiagnose.objects.get(id=int(idx))
    except models.XrayDiagnose.DoesNotExist:
      print("没有该 id 的xray")
      continue
    qd.status=2
    qd.user=request.user
    qd.p_dx=int(p_value)
    qd.n_dx=int(n_value)
    qd.save()
  return JsonResponse({"success": True})


  # try:
  #   for idx, value in zip(ids, values):
  #     xray = models.QualityDiagnose.objects.get(id=int(idx))
  #     if xray.dr_dx.all():
  #       continue
  #     if idx in noClears:
  #       xray.is_clear = False
  #     dr_dx_list = [models.DiagnoseParam.objects.get(id=int(i)) for i in value]
  #     no_find = models.DiagnoseParam.objects.get(name='No Finding')
  #
  #
  #     if no_find in dr_dx_list:
  #       xray.dr_dx.add(no_find)
  #     else:
  #       if idx in others:
  #         dp = models.DiagnoseParam.objects.create(name='other-' + xray.imagepath + "-" + str(time.time()),
  #                                                  value=others[idx], status=1)
  #         xray.dr_dx.add(dp)
  #       for dr_dx in dr_dx_list:
  #         xray.dr_dx.add(dr_dx)
  #     xray.user = request.user
  #     xray.status = 2
  #     xray.save()
  #
  # except Exception as e:
  #   savepoint_rollback(point)
  #   return JsonResponse({"success": False})
  # else:
  #   savepoint_commit(point)
  #   return JsonResponse({"success": True})


@login_required(login_url='/xr/login')
def task(request):
  labeled = models.XrayDiagnose.objects.filter(user=request.user).filter(status=2).count()
  total = models.XrayDiagnose.objects.filter(status=0).count()
  return JsonResponse({"success": True, "count": labeled, "total": total})


@login_required(login_url='/xr/login')
def imageview(request,image_path):
  from xrlabel import img_dic
  import cv2
  image = cv2.imencode('.jpg', img_dic[image_path])[1]
  img_bin = image.tobytes()
  return HttpResponse(img_bin,content_type='image/png')


def upload(request):
  if request.method == "POST":
    file = request.FILES.get("file", None)
    if not file:
      return HttpResponse('请上传文件')
    filename=file.name
    if not filename.endswith('.csv'):
      return HttpResponse('请上传csv文件')
    path=os.path.join(settings.BASE_DIR,'datas',filename)
    with open(path,'wb') as f:
      for chunk in file.chunks():  # 分块写入文件
        f.write(chunk)
    from scripts import import_diagnose
    try:
      import_diagnose.main(path)
    except Exception as e:
      print(e)
      return HttpResponse('导入数据库失败')

    return redirect('/xr/main')

def download(request):
  from scripts import export_datas
  data=export_datas.main()
  data=json.dumps(data).encode()
  filename='xray_dr_diagnose-%s.json'%(time.strftime('%Y-%m-%d'))
  response = HttpResponse(data)
  response['Content-Type']='application/octet-stream'
  response['Content-Disposition']='attachment;filename="%s"'%filename
  return response


def reset(request):
  from scripts import update_status
  update_status.main()
  return redirect('/xr/main')


def count_dr(request):
  from scripts import count_dr_diagnose
  data=count_dr_diagnose.main()
  return HttpResponse(data)
