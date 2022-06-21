import cv2
import mediapipe as mp
import numpy as np
import math
import os
import pydirectinput as py
import cvzone
import hand_detector_module as htm
import DragDrop as dp
import fileExplore as file
import speech2text as st


# import convertapi
# import asyncio
# from multiprocessing import Process
# import threading



def main():
    # imgCanvas = np.zeros((detector.hDraw, detector.wDraw, 3), np.uint8)  # Canvas for storing the art
    fakCursor = np.zeros((detector.hDraw, detector.wDraw, 3), np.uint8) + 255  # for fake cursor get's refresh each frames
    Canvas = np.zeros((detector.hDraw, detector.wDraw, 4), np.uint8)
    # xp_cam, yp_cam = 0, 0 #previous points for drawing in webcam
    # xp, yp = 0, 0         # previous points for drawing
    plocX, plocY = 0, 0   #preious location of x and y for smoothning the values
    clocX, clocY = 0, 0   #current location of x and y for smoothning the values
    color = 0,0,0,255
    size = 5
    text = ""
    imTextList = []
    # textY = 0
    slideNum = 0
    FirstTime = True   # for opening ppt
    buttonPressed = False
    buttonPressedundo = False
    delayCounter = 0
    exits = False      # exiting from ppt
    pptRequest = False
    Pass = False       # from keyboard to pencil
    undo = False
    clear = False
    right = False
    left = False


    while True:
        y = 0
        Y = 200
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)                           # finding the hands
        lmList, bbox = detector.findPosition(img, draw=False)   # getting the landmarks cordinates wrt id, bbox for the hand region
        images = detector.storeImage()                          # getting images for the main menu
        drawImage = detector.storeDrawImage()                      # getting images for the canvas menu
        # cv2.imshow("Frame", images[detector.selectedImage])




        if len(lmList) != 0:                                    # if hand is detected then only proceed
            # tip of index and middle fingers
            x1, y1 = lmList[8][1:]      # index finger
            x2, y2 = lmList[12][1:]     # moddle finger

            if detector.mode == "Cursor":
                # Convering the cordinates of webcam wrt monitor screen
                x3 = np.interp(x1, (detector.frameR, detector.wCam - detector.frameR), (0, detector.wScr))
                y3 = np.interp(y1, (detector.frameR, detector.hCam - detector.frameR), (0, detector.hScr))

                # smoothing the values
                clocX = plocX + (x3 - plocX) // detector.smootheningCursor
                clocY = plocY + (y3 - plocY) // detector.smootheningCursor

            elif detector.mode == "Drawing" or detector.mode == "Presentation":
                # Convering the cordinates of webcam wrt drawing screen
                x3 = np.interp(x1, (detector.frameR, detector.wCam - detector.frameR), (0, detector.wDraw))
                y3 = np.interp(y1, (detector.frameR, detector.hCam - detector.frameR), (0, detector.hDraw))

                # smoothing the values
                clocX = plocX + (x3 - plocX) // detector.smootheningDrawing
                clocY = plocY + (y3 - plocY) // detector.smootheningDrawing
            else:
                # Converting the cordinates of webcam wrt main menu screen
                x3 = np.interp(x1, (0, detector.wCam), (0, detector.mainScreenWidth))
                y3 = np.interp(y1, (0, detector.hCam), (0, detector.mainScreenHeigth))


            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            # 4. If Selection Mode - one finger are up
            if fingers:
                # xp, yp = 0, 0

                if detector.mode == "Main":
                    detector.selectedImage = 0
                elif detector.mode == "Drawing":
                    detector.selectedImage = 1
                elif detector.mode == "Cursor":
                    detector.selectedImage = 2
                elif detector.mode == "Presentation":
                    detector.selectedImage = 3
                # print("Selection Mode")


                ################################################
                # cursor function
                ################################################

                if detector.mode == "Cursor":
                    if detector.fingers[1] and detector.fingers[2] == 0:
                        py.moveTo(int(clocX), int(clocY))
                    if detector.Clicked(img):
                        py.doubleClick()#click()
                        cv2.waitKey(500)

                    # exiting
                    if detector.fingers == [0,1,1,1,1]:
                        detector.mode = "Main"

                ################################################
                # Presentation function
                ################################################

                if detector.mode == "Presentation":

                    if FirstTime:

                        # p3 = threading.Thread(target=detector.Cursor(clocX, clocY, img))
                        # p3.start()

                        # py.FAILSAFE = False
                        #
                        # if detector.fingers[1] and detector.fingers[2] == 0:
                        #     py.moveTo(clocX, clocY)
                        # if detector.Clicked(img):
                        #     py.doubleClick()  # click()
                        #     cv2.waitKey(500)


                        # detector.pptx_path = file.browseFiles()
                        # p1 = threading.Thread(target=file.browseFiles, args=(detector, detector.fingers[1], detector.fingers[2], clocX,clocY,img))
                        # p1.setDaemon(True)
                        # detector.pptx_path = p1.start()
                        # print(detector.pptx_path)
                        # p1.join()
                        # p2.join()

                        detector.pptx_path = file.browseFiles()

                        if detector.pptx_path:
                            # p1.root.quit()
                            # p3.join()
                            detector.pptx_path = '\\'.join(detector.pptx_path.split('/'))
                            file.ppt2img(detector.pptx_path)

                            path = "C:\\Users\\abdulla khan\\Virtual-interaction\\presentationIMGS"
                            # print(sorted(os.listdir(path), key=len))
                            # for i in sorted(os.listdir(path), key=len):
                            #     detector.pptIMG.append(cv2.imread(path + "\\" + i))
                            pptLength = len(sorted(os.listdir(path), key=len))
                            FirstTime = False

                    # print("Slide=",slideNum)
                    # print(len(detector.pptIMG))
                    if detector.pptx_path:

                        # cv2.namedWindow("Canvas", cv2.WND_PROP_FULLSCREEN)
                        # cv2.setWindowProperty("Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN - 500)

                        if (detector.fingers == [0, 0, 0, 0, 1] and slideNum < pptLength - 1 and buttonPressed is False) or right:
                            right = False
                            slideNum += 1
                            buttonPressed = True

                        elif (detector.fingers == [1, 0, 0, 0, 0] and slideNum > 0 and buttonPressed is False) or left:
                            left = False
                            slideNum -= 1
                            buttonPressed = True

                        elif detector.fingers == [0, 0, 0, 0, 0]:
                            buttonPressed = False

                        # ppt = detector.pptIMG[slideNum]  "C:\Users\abdulla khan\Virtual-interaction\PresentationIMGS\Slide1.PNG"
                        path = "presentationIMGS"
                        ppt = cv2.resize(cv2.imread(path + "\\Slide" + str(slideNum+1) + ".png"), (detector.wDraw, detector.hDraw))


                        if detector.fingers == [0, 1, 0, 0, 0] or detector.fingers == [0, 1, 1, 0, 0]:
                            cv2.circle(ppt, (int(clocX), int(clocY)), 10, (0, 0, 0),5)

                        imgSmall = cv2.resize(img, (detector.smallcam_Width, detector.smallcam_Height))
                        h, w, _ = ppt.shape
                        ppt[h - detector.smallcam_Height: h, w - detector.smallcam_Width: w] = imgSmall

                        if clocY <= 95 and clocX <= 400:
                            cv2.rectangle(ppt, (40, 40), (180,100), (100,100,100), 8)
                            cv2.putText(ppt, "QUIT", (55, 85), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 5)

                            if clocX >= 40 and clocX <= 180 and clocY >= 40 and clocY <= 100 and detector.Clicked(img):
                                exits = True

                            cv2.rectangle(ppt, (200, 40), (340, 100), (100, 100, 100), 8)
                            cv2.putText(ppt, "EDIT", (215, 85), cv2.FONT_HERSHEY_PLAIN,3, (0, 0, 0), 5)

                            if clocX >= 200 and clocX <= 340 and clocY >= 40 and clocY <= 100 and detector.Clicked(img):
                                detector.mode = "Drawing"
                                pptRequest = True


                        ## left button ##
                        elif clocX <= 95 and slideNum > 0:
                            pts = [(80, h//2 - 75), (15, h//2), (80, h//2 + 75)]
                            cv2.polylines(ppt, np.array([pts]), False, (100,100,100), 5)

                            if detector.Clicked(img) and buttonPressedundo == False:
                                left = True
                                buttonPressedundo = True

                        ## right button ##
                        elif clocX >= w - 95 and slideNum < pptLength - 1:
                            pts = [(w - 80,h//2 - 75), (w - 15,h//2), (w - 80,h//2 + 75)]
                            cv2.polylines(ppt, np.array([pts]), False, (100,100,100), 5)
                            if detector.Clicked(img) and buttonPressedundo == False:
                                right = True
                                buttonPressedundo = True

                        if not(detector.Clicked(img)):
                            buttonPressedundo = False

                        # print(clocY)
                        # cv2.imshow("Canvas", ppt)
                        cv2.imshow("Canvas", cv2.resize((ppt),(detector.wScr, detector.hScr)))

                    if exits or not(detector.pptx_path) :
                        if detector.pptx_path:
                            file.eraseFile(path)
                            slideNum = 0
                            cv2.destroyWindow("Canvas")
                            detector.pptIMG = []

                        FirstTime = True
                        detector.pptx_path = ""
                        detector.mode = "Main"
                        print("Exit presentation")
                        cv2.waitKey(500)


                ################################################
                # drawing function
                ################################################

                elif detector.mode == "Drawing":
                    # print("Drawing!!!")
                    # cv2.namedWindow("Canvas", cv2.WND_PROP_FULLSCREEN)
                    # cv2.setWindowProperty("Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN - 500)

                    if pptRequest:
                        fakCursor = np.zeros((detector.hDraw, detector.wDraw, 3), np.uint8) + 255
                        fakCursor[125:,:] = cv2.resize(cv2.imread(path + "\\Slide" + str(slideNum+1) + ".png"), (detector.wDraw, detector.hDraw - 125))
                        Canvas = np.zeros((detector.hDraw, detector.wDraw, 4), np.uint8)
                    else:
                        fakCursor = np.zeros((detector.hDraw, detector.wDraw, 3), np.uint8) + 255
                        Canvas = np.zeros((detector.hDraw, detector.wDraw, 4), np.uint8)

                    fakCursor[0:125, :] = drawImage[detector.header]

                    clocX, clocY = int(clocX), int(clocY)

                    #################################
                    # drag n drop for text images
                    #################################
                    cursor = (clocX, clocY)
                    if detector.Clicked(img):
                        for imgObject in imTextList:
                            imgObject.update(cursor)

                    # try:

                    for imgObject in imTextList:

                        # Draw for JPG image
                        h, w = imgObject.size
                        ox, oy = imgObject.posOrigin
                        if ox > 0 and (ox + w) < detector.wDraw  and oy > 125 and (oy + h) < detector.hDraw:
                            fakCursor = cvzone.overlayPNG(fakCursor, imgObject.img, [ox, oy])
                            imgObject.previousValue(ox, oy)
                        # fakCursor[oy:oy + h, ox:ox + w] = imgObject.img
                        else:
                            fakCursor = cvzone.overlayPNG(fakCursor, imgObject.img, [imgObject.prev_ox, imgObject.prev_oy])
                    # except:
                    #     pass


                    ################# Drawing ###################

                    for i in range(len(detector.annotations)):
                        for j in range(len(detector.annotations[i])):
                            if j!= 0:
                                # cv2.line(fakCursor, detector.annotations[i][j - 1], detector.annotations[i][j], detector.annotationColor[i], detector.annotationSize[i])
                                cv2.line(Canvas, detector.annotations[i][j - 1], detector.annotations[i][j],detector.annotationColor[i], detector.annotationSize[i])

                    fakCursor = cvzone.overlayPNG(fakCursor, Canvas)

                    if detector.headerMode == "Menu":
                        detector.header = 5
                        menuImage = cv2.vconcat([detector.MenuImage, detector.SizeImage])
                        h, w, _ = menuImage.shape
                        fakCursor[125:125 + h, :w] = menuImage

                        if clocX >= 10 and clocX <= 150 and clocY >= 135 and clocY <= 190 and detector.Clicked(img):
                            clear = True
                            menuImage = cv2.vconcat([detector.ClearImage, detector.SizeImage])
                            h, w, _ = menuImage.shape
                            fakCursor[125:125 + h, :w] = menuImage
                        elif clocX >= 10 and clocX <= 150 and clocY >= 206 and clocY <= 265 and detector.Clicked(img) and buttonPressedundo == False:
                            undo = True
                            menuImage = cv2.vconcat([detector.UndoImage, detector.SizeImage])
                            h, w, _ = menuImage.shape
                            fakCursor[125:125 + h, :w] = menuImage
                            buttonPressedundo = True
                        elif clocX >= 15 and clocX <= 145 and clocY >= 352 and clocY <= 400 and detector.Clicked(img):
                            size = detector.drawSize = 2
                            detector.SizeImage = detector.Size1Image
                        elif clocX >= 15 and clocX <= 145 and clocY >= 410 and clocY <= 456 and detector.Clicked(img):
                            size = detector.drawSize = 5
                            detector.SizeImage = detector.Size2Image
                        elif clocX >= 15 and clocX <= 145 and clocY >= 460 and clocY <= 505 and detector.Clicked(img):
                            size = detector.drawSize = 8
                            detector.SizeImage = detector.Size3Image
                        elif detector.Clicked(img) == False:
                            buttonPressedundo = False
                        else:
                            pass

                    elif detector.headerMode == "Pencil":
                        detector.header = 0
                        detector.drawColor = color
                        detector.drawSize = size
                    elif detector.headerMode == "Eraser":
                        detector.header = 1
                        detector.drawColor = (255, 255, 255,0)
                        detector.drawSize = 20
                    elif detector.headerMode == "Colors":
                        fakCursor[125:265, 400:540] = detector.ColorsImage
                        detector.header = 2

                        if clocX >= 411 and clocX <= 437 and clocY >= 137 and clocY <= 160 and detector.Clicked(img):
                            color = detector.drawColor = (42,42,234,255)
                        elif clocX >= 457 and clocX <= 483 and clocY >= 137 and clocY <= 160 and detector.Clicked(img):
                            color = detector.drawColor = (255,182,56,255)
                        elif clocX >= 504 and clocX <= 530 and clocY >= 137 and clocY <= 160 and detector.Clicked(img):
                            color = detector.drawColor = (87,217,126,255)

                        elif clocX >= 411 and clocX <= 437 and clocY >= 183 and clocY <= 206 and detector.Clicked(img):
                            color = detector.drawColor = (0, 0, 0,255)
                        elif clocX >= 457 and clocX <= 483 and clocY >= 183 and clocY <= 206 and detector.Clicked(img):
                            color = detector.drawColor = (0,218,255,255)
                        elif clocX >= 504 and clocX <= 530 and clocY >= 183 and clocY <= 206 and detector.Clicked(img):
                            color = detector.drawColor = (255, 255, 255,255)

                        elif clocX >= 411 and clocX <= 437 and clocY >= 229 and clocY <= 252 and detector.Clicked(img):
                            color = detector.drawColor = (196,102,255,255)
                        elif clocX >= 457 and clocX <= 483 and clocY >= 229 and clocY <= 252 and detector.Clicked(img):
                            color = detector.drawColor = (255, 82, 140,255)
                        elif clocX >= 504 and clocX <= 530 and clocY >= 229 and clocY <= 252 and detector.Clicked(img):
                            color = detector.drawColor = (30,52,109,255)
                        else:
                            pass

                    elif detector.headerMode == "Text":
                        detector.header = 3
                        h, w, _ = fakCursor.shape
                        fakCursor[h - 400 - 50: h - 50, w - 700 - 300: w - 300] = detector.KeyboardImage1
                        if detector.fingers == [0, 1, 1, 0, 0] and detector.Clicked(img) and buttonPressed is False:
                            buttonPressed = True

                            if detector.Keyboard(clocX, clocY) == "OK" :
                                drag = dp.DragImg(im,[200,200])
                                imTextList.append(drag)
                                text = ""
                                Pass = True
                            elif detector.Keyboard(clocX, clocY) == "Remove" :
                                fakCursor[h - 400 - 50: h - 50, w - 700 - 300: w - 300] = detector.KeyboardImage5
                                text = text[:-1]
                            elif detector.Keyboard(clocX, clocY) == "Mike" :
                                # print("Mike")
                                fakCursor[h - 400 - 50: h - 50, w - 700 - 300: w - 300] = detector.KeyboardImage2
                                hh, ww, _ = detector.Listen.shape
                                fakCursor[125:125+hh , w - ww : w] = detector.Listen

                                imgSmall = cv2.resize(img, (detector.smallcam_Width, detector.smallcam_Height))
                                h, w, _ = fakCursor.shape
                                fakCursor[h - detector.smallcam_Height: h, w - detector.smallcam_Width: w] = imgSmall

                                cv2.imshow("Canvas", cv2.resize((fakCursor), (detector.wScr, detector.hScr)))
                                cv2.waitKey(1)
                                called = st.speech2text().upper()
                                if called == "ERROR":
                                    hh, ww, _ = detector.Sorry.shape
                                    fakCursor[125:125+hh , w - ww : w] = detector.Sorry
                                    cv2.waitKey(500)
                                else:
                                    text += called
                            elif detector.Keyboard(clocX, clocY) == "\n":
                                fakCursor[h - 400 - 50: h - 50, w - 700 - 300: w - 300] = detector.KeyboardImage4
                                text += detector.Keyboard(clocX, clocY)
                            elif detector.Keyboard(clocX, clocY) == " ":
                                fakCursor[h - 400 - 50: h - 50, w - 700 - 300: w - 300] = detector.KeyboardImage3
                                text += detector.Keyboard(clocX, clocY)
                            else:
                                text += detector.Keyboard(clocX, clocY)

                        elif detector.Clicked(img) == False:
                            buttonPressed = False

                        if text:
                            y = text.count('\n') + 1
                            im = np.zeros((20 * y, (len(max(text.split('\n'), key=len)) * 10), 4), np.uint8)
                            # print(text)
                            for i in text.split('\n'):
                                y += 15
                                Y += 15
                                im = cv2.putText(im, i, (0, y), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)
                                fakCursor = cv2.putText(fakCursor, i, (200,Y), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)


                    elif detector.headerMode == "Shapes":
                        fakCursor[125:225, 600:1100] = detector.ShapesImage
                        if clocX >= 617 and clocX <= 684 and clocY >= 143 and clocY <= 210 and detector.Clicked(img) and buttonPressed is False:
                            buttonPressed = True
                            shapesX, shapesY = 80, 80
                            im = np.zeros((shapesY, shapesX, 4), np.uint8)
                            cv2.rectangle(im, (0, 0), (shapesX - 1, shapesY - 1), color, size)
                            drag = dp.DragImg(im, [200, 200])
                            imTextList.append(drag)
                        elif clocX >= 702 and clocX <= 802 and clocY >= 143 and clocY <= 210 and detector.Clicked(img) and buttonPressed is False:
                            buttonPressed = True
                            shapesX, shapesY = 180, 80
                            im = np.zeros((shapesY, shapesX, 4), np.uint8)
                            cv2.rectangle(im, (0, 0), (shapesX - 1, shapesY - 1), color, size)
                            drag = dp.DragImg(im, [200, 200])
                            imTextList.append(drag)
                        elif clocX >= 823 and clocX <= 892 and clocY >= 143 and clocY <= 210 and detector.Clicked(img) and buttonPressed is False:
                            buttonPressed = True
                            shapesX, shapesY = 80, 80
                            im = np.zeros((shapesY, shapesX, 4), np.uint8)
                            pts = [(shapesX//2, 4), (shapesX-4, shapesY-1), (4, shapesY-1)]
                            cv2.polylines(im, np.array([pts]), True, color, size)
                            drag = dp.DragImg(im, [200, 200])
                            imTextList.append(drag)

                        elif clocX >= 913 and clocX <= 983 and clocY >= 143 and clocY <= 210 and detector.Clicked(img) and buttonPressed is False:
                            buttonPressed = True
                            shapesX, shapesY = 80, 80
                            im = np.zeros((shapesY, shapesX, 4), np.uint8)
                            cv2.circle(im, (shapesX // 2, shapesY // 2), (shapesX // 2 - 4), color, size)
                            drag = dp.DragImg(im, [200, 200])
                            imTextList.append(drag)
                        elif clocX >= 1000 and clocX <= 1075 and clocY >= 143 and clocY <= 210 and detector.Clicked(img) and buttonPressed is False:
                            buttonPressed = True
                            shapesX, shapesY = 80, 20
                            im = np.zeros((shapesY, shapesX, 4), np.uint8)
                            cv2.line(im, (0, shapesY // 2), (shapesX, shapesY // 2), color, size)
                            drag = dp.DragImg(im, [200, 200])
                            imTextList.append(drag)

                        elif detector.Clicked(img) == False:
                            buttonPressed = False

                        detector.header = 4
                    else:
                        pass

                    if clocX >= 0 and clocX <= 100 and clocY >= 17 and clocY <= 110:
                        detector.header = 5
                        if detector.Clicked(img):
                            detector.headerMode = "Menu"
                            print("Menu")
                    elif clocX >= 115 and clocX <= 244 and clocY >= 17 and clocY <= 110 or Pass:
                        detector.header = 0
                        if detector.Clicked(img) or Pass:
                            detector.headerMode = "Pencil"
                            Pass = False
                            # print("Pencil")
                    elif clocX >= 254 and clocX <= 394 and clocY >= 17 and clocY <= 110:
                        detector.header = 1
                        if detector.Clicked(img):
                            detector.headerMode = "Eraser"
                            # print("Eraser")
                    elif clocX >= 404 and clocX <= 533 and clocY >= 17 and clocY <= 110:
                        detector.header = 2
                        if detector.Clicked(img):
                            detector.headerMode = "Colors"
                            # print("Colors")
                    elif clocX >= 568 and clocX <= 703 and clocY >= 17 and clocY <= 110:
                        detector.header = 3
                        if detector.Clicked(img):
                            detector.headerMode = "Text"
                            # print("Text")
                    elif clocX >= 750 and clocX <= 878 and clocY >= 17 and clocY <= 110:
                        detector.header = 4
                        if detector.Clicked(img):
                            detector.headerMode = "Shapes"
                            # print("Shapes")
                    elif clocX >= 906 and clocX <= 1037 and clocY >= 34 and clocY <= 102:
                        if detector.Clicked(img) and buttonPressed == False:
                            buttonPressed = True
                            i = detector.fileList()
                            cv2.imwrite("Snapshot//" + str(i) + ".png",fakCursor)
                            cv2.putText(fakCursor, "SAVED", (930,155), cv2. FONT_HERSHEY_PLAIN, 2, (0,0,0), 2)
                            i += 1
                        elif detector.Clicked(img) == False:
                            buttonPressed = False

                    else:
                        pass

                    ######### displaying Cursor ################
                    cv2.circle(img, (x1, y1), detector.drawSize + 10, detector.drawColor, 3)
                    cv2.circle(fakCursor, (clocX, clocY), detector.drawSize + 10, detector.drawColor, 3)
                    cv2.circle(drawImage[detector.header], (clocX, clocY), detector.drawSize + 10, detector.drawColor, 3)


                    if detector.fingers[1] and detector.fingers[2] == False and (detector.headerMode == "Pencil" or detector.headerMode == "Eraser") and clocY > 126:

                        if detector.annotationStart is False:
                            detector.annotationStart = True
                            detector.annotationNumber += 1
                            detector.annotations.append([])
                            detector.annotationColor.append(detector.drawColor)
                            detector.annotationSize.append(detector.drawSize)
                        # print(detector.annotationNumber)
                        detector.annotations[detector.annotationNumber].append((clocX,clocY))

                    else:
                        detector.annotationStart = False

                    ##########  UNDO  #############
                    if (fingers == [0, 1, 1, 1, 0] and buttonPressed == False) or undo:
                        undo = False
                        buttonPressed = True
                        if detector.annotations and detector.annotationColor and detector.annotationSize:
                            detector.annotations.pop(-1)
                            detector.annotationColor.pop(-1)
                            detector.annotationSize.pop(-1)
                            detector.annotationNumber -= 1
                            # cv2.waitKey(500)

                    elif fingers != [0, 1, 1, 1, 0] and buttonPressed == True:
                        buttonPressed = False

                    if clear:         # clear screen
                        # imgCanvas = np.zeros((detector.hDraw, detector.wDraw, 3), np.uint8)
                        # fakCursor = np.zeros((detector.hDraw, detector.wDraw, 3), np.uint8) + 255
                        Canvas = np.zeros((detector.hDraw, detector.wDraw, 4), np.uint8)
                        clear = False
                        detector.annotations = []
                        detector.annotationNumber = -1
                        detector.annotationStart = False
                        detector.annotationColor = []
                        detector.annotationSize = []
                        text = ""
                        imTextList = []

                    # webcam attachment
                    imgSmall = cv2.resize(img, (detector.smallcam_Width, detector.smallcam_Height))
                    h, w, _ = fakCursor.shape
                    fakCursor[h - detector.smallcam_Height: h, w - detector.smallcam_Width: w] = imgSmall



                    cv2.imshow("Canvas", cv2.resize((fakCursor),(detector.wScr, detector.hScr)))

                    # Exiting
                    if clocX >= 1076 and clocX <= 1233 and clocY >= 34 and clocY <= 102 and pptRequest:
                        if detector.Clicked(img):
                            detector.mode = "Presentation"
                            pptRequest = False
                            FirstTime = False

                            detector.annotations = []
                            detector.annotationNumber = -1
                            detector.annotationStart = False
                            detector.annotationColor = []
                            detector.annotationSize = []
                            text = ""
                            imTextList = []
                            detector.headerMode = "Pencil"
                            detector.header = 0
                            detector.SizeImage = detector.Size2Image
                            detector.drawSize = 5
                            size = 5
                            detector.drawColor = (0,0,0,255)
                            color = (0, 0, 0,255)
                            Canvas = np.zeros((detector.hDraw, detector.wDraw, 4), np.uint8)
                            cv2.waitKey(500)

                    elif clocX >= 1076 and clocX <= 1233 and clocY >= 34 and clocY <= 102:
                        if detector.Clicked(img):
                            detector.mode = "Main"
                            print("Exit Canvas")
                            cv2.destroyWindow("Canvas")

                            detector.annotations = []
                            detector.annotationNumber = -1
                            detector.annotationStart = False
                            detector.annotationColor = []
                            detector.annotationSize = []
                            text = ""
                            imTextList = []
                            detector.headerMode = "Pencil"
                            detector.header = 0
                            detector.SizeImage = detector.Size2Image
                            detector.drawSize = 5
                            size = 5
                            detector.drawColor = (0, 0, 0,255)
                            color = (0, 0, 0,255)
                            Canvas = np.zeros((detector.hDraw, detector.wDraw, 4), np.uint8)
                            cv2.waitKey(500)


                    # if detector.fingers == [0,1,1,1,1]:
                    #     detector.mode = "Main"
                    #     print("Exit Canvas")
                    #     cv2.waitKey(500)


                ############################################
                # Main Function
                ############################################


                elif detector.mode == "Main":
                    if x3 >= 102 and x3 <= 454 and y3 >= 104 and y3 <= 157:
                        detector.selectedImage = 1
                        if detector.Clicked(img):
                            detector.mode = "Drawing"
                            cv2.waitKey(500)
                            # print("Drawing")
                    elif (x3 >= 102 and x3 <= 454 and y3 >= 183 and y3 <= 237) :
                        detector.selectedImage = 2
                        if detector.Clicked(img):
                            detector.mode = "Cursor"
                            cv2.waitKey(500)
                            # print("Cursor")
                    elif x3 >= 102 and x3 <= 454 and y3 >= 263 and y3 <= 317:
                        detector.selectedImage = 3
                        if detector.Clicked(img):
                            detector.mode = "Presentation"
                            cv2.waitKey(500)
                            # print("Presentation")
                    elif x3 >= 152 and x3 <= 404 and y3 >= 343 and y3 <= 395:
                        detector.selectedImage = 4
                        if detector.Clicked(img):
                            print("Exit......")
                            break
                    # print(detector.selectedImage)
                    # cv2.circle(images[detector.selectedImage], (int(x3), int(y3)), 15, (0,0,255), cv2.FILLED)
                    try:
                        images[detector.selectedImage] = cvzone.overlayPNG(images[detector.selectedImage], detector.CursorImage, [int(x3), int(y3)])
                    except:
                        pass
                    # cv2.imshow("Frame", images[detector.selectedImage])

            plocX, plocY = clocX, clocY

        if buttonPressed:
            delayCounter += 1
            if delayCounter > 15: # delay = 15

                delayCounter = 0
                buttonPressed = False

        if buttonPressedundo:
            delayCounter += 1
            if delayCounter > 15: # delay = 15

                delayCounter = 0
                buttonPressedundo = False

        if detector.mode != "Drawing" and detector.mode != "Presentation":
            cv2.imshow("MainMenu", images[detector.selectedImage])
        else:
            pass
            # cv2.destroy
        cv2.imshow("Webcam", img)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()


# async def prep():
#     detector.pptx_path = await asyncio.gather(file.browseFiles())

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector(maxHands=1, detectionCon=0.8)
    main()
    # p2 = threading.Thread(target=main)  # , args=(clocX,clocY,img))
    # p2.start()