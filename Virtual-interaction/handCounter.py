import cv2
import numpy as np
import time
import os
import hand_detector_module as htm


cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.65,maxHands=2)

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList,_ = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        #tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        
        # 
        fingers = detector.fingersUp()
        count = fingers.count(1)
        cv2.putText(img, str(count), (100, 100) , cv2.FONT_HERSHEY_COMPLEX, 2.5, (0,0,255))


    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()