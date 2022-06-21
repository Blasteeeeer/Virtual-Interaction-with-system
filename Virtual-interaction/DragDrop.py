from PIL import Image
import cv2

class DragImg():
    def __init__(self, img, posOrigin):

        # cv2.imwrite("IMGS/test_in.png", img)
        # self.convertImage2Transparent("IMGS/test_in.png")
        # im = cv2.imread("IMGS/test_out.png", cv2.IMREAD_UNCHANGED)

        self.posOrigin = posOrigin
        self.img = img

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2

    def previousValue(self, prev_ox, pre_oy):
        self.prev_ox = prev_ox
        self.prev_oy = pre_oy


    def convertImage2Transparent(self, in_path = "IMGS/test_in.png", out_path = "IMGS/test_out.png"):

        #  only white to transparent
        img = Image.open(in_path)
        img = img.convert("RGBA")

        datas = img.getdata()

        newData = []

        for items in datas:
            if items[0] == 255 and items[1] == 255 and items[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(items)

        img.putdata(newData)
        img.save(out_path, "PNG")

