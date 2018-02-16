''' Create random list of images

Script randomly selects desired number of images from dataset
and put their paths line by line in "train-list.txt". Such
file is required by original "darknet" framework.
'''

import glob
import os
import random
import shutil

# Number of images to list
train_num = 1000

# Path to dataset images folder
data_path = '/home/rr/Desktop/Caltech_ped_det/frames/'
labels_path = '/home/rr/Desktop/Caltech_ped_det/labels/'

part_data_path = '/home/rr/Desktop/Caltech_ped_det/part/frames/'
part_labels_path = '/home/rr/Desktop/Caltech_ped_det/part/labels/'

if not os.path.exists(part_data_path):
    os.makedirs(part_data_path)

if not os.path.exists(part_labels_path):
    os.mkdir(part_labels_path)


images = glob.glob(data_path+'*.jpg')
random.shuffle(images)

if train_num > len(images):
    train_num = len(images)

for i in range(train_num):
    name = (images[i].split('/')[-1]).split('.')[0]
    shutil.copyfile(images[i], part_data_path+name+'.jpg')
    shutil.copyfile(labels_path+name+'.txt', part_labels_path+name+'.txt')
