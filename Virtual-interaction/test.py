import cv2
import cvzone
import numpy as np

im = cv2.resize(cv2.imread("CursorIMGS/cursor.png", cv2.IMREAD_UNCHANGED), (50,50))
# im = cv2.imread("CursorIMGS/cursor.png", cv2.IMREAD_UNCHANGED)

# im = cv2.imread("IMGS/test_out.png", cv2.IMREAD_UNCHANGED)

cv2.imshow("display",im)
print(im.shape)

blue = cv2.resize(cv2.imread("MainIMG/1.jpg"), (550,500))
# blue = cv2.imread("MainIMG/1.jpg")
blue = cvzone.overlayPNG(blue, im, [50,100])

cv2.imshow("Final",blue)
cv2.waitKey(0)
