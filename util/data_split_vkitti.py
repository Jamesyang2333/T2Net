import os
import imghdr
from PIL import Image
import random

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

indir = "../datasets/vkitti_rgb_dirs.txt"
ratio = 0.2
dirList = []
with open(indir, 'r') as input:
    for line in input:
        if line.strip():
            dirList.append(os.path.join(os.getcwd(), line.strip()))

pathList = []
dirList = []
with open(indir, 'r') as input:
    for line in input:
        if line.strip():
            dirList.append(os.path.join(os.getcwd(), line.strip()))

for dir in dirList:
    idx = dir[-10: -6]
    segdir = "../datasets/vkitti/vkitti_semantic_processed/" + idx
    fileList = os.listdir(dir)
    for current in fileList:
        completePath = os.path.join(dir, current)
        if is_image(completePath):
            pathList.append([idx, current])

    random.shuffle(pathList)
    testSize = int(len(pathList) * float(ratio))
    testList = pathList[0: testSize]
    trainList = pathList[testSize:]

with open("../datasets/vkitti_rgb.txt", 'w') as allFile:
    for path in pathList:
        allFile.write(os.path.join(dir, path[1]) + "\n")
    allFile.close()

with open("../datasets/vkitti_semantic.txt", 'w') as allFile:
    for path in pathList:
        allFile.write("datasets/vkitti/vkitti_semantic_processed/" + path[0] + "/" + path[1] + "\n")
    allFile.close()

with open("../datasets/vkitti_rgb_train.txt", 'w') as allFile:
    for path in trainList:
        allFile.write(os.path.join(dir, path[1]) + "\n")
    allFile.close()

with open("../datasets/vkitti_semantic_train.txt", 'w') as allFile:
    for path in trainList:
        allFile.write("datasets/vkitti/vkitti_semantic_processed/" + path[0] + "/" + path[1] + "\n")
    allFile.close()

with open("../datasets/vkitti_rgb_test.txt", 'w') as allFile:
    for path in testList:
        allFile.write(os.path.join(dir, path[1]) + "\n")
    allFile.close()

with open("../datasets/vkitti_semantic_test.txt", 'w') as allFile:
    for path in testList:
        allFile.write("datasets/vkitti/vkitti_semantic_processed/" + path[0] + "/" + path[1] + "\n")
    allFile.close()

print("The dataset has been splited into " + str(len(pathList) - testSize) + " training images and " + str(testSize) + " test images")

