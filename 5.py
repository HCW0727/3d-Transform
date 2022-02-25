import cv2
from cv2 import threshold
import numpy as np


img = cv2.imread("test_result.jpg")
_,img = threshold(img,253,255,cv2.THRESH_BINARY_INV)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()       