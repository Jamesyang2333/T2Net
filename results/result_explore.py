import cv2 as cv

img = cv.imread("vkitti_semantic_v100/test_49/images/000000_10_lab_t_g.png")

vals = {21}
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        vals.add(img[i][j][0])
print(vals)