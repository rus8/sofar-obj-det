""" Arranging of Caltech Pedestrian dataset

This script analyses labels, selects proper bounding boxes,
saves them in special YOLO format, and copies images giving
them same names as for label files.

It requires extracted images from videos to be stored in
"images" folder in dataset directory.

The result is folder "frames" and folder "labels" in
dataset directory.
"""

import os
import shutil
import glob
from scipy.io import loadmat
from collections import defaultdict

# Path to dataset folder which should contain "annotations" folder
# "images" folder.
data_path = '/home/rr/Desktop/Caltech_ped_det'

img_w = 640
img_h = 480

def create_label(name, bboxes):
    '''Saves bounding boxes for a single image in ".txt" file.

    :param name: Name for a label file.
    :param bboxes: List of bounding boxes of pedestrians.
    '''
    label_path = data_path + "/labels/" + name + ".txt"
    with open(label_path, 'w') as fp:
        for bbox in bboxes:
            str_x = str(float(bbox[0]) / img_w)
            str_y = str(float(bbox[1]) / img_h)
            str_w = str(float(bbox[2]) / img_w)
            str_h = str(float(bbox[3]) / img_h)
            str_line = '0 '+ str_x + ' ' + str_y + ' ' + str_w + ' ' + str_h + '\n'
            fp.write(str_line)
        fp.close()


def copy_img(name, set, vid, id):
    '''Copy image file from original direction to the folder common
    for all images, giving it name based on the set and video file
    from which it was cut.

    :param name: New name for image.
    :param set: Name of the set of videos.
    :param vid: Name of the video, from which the frame was cut.
    :param id: Image id.
    '''
    old_path = data_path + '/images/' + set + '/' + vid + '.seq/' + str(id) + '.jpg'
    new_path = data_path + '/frames/' + name + '.jpg'
    shutil.copyfile(old_path, new_path)

if not os.path.exists(data_path+'/images'):
    os.mkdir(data_path+'/images')

if not os.path.exists(data_path+'/labels'):
    os.mkdir(data_path+'/labels')

pedestrians = 0
tot_pictures = 0
ped_pictures = 0
data = defaultdict(dict)
labels = dict()  # Stores data to be saved as json file
for dname in sorted(glob.glob(data_path + '/annotations/set*')):
    set_name = os.path.basename(dname)
    data[set_name] = defaultdict(dict)
    # For each video in the set parse annotation file
    for anno_fn in sorted(glob.glob('{}/*.vbb'.format(dname))):

        vbb = loadmat(anno_fn)
        nFrame = int(vbb['A'][0][0][0][0][0])
        objLists = vbb['A'][0][0][1][0]
        maxObj = int(vbb['A'][0][0][2][0][0])
        objInit = vbb['A'][0][0][3][0]
        objLbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
        objStr = vbb['A'][0][0][5][0]
        objEnd = vbb['A'][0][0][6][0]
        objHide = vbb['A'][0][0][7][0]
        altered = int(vbb['A'][0][0][8][0][0])
        log = vbb['A'][0][0][9][0]
        logLen = int(vbb['A'][0][0][10][0][0])

        video_name = os.path.splitext(os.path.basename(anno_fn))[0]
        data[set_name][video_name]['nFrame'] = nFrame
        data[set_name][video_name]['maxObj'] = maxObj
        data[set_name][video_name]['log'] = log.tolist()
        data[set_name][video_name]['logLen'] = logLen
        data[set_name][video_name]['altered'] = altered
        data[set_name][video_name]['frames'] = defaultdict(list)

        n_obj = 0

        # For each frame in video add bboxes to the label's dictionary
        for frame_id, obj in enumerate(objLists):
            bboxes = []  # List for bounding boxes of persons
            pic_obj = 0  # Number of objects in image
            bad_pic = False  # Flag for pictures which contains "people" and "person?" classes
            if len(obj) > 0:
                for id, pos, occl, lock, posv in zip(
                        obj['id'][0], obj['pos'][0], obj['occl'][0],
                        obj['lock'][0], obj['posv'][0]):
                    keys = obj.dtype.names
                    id = int(id[0][0]) - 1  # MATLAB is 1-origin
                    pos = pos[0].tolist()
                    # if pos[3] > 15:
                    #     print(set_name, video_name, frame_id, id, " : ", pos)
                    occl = int(occl[0][0])
                    lock = int(lock[0][0])
                    posv = posv[0].tolist()
                    label = str(objLbl[id])

                    # Consider only pictures with persons presented separately or without people at all
                    if label == 'people' or label == 'person?':
                        bad_pic = True
                        bboxes = []
                        break
                    elif label == 'person':
                        bboxes.append(pos)
                        pic_obj += 1

            if not bad_pic:
                tot_pictures += 1
                if bboxes:
                    ped_pictures += 1
                n_obj += pic_obj
                # labels[set_name+'/'+video_name+'.seq/'+str(frame_id)+'.jpg'] = bboxes
                file_name = set_name + '-' + video_name + '-' + str(frame_id)
                create_label(file_name, bboxes)
                copy_img(file_name, set_name, video_name, frame_id)
                # labels[set_name + '-' + video_name + '-' + str(frame_id) + '.jpg'] = bboxes
        print(dname, anno_fn, n_obj)
        pedestrians += n_obj
