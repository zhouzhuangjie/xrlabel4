#生成总的img_dic
import pickle

img_dic={}
pickle_path_list=['/home/zzj/RawData/chexpert_img_dic.pkl','/home/zzj/RawData/chexray14_img_dic.pkl',
'/home/zzj/RawData/njxray_3channel_img_dic.pkl']
for pickle_path in pickle_path_list:
    f = open(pickle_path,'rb')
    img_dic_subset = pickle.load(f)
    f.close()
    for key in img_dic_subset.keys():
        image=img_dic_subset[key]
        img_dic[key]=image
