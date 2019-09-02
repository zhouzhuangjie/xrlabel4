import json
import os
import time


def main():
  from xray import models
  query = models.XrayDiagnose.objects.filter(status=2)
  list = []
  id = 1
  for i in query:
    dict = {}
    dict['id'] = id
    dict['filename'] = i.imagepath
    dict['raw_Pneumonia']=i.raw_p_dx
    dict['raw_Nodule']=i.raw_n_dx
    dict['dr_Pneumonia']=i.p_dx
    dict['dr_Nodule']=i.n_dx
    # dict['check_user']=i.user.username
    list.append(dict)
    id += 1
  from django.conf import settings
  filename = 'xray_2labels-%s.json' % (time.strftime('%Y-%m-%d'))
  path = os.path.join(settings.BASE_DIR, 'datas', filename)
  with open(path, 'w') as f:
    json.dump(list, f, ensure_ascii=False)
  return list


if __name__ == '__main__':
  import sys

  sys.path.insert(0, '/home/zzj/projects/xrlabel4/')
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xrlabel.settings')
  import django

  django.setup()


  main()
