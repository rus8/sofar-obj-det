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
gt_path = "/Users/luigi/Desktop/MOD17/MOT17Det/train/MOT17-02/gt/gt.txt"

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

    """
    gt = pd.read_csv(gt_path, header=None ).values
    gt_sorted = np.sort(gt, axis=0)

    data = dict()
    pedestrians = 0
    tot_pictures = 600
    for row in gt_sorted:
        print(row)
        break