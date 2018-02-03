""" Evaluation of Kitti dataset

This script analyses labels, selects proper bounding boxes,
and saves them in special format using json.

Python dictionary / json format:
{"file1_path": [[bb_1_x bb_1_y bb_1_w bb_1_h] ... [bb_i_x bb_i_y bb_i_w bb_i_h]],
 "file2_path": ... }
"""
import glob
import json


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

    data = dict()

    for current_file in glob.glob('/Users/luigi/Desktop/label_2/*.txt'):

        # count number of lines in the file
        lines = file_len(current_file)
        fo = open(current_file, "r")
        for x in range(lines):
            """Check pedestrian values
            
            I split the line every time I find a space and the analyze the values
            """
            line = fo.readline()
            words = line.split(" ")
            if words[0]== "Pedestrian"
                coordinates[0] =
           # print("Read Line: ", line)

        # Close opend file
        fo.close()

    # write results in json file
    json.dump(data, open("/Users/luigi/Git/sofar-obstacle-detection/" + '/results.json', 'w'))
