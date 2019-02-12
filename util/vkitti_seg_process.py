import os
import cv2 as cv
import numpy as np
import imghdr
from PIL import Image

def is_image(file_name):
    """
    To check if a file is an image

    Parameters
    ----------
    file_name: absolute path of the file

    Returns
    -------
    Boolean
        True: if the file is an image
        False: if the file is not an image

    """
    try:
        x = imghdr.what(file_name)
        if x == None:
            try:
                im = Image.open(file_name)
            except IOError:
                return False

        return True
    except IOError:
        return False

vkitti_to_kitti_dict = {"Terrain": "terrain", "Sky": "sky", "Tree": "vegetation",
                        "Vegetation": "vegetation", "Building": "building",
                        "Road": "road", "GuardRail": "guard rail", "TrafficSign": "traffic sign",
                        "TrafficLight": "traffic light", "Pole": "pole", "Misc": "misc", "Truck": "truck",
                        "Van": "caravan", "Car": "car"}

vkitti_class_list = ["terrain", "sky", "vegetation", "building", "road", "guard rail", "traffic sign", "traffic light",
                     "pole", "misc", "truck", "caravan", "car"]

vkitti_class_dic = {"terrain": 0, "sky": 1, "vegetation": 2, "building": 3,
                        "road": 4, "guard rail": 5, "traffic sign": 6,
                        "traffic light": 7, "pole": 8, "misc": 9, "truck": 10,
                        "caravan": 11, "car": 12}

indir = "../datasets/vkitti_semantic_raw_dirs.txt"

dirList = []

with open(indir, 'r') as input:
    for line in input:
        if line.strip():
            dirList.append(os.path.join(os.getcwd(), line.strip()))

for dir in dirList:
    idx = dir[-10: -6]
    print(idx)
    outdir = "../datasets/vkitti/vkitti_semantic_processed/" + idx
    encoding_file = "../datasets/vkitti/vkitti_1.3.1_scenegt/" + idx + "_clone_scenegt_rgb_encoding.txt"
    color_dict = []
    colors = []
    with open(encoding_file, 'r') as input:
        count = 0
        for line in input:
            if count == 0:
                count += 1
                continue
            if line.strip():
                strings = line.strip().split()
                print(strings)
                num = int(strings[1]) * 256 * 256 + int(strings[2]) * 256 + int(strings[3])
                colors.append(np.array([int(strings[3]), int(strings[2]), int(strings[1])]))
                if strings[0] in vkitti_to_kitti_dict:
                    color_dict.append(vkitti_class_dic[vkitti_to_kitti_dict[strings[0]]])
                else:
                    color_dict.append(vkitti_class_dic[vkitti_to_kitti_dict[strings[0][:3]]])
    if not os.access(outdir, os.F_OK):
        os.mkdir(outdir)
    fileList = os.listdir(dir)
    for file in fileList:
        print(file)
        if is_image(os.path.join(dir, file)):
            current_img = cv.imread(os.path.join(dir, file))
            label_seg = np.zeros((current_img.shape[:2]), dtype=np.int)
            for i in range(len(colors)):
                label_seg[(current_img==colors[i]).all(axis=2)] = color_dict[i]
            cv.imwrite(os.path.join(outdir, file), label_seg)



