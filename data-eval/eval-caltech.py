""" Evaluation of Caltech Pedestrian dataset

This script analyses labels, selects proper bounding boxes,
and saves them in special format using json.

Python dictionary / json format:
{"file1_path": [[bb_1_tl_x bb_1_tl_y bb_1_br_x bb_1_br_y] ... [bb_i_tl_x bb_i_tl_y bb_i_br_x bb_i_br_y]],
 "file2_path": ... }
"""

import os
import glob
import json
from scipy.io import loadmat
from collections import defaultdict

data_path = '/home/rr/Desktop/Caltech-dataset'

pedestrians = 0
tot_pictures = 0
ped_pictures = 0
data = defaultdict(dict)
labels = dict()
for dname in sorted(glob.glob(data_path + '/annotations/set*')):
    set_name = os.path.basename(dname)
    data[set_name] = defaultdict(dict)
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
                    # datum = dict(zip(keys, [id, pos, occl, lock, posv]))
                    # datum['lbl'] = str(objLbl[datum['id']])
                    # datum['str'] = int(objStr[datum['id']])
                    # datum['end'] = int(objEnd[datum['id']])
                    # datum['hide'] = int(objHide[datum['id']])
                    # if datum['hide'] > 0:
                    #     print(set_name, video_name, frame_id, id, " : ", occl, datum['hide'])
                    # datum['init'] = int(objInit[datum['id']])
                    # data[set_name][video_name][
                    #     'frames'][frame_id].append(datum)
                    label = str(objLbl[id])

                    # Consider only pictures with persons presented separately or without people at all
                    if label == 'people' or label == 'person?':
                        bad_pic = True
                        bboxes = []
                        break
                    elif label == 'person':
                        coordinates = pos
                        coordinates[2] += coordinates[0]
                        coordinates[3] += coordinates[1]
                        bboxes.append(coordinates)
                        pic_obj += 1

            if not bad_pic:
                tot_pictures += 1
                if bboxes:
                    ped_pictures += 1
                n_obj += pic_obj
                labels[set_name+'/'+video_name+'.seq/'+str(frame_id)+'.jpg'] = bboxes
        print(dname, anno_fn, n_obj)
        pedestrians += n_obj

print('Number of objects:', pedestrians)
json.dump(labels, open(data_path + '/caltech-labels.json', 'w'))

print("\nTotal number of pictures: ", tot_pictures)
print("Total number of pedestrians: ", pedestrians)
print("Total number of pictures with pedestrians: ", ped_pictures)
print("Total number of pictures without pedestrians: ", tot_pictures - ped_pictures)
print("Average of pedestrians per picture with pedestrians: ", pedestrians/ped_pictures)
print("Average of pedestrians per picture in general: ", pedestrians / tot_pictures)
