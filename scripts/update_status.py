#如果医生打开了界面,展示了又没有提交,手动修改为未展示
import os

def main():
  from xray import models
  num = models.XrayDiagnose.objects.filter(status=1).update(status=0)
  print('已成功修改', num, '个')
if __name__ == '__main__':
  import sys
  sys.path.insert(0,'/home/zzj/projects/xrlabel4/')
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xrlabel.settings')
  import django

  django.setup()
  main()




