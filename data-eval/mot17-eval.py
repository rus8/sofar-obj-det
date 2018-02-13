""" Evaluation of MOT17 dataset

This script analyses labels, selects proper bounding boxes,
and saves them in special format using json.

Python dictionary / json format:
{"file1_path": [[bb_1_tl_x bb_1_tl_y bb_w bb_1_h] ... [bb_i_tl_x bb_i_tl_y bb_i_w bb_i_h]],
 "file2_path": ... }
"""
import glob
import json
import numpy as np
import pandas as pd

# Change this with the path of labels folder
gt_path = "/Users/luigi/Desktop/MOD17/MOT17Det/train/MOT17-09/gt/gt.txt"

def file_len(fo):
    """ Number of lines per file
    This function is supposed to evaluate how many lines are in the file
    """
    with open(fo) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


if __name__ == "__main__":
    """Label files evaluation
    The main purpose of this script is to understand how many pictures contain pedestrians and compute an average of pedestrians per picture.
    After that, the number of pedestrians per pictures and relative bounding boxes is stored in a json file, following the "standard" used for also
    the other evaluation scripts.

    """
    gt = pd.read_csv(gt_path, header=None ).values
    #gt_sorted = np.sort(gt, axis=0, kind='mergesort')

    data = dict()
    pedestrians = 0
    tot_pictures = 0
    ped_pictures = 0

    # First of all remove every picture with people inside vehicles
    to_delete = []
    for row in gt:
        if row[7] == 2 and row[6] > 0:
            to_delete.append(row[0])
    for row in gt:
        if row[0] in to_delete:
            gt = np.delete(gt, (row), axis=0)

    for row in gt:
        if row[7] == 1 or row[7] == 7:
            if row[6] > 0:
                pedestrians += 1
                bboxes_list = []
                bbox = []
                bbox.append(row[2])
                bbox.append(row[3])
                bbox.append(row[4])
                bbox.append(row[5])
                bboxes_list.append(bbox)
                pic_id = str(int(row[0]))
                if pic_id + '.jpg' not in data:
                    data[pic_id+'.jpg'] = bboxes_list
                    ped_pictures += 1
                else:
                    data[pic_id+'.jpg'].append(bboxes_list)
    tot_pictures = len(data)

    # write results in json file
    json.dump(data, open("/Users/luigi/Git/sofar-obstacle-detection/" + '/mot17-label.json', 'w'))

    print("\nTotal number of pictures: ", tot_pictures)
    print("Total number of pedestrians: ", pedestrians)
    print("Total number of pictures with pedestrians: ", ped_pictures)
    print("Total number of pictures without pedestrians: ", tot_pictures - ped_pictures)
    print("Average of pedestrians per picture with pedestrians: ", pedestrians / ped_pictures)
    print("Average of pedestrians per picture in general: ", pedestrians / tot_pictures)
