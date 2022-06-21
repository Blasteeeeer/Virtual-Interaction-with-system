import math
import os

import cv2
import mediapipe as mp
import numpy as np
import pydirectinput as py



class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.frameR = 110  # Frame Reduction


        self.smootheningCursor = 7
        self.smootheningDrawing = 4
        self.mode = "Main"
        self.wScr, self.hScr = py.size()
        self.wCam, self.hCam = 640 , 480 # setting cam size

        self.wDraw, self.hDraw = 1280, 720

        self.mainScreenWidth, self.mainScreenHeigth = 550, 500  # setting size of the main menu
        self.selectedImage = 0
        self.drawColor = (0,0,0,255)
        self.drawSize = 5
        self.smallcam_Width, self.smallcam_Height = 213, 120
        self.header = 0
        self.headerMode = "Pencil"

        self.ColorsImage = cv2.resize(cv2.imread("IMGS/Colors.png"), (140,140))
        self.ShapesImage = cv2.resize(cv2.imread("IMGS/shapes.png"), (500, 100))

        self.KeyboardImage1 = cv2.resize(cv2.imread("IMGS/keyboard1.png"), (700,400))
        self.KeyboardImage2 = cv2.resize(cv2.imread("IMGS/keyboard2.png"), (700,400))
        self.KeyboardImage3 = cv2.resize(cv2.imread("IMGS/keyboard3.png"), (700,400))
        self.KeyboardImage4 = cv2.resize(cv2.imread("IMGS/keyboard4.png"), (700,400))
        self.KeyboardImage5 = cv2.resize(cv2.imread("IMGS/keyboard5.png"), (700,400))

        self.Listen = cv2.resize(cv2.imread("IMGS/listen.png"), (360,50))
        self.Sorry = cv2.resize(cv2.imread("IMGS/sorry.png"), (360,50))

        self.MenuImage = cv2.resize(cv2.imread("IMGS/menuScreen/menu.png"), (160, 150))
        self.ClearImage = cv2.resize(cv2.imread("IMGS/menuScreen/clear.png"), (160, 150))
        self.UndoImage = cv2.resize(cv2.imread("IMGS/menuScreen/undo.png"), (160, 150))

        self.Size1Image = cv2.resize(cv2.imread("IMGS/menuScreen/size1.png"), (160, 250))
        self.Size2Image = cv2.resize(cv2.imread("IMGS/menuScreen/size2.png"), (160, 250))
        self.Size3Image = cv2.resize(cv2.imread("IMGS/menuScreen/size3.png"), (160, 250))

        self.SizeImage = self.Size2Image

        self.annotations = []
        self.annotationNumber = -1
        self.annotationStart = False
        self.annotationColor = []
        self.annotationSize = []
        self.pptx_path = ""
        self.pptIMG = []

        self.CursorImage = cv2.resize(cv2.imread("CursorIMGS/cursor2.png", cv2.IMREAD_UNCHANGED), (20,40))


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img


    def findPosition(self, img, handNo=0, draw=False):
        xList = []      # for finding max x cordinates
        yList = []      # for finding max y cordinates
        bbox = []       # for creating a box arounnd hand
        self.lmList = []
        self.bbox = 0, 0, 0, 0
        self.handNo = handNo
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[self.handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)       # conversion of x,y cordinates wrt to image pixel
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            self.bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, self.bbox


    def fingersUp(self):
        self.fingers = []    # [thumb, index, middle, ring, pinky]  1 -> open  0 -> closed
        self.handednes = self.handedness()

        # for thumb
        if self.handednes == 'Left':
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]: #left hand
                self.fingers.append(1)
            else:
                self.fingers.append(0)
        else:
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]: #right hand
                self.fingers.append(1)
            else:
                self.fingers.append(0)

        # for other Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                self.fingers.append(1)
            else:
                self.fingers.append(0)
        return self.fingers


    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


    def handedness(self):           # for finding left or rigth hand
        self.handed = self.results.multi_handedness[self.handNo].classification[0].label
        return self.handed


    def storeImage(self):           # fetching images for main menu
        images = []
        for i in os.listdir("MainIMG"):
            im = cv2.imread("MainIMG/" + i)
            im = cv2.resize(im, (550, 500))
            images.append(im)
        return images

    def storeDrawImage(self):       # fetching images for canvas
        drawImage = []
        mylist = os.listdir("PAINTER_IMGS")
        for i in mylist:
            im = cv2.resize(cv2.imread("PAINTER_IMGS//" + i), (self.wDraw, 125))
            drawImage.append(im)
        return drawImage

    def Clicked(self, img):         # detecting clicked when index and middle finger are closed
        if self.fingers[1] == 1 and self.fingers[2] == 1:
            # Find distance between fingers
            length, img, lineInfo = self.findDistance(8, 12, img)
            # 10. Click mouse if distance short
            if length < 40:
                return True
            else:
                return False

    def fileList(self):         # finding the no. of images in snapshot folder to save the new images
        path = "Snapshot"
        return len(os.listdir(path))

    def Keyboard(self,clocX,clocY):

        clocX = clocX - 281
        clocY = clocY - 271

        if clocX >= 23 and clocX <= 85 and clocY >= 25 and clocY <= 87:
            char = '1'
        elif clocX >= 89 and clocX <= 151  and clocY >= 25 and clocY <= 87:
            char = '2'
        elif clocX >= 155 and clocX<= 217  and clocY >= 25 and clocY <= 87:
            char = '3'
        elif clocX >= 221 and clocX <= 283 and clocY >= 25 and clocY <= 87:
            char = '4'
        elif clocX >= 287 and clocX <= 349 and clocY >= 25 and clocY <= 87:
            char = '5'
        elif clocX >= 353 and clocX <= 415 and clocY >= 25 and clocY <= 87:
            char = '6'
        elif clocX >= 419 and clocX <= 481 and clocY >= 25 and clocY <= 87:
            char = '7'
        elif clocX >= 485 and clocX <= 547 and clocY >= 25 and clocY <= 87:
            char = '8'
        elif clocX >= 551 and clocX <= 613 and clocY >= 25 and clocY <= 87:
            char = '9'
        elif clocX >= 617 and clocX <= 679 and clocY >= 25 and clocY <= 87:
            char = '0'


        elif clocX >= 23 and clocX <= 85 and clocY >= 98 and clocY <= 160:
            char = 'Q'
        elif clocX >= 89 and clocX <= 151 and clocY >= 98 and clocY <= 160:
            char = 'W'
        elif clocX >= 155 and clocX <= 217 and clocY >= 98 and clocY <= 160:
            char = 'E'
        elif clocX >= 221 and clocX <= 283 and clocY >= 98 and clocY <= 160:
            char = 'R'
        elif clocX >= 287 and clocX <= 349 and clocY >= 98 and clocY <= 160:
            char = 'T'
        elif clocX >= 353 and clocX <= 415 and clocY >= 98 and clocY <= 160:
            char = 'Y'
        elif clocX >= 419 and clocX <= 481 and clocY >= 98 and clocY <= 160:
            char = 'U'
        elif clocX >= 485 and clocX <= 547 and clocY >= 98 and clocY <= 160:
            char = 'I'
        elif clocX >= 551 and clocX <= 613 and clocY >= 98 and clocY <= 160:
            char = 'O'
        elif clocX >= 617 and clocX <= 689 and clocY >= 98 and clocY <= 160:
            char = 'P'

        elif clocX >= 23 and clocX <= 85 and clocY >= 170 and clocY <= 234:
            char = 'A'
        elif clocX >= 89 and clocX <= 151 and clocY >= 170 and clocY <= 234:
            char = 'S'
        elif clocX >= 155 and clocX <= 217 and clocY >= 170 and clocY <= 234:
            char = 'D'
        elif clocX >= 221 and clocX <= 283 and clocY >= 170 and clocY <= 234:
            char = 'F'
        elif clocX >= 287 and clocX <= 349 and clocY >= 170 and clocY <= 234:
            char = 'G'
        elif clocX >= 353 and clocX <= 415 and clocY >= 170 and clocY <= 234:
            char = 'H'
        elif clocX >= 419 and clocX <= 481 and clocY >= 170 and clocY <= 234:
            char = 'J'
        elif clocX >= 485 and clocX <= 547 and clocY >= 170 and clocY <= 234:
            char = 'K'
        elif clocX >= 551 and clocX <= 613 and clocY >= 170 and clocY <= 234:
            char = 'L'


        elif clocX >= 89 and clocX <= 151 and clocY >= 245 and clocY <= 306:
            char = 'Z'
        elif clocX >= 155 and clocX <= 217 and clocY >= 245 and clocY <= 306:
            char = 'X'
        elif clocX >= 221 and clocX <= 283 and clocY >= 245 and clocY <= 306:
            char = 'C'
        elif clocX >= 287 and clocX <= 349 and clocY >= 245 and clocY <= 306:
            char = 'V'
        elif clocX >= 353 and clocX <= 415 and clocY >= 245 and clocY <= 306:
            char = 'B'
        elif clocX >= 419 and clocX <= 481 and clocY >= 245 and clocY <= 306:
            char = 'N'
        elif clocX >= 485 and clocX <= 547 and clocY >= 245 and clocY <= 306:
            char = 'M'

        elif clocX >= 89 and clocX <= 290 and clocY >= 317 and clocY <= 380:
            char = ' '
        elif clocX >= 300 and clocX <= 400 and clocY >= 317 and clocY <= 380:
            char = '\n'
        elif clocX >= 405 and clocX <= 480 and clocY >= 317 and clocY <= 380:
            char = 'Remove'
        elif clocX >= 495 and clocX <= 547 and clocY >= 317 and clocY <= 380:
            char = 'Mike'
        elif clocX >= 593 and clocX <= 658 and clocY >= 317 and clocY <= 380:
            char = 'OK'
        else:
            return ""

        return char

    def Cursor(self,clocX,clocY,img):
        if self.fingers[1] and self.fingers[2] == 0:
            py.moveTo(clocX, clocY)
        if self.Clicked(img):
            py.click()
            cv2.waitKey(500)





