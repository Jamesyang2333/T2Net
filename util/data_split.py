import os
import random
import argparse
import imghdr
import logging
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

# def _process_image(im_url, out_url):
#     """
#     process an image according to the input parameters and save the file in an output folder
#
#     Parameters
#     ----------
#     im_url: absolute path of the file
#     out_url: absolute path of the output folder
#
#     Returns
#     -------
#
#     """
#
#     if is_image(im_url):
#         img = cv.imread(im_url)
#
#         if args.mode == "overexposure":
#             alpha_over = 1.5 + np.random.random() * 1.5
#             beta_over = 100
#             new_image = cv.convertScaleAbs(img, alpha=alpha_over, beta=beta_over)
#
#         else:
#             gamma_under = 6 + np.random.random() * 4
#             lookUpTable_under = np.empty((1, 256), np.uint8)
#             for i in range(256):
#                 lookUpTable_under[0, i] = np.clip(pow(i / 255.0, gamma_under) * 255.0, 0, 255)
#             new_image = cv.LUT(img, lookUpTable_under)
#
#         cv.imwrite(out_url, new_image)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--ratio", type=str, required=True,
                        help="Ratio of test set for this split")
    parser.add_argument("-i", "--indir", type=str, required=True,
                        help="Relative path of the input file containing the data locations.")
    parser.add_argument("-o", "--outdir", type=str, required=True,
                        help="Relative path of the output directory for output txt files")
    parser.add_argument("-n", "--nameOfDataset", type=str, required=True,
                        help="Name of the dataset used in the output files")
    # parser.add_argument("-j", "--njobs", type=int,required=False, default=1,
    #                     help="Number of jobs to run in parallel")
    # parser.add_argument("-m", "--max_size", type=int, required=False, default=0,
    #                     help="Input directory containing images.")
    args = parser.parse_args()

    in_dir = os.path.join(os.getcwd(), args.indir)
    out_dir = os.path.join(os.getcwd(), args.outdir)

    if not os.access(out_dir, os.F_OK):
        os.mkdir(out_dir)

    pathList = []
    dirList = []
    with open(in_dir, 'r') as input:
        for line in input:
            if line.strip():
                dirList.append(os.path.join(os.getcwd(), line.strip()))

    for dir in dirList:
        fileList = os.listdir(dir)
        for current in fileList:
            completePath = os.path.join(dir, current)
            if is_image(completePath):
                pathList.append(completePath)

    random.shuffle(pathList)
    testSize = int(len(pathList) * float(args.ratio))
    testList = pathList[0: testSize]
    trainList = pathList[testSize:]
    with open(os.path.join(out_dir, args.nameOfDataset + ".txt"), 'w') as allFile:
        for path in pathList:
            allFile.write(path + "\n")
        allFile.close()

    with open(os.path.join(out_dir, args.nameOfDataset + "_train.txt"), 'w') as trainFile:
        for path in trainList:
            trainFile.write(path + "\n")
        trainFile.close()

    with open(os.path.join(out_dir, args.nameOfDataset + "_test.txt"), 'w') as testFile:
        for path in trainList:
            testFile.write(path + "\n")
        testFile.close()
    print("The dataset has been splited into " + str(len(pathList) - testSize) + " training images and " + str(testSize) + " test images")




