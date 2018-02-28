""" Evaluation of Kitti dataset

This script analyses labels, selects proper bounding boxes,
and saves them in special format using json.

Python dictionary / json format:
{"file1_path": [[bb_1_tl_x bb_1_tl_y bb_1_br_x bb_1_br_y] ... [bb_i_tl_x bb_i_tl_y bb_i_br_x bb_i_br_y]],
 "file2_path": ... }
"""
import glob
import json
import os

# Change this with the path of labels folder
path = "/Users/luigi/Desktop/Kaist/annotations"

def file_len(fo):
    """ Number of lines per file

    This function is supposed to evaluate how many lines are in the file
    """
    with open(fo) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__== "__main__":

    filePaths = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.')]
        for name in files:
            filePaths.append(os.path.join(root, name))
    data = dict()
    pedestrians = 0
    ped_pictures = 0
    tot_pictures = 0
    for current_file in filePaths:
        tot_pictures += 1
        # count number of lines in the file
        lines = file_len(current_file)
        fo = open(current_file, "r")
        bboxes = []

        print("Analyzing file: " + current_file)
        for x in range(lines):
            """Check pedestrian values
            
            Split the line every time I find a space and then analyze the values
            """
            line = fo.readline()
            words = line.split(" ")
            if words[0] == "person":
                pedestrians += 1
                coordinates = []
                coordinates.append(int(words[1]))
                coordinates.append(int(words[2]))
                coordinates.append(int(words[3]))
                coordinates.append(int(words[4]))
                bboxes.append(coordinates)

        # Close opened file
        fo.close()

        # Add things to the dictionary
        path_words = current_file.split("/")
        picture_code = path_words[-1].split(".")
        data[picture_code[0] + '.png'] = bboxes
        if bboxes:
            ped_pictures += 1

    print("\nTotal number of pictures: ", tot_pictures)
    print("Total number of pedestrians: ", pedestrians)
    print("Total number of pictures with pedestrians: ", ped_pictures)
    print("Total number of pictures without pedestrians: ", tot_pictures - ped_pictures)
    print("Average of pedestrians per picture with pedestrians: ", pedestrians / ped_pictures)
    print("Average of pedestrians per picture in general: ", pedestrians / tot_pictures)
