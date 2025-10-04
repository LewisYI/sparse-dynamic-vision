#  来源：https://blog.csdn.net/qq_36265860/article/details/111114719
import numpy as np
import os
import sys
import cv2

image_path = "utils\\00000.jpg"
gray_img = cv2.imread(image_path)
gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2GRAY)
print(gray_img.shape)
print(gray_img)
# 偏移方向 建议设置区间[-5,5]
xshift = 3
yshift = -3
xlong = gray_img.shape[1] - 2 * abs(xshift)
ylong = gray_img.shape[0] - 2 * abs(yshift)
pic_shape = [ylong, xlong, 3]
print(pic_shape)
img = np.full(pic_shape, 0, dtype=np.uint8)

for i in range(abs(yshift), ylong):
    for j in range(abs(xshift), xlong):
        if int(gray_img[i + yshift][j + xshift]) - int(gray_img[i][j]) > 10:
            img[i][j] = [0, 255, 0]
        if int(gray_img[i + yshift][j + xshift]) - int(gray_img[i][j]) < -10:
            img[i][j] = [0, 0, 255]
cv2.imshow("image", img)
cv2.waitKey(0)