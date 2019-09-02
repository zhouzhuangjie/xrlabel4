#如果医生打开了界面,展示了又没有提交,手动修改为未展示
import os

def main():
  from xray import models
  from django.contrib.auth.models import User
  from django.db.models import Count

  query=models.XrayDiagnose.objects.filter(status=2).values_list('user').annotate(c=Count('user'))
  str=''
  for i in query:
    username=User.objects.get(id=i[0]).username
    print('%s 医生已成功标记%s个'%(username,i[1]))
    str+='%s:%s\n'%(username,i[1])

  return str



if __name__ == '__main__':
  import sys
  sys.path.insert(0,'/home/zzj/projects/xrlabel4/')
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xrlabel.settings')
  import django

  django.setup()
  main()



