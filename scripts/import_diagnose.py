import os

import pandas as pd


def main(path):
  from xray import models
  data = pd.read_csv(path)
  image_label = data.loc[0:, [data.columns[0], data.columns[1], data.columns[2]]]
  # image_label = data.loc[0:, [data.columns[0], data.columns[3]]]
  j=0
  for i in image_label.values:
    imagepath,p_dx,n_dx=i
    models.XrayDiagnose.objects.create(
      imagepath=imagepath,
      raw_p_dx=p_dx,
      raw_n_dx=n_dx,
    )
    j+=1
  print("从%s 文件中导入%s 个数据"%(path.rsplit('/',1)[-1],j))



if __name__ == '__main__':
  import sys

  sys.path.insert(0, '/home/zzj/projects/xrlabel4/')
  # sys.path.insert(0, '/Users/zhouzhuangjie/Desktop/xrlabel4')
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xrlabel.settings')
  import django

  django.setup()

  # path='/Users/zhouzhuangjie/PycharmProject/xrlabel/datas/test_pred_df.csv'
  path = '/Users/zhouzhuangjie/Desktop/康睿文件/pn_nod_img_df2(1).csv'
  main(path)