if __name__  == "__main__":
    cap = cv2.VideoCapture(0)
    detector = handDetector(maxHands=1, detectionCon=0.8)
    clocX, clocY = 0, 0
    plocX, plocY = 0, 0
    edge = True
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)  # finding the hands
        lmList, bbox = detector.findPosition(img, draw=False)  # getting the landmarks cordinates wrt id, bbox for the hand region

        if len(lmList) != 0:  # if hand is detected then only proceed
            # tip of index and middle fingers
            x1, y1 = lmList[8][1:]  # index finger
            x2, y2 = lmList[12][1:]  # moddle finger
            x3 = np.interp(x1, (detector.frameR, detector.wCam - detector.frameR), (0, detector.wScr))
            y3 = np.interp(y1, (detector.frameR, detector.hCam - detector.frameR), (0, detector.hScr))
            clocX = plocX + (x3 - plocX) / detector.smootheningCursor
            clocY = plocY + (y3 - plocY) / detector.smootheningCursor
            fingers = detector.fingersUp()

            if detector.fingers[1] and detector.fingers[2] == False:
                print("Moved")
                # py.moveTo(int(clocX), int(clocY))
                toggle = True

            elif detector.Clicked(img):
                print("Clicked")
                # py.click()

            cv2.waitKey(100)

            # detector.Cursor(clocX,clocY,img)




        plocX, plocY = clocX, clocY
        cv2.imshow("Frame", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


##### W = 7cm  actual Width of object
##### f (focal length) = (w*d)/W     ### w = pixel width of the object
##### d (distance from cam to object) = (W*f)/w
