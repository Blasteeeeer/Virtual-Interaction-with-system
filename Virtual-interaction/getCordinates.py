import cv2

# cap = cv2.VideoCapture(0)
# cv.namedWindow("Frame", cv.WND_PROP_FULLSCREEN)
# cv.setWindowProperty("Frame", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ',', y)

#
while True:
    # _, img = cap.read()
    # img = cv.flip(img, 1)
    # img = cv2.imread("C://Users//abdulla khan//Virtual-interaction//1.png")
    img = cv2.imread("C://Users//abdulla khan//Virtual-interaction//Snapshot//3.png")
    # img = cv2.resize(cv2.imread("MainIMG/1.jpg"), (550,500))

    # img1 = cv2.resize(cv2.imread("IMGS/menuScreen/menu.png"), (240, 350))
    # img2 = cv2.resize(cv2.imread("IMGS/menuScreen/size1.png"), (240, 350))
    # img = cv2.vconcat([img1, img2])

    # print(img.shape)
    # img = cv2.resize(img,(700,400))
    # print("after",img.shape)
    # img = cv2.imread("C://Users//abdulla khan//Downloads//aircanvas painter (1).png")
    # cv2.imshow("out", img[:120,:120])
    cv2.imshow("Frame", img)
    cv2.setMouseCallback('Frame', click_event)
    if cv2.waitKey(1) == ord('q'):
        break

# for i in range(2,8):
#     img = cv2.imread("C://Users//abdulla khan//Virtual-interaction//PAINTER_IMG//" + str(i) + ".png")
#     img = img[:206, :]
#     img = cv2.resize(img, (1280, 125))
#     cv2.imwrite("C://Users//abdulla khan//Virtual-interaction//PAINTER_IMGS//" + str(i-1) + ".png",img)


cap.release()
cv2.destroyAllWindows()
