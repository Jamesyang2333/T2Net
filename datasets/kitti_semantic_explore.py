import cv2 as cv
import numpy as np
from PIL import Image
# # seman = cv.imread("data_semantics/training/semantic/000000_10.png")
# # print(type(seman))
import scipy.misc as sp
# # instance_semantic_gt = sp.imread('data_semantics/training/semantic/000000_10.png')
# # for i in range(len(instance_semantic_gt)):
# #     for j in range(len(instance_semantic_gt[0])):
# #         if instance_semantic_gt[i][j] <= 6:
# #             print(str(i) + " " + str(j))
# #
# # cv.imshow("semantics", seman)
# #
# # cv.waitKey(0)
#
def all_idx(idx, axis):
    grid = np.ogrid[tuple(map(slice, idx.shape))]
    grid.insert(axis, idx)
    return tuple(grid)

def onehot_initialization(a):
    ncols = 13
    out = np.zeros(a.shape + (ncols,), dtype=int)
    out[all_idx(a, axis=2)] = 1
    return out


# img = sp.imread('vkitti/vkitti_semantic_processed/0001/00000.png')
# img = onehot_initialization(img)
# print(type(img))
# print(img.shape)
# print(img[0][0])

import os

pathList = os.listdir("vkitti/vkitti_semantic_processed/0001")
for file in pathList:
    #print(file)
    path = "vkitti/vkitti_semantic_processed/0001/" + file
    image = sp.imread(path)
    if image.max() > 12 or image.min() < 0:
        print("error")

# lab_source = Image.open("vkitti/vkitti_semantic_processed/0001/00000.png")
# print(type(lab_source))
# lab_source = lab_source.resize((640, 192), Image.NEAREST)
# print(type(lab_source))
# lab_source = np.array(lab_source)
# print(type(lab_source))
# print(lab_source.shape)