import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

detector = HandDetector(detectionCon=0.5, maxHands=2)
colorR = (255,0,255)
cx, cy, w, h = 100, 100, 200, 200



class DragRect():
    def __init__(self,posCenter, colordata=(255,0,255), size=[200,200]):
        self.posCenter = posCenter
        self.colordata = colordata
        self.size = size
    def update(self,cursor,length, length2):
        cx, cy = self.posCenter
        w, h = self.size
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            self.colordata = (240,12,255)

            if length < 30:
                self.posCenter = cursor[0], cursor[1]
                self.colordata = (0,255,0)
            if length2 > 80:
                self.size = int(length2),int(length2)

        else:
            self.colordata = (255,0,255)



#rect = DragRect([150,150])
rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))


while True:
    Success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img= detector.findHands(img)

    if hands:
        lmList1 = hands[0]["lmList"]

        length,_ = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2])
        cursor = lmList1[8]
        distance = cursor[2] * (-1)
        distance = distance / 1.5
        if len(hands) == 2:
            lmList2 = hands[1]["lmList"]
            length2,info2 = detector.findDistance(lmList1[8][0:2],lmList2[8][0:2])
            fingerup = detector.fingersUp(hands[1])
            if(fingerup == [0, 0, 0, 0, 0]):

            #cursor = lmList2[8]
                for rect in rectList:
                   rect.update(cursor, length, length2)

        if len(hands) != 2:
            for rect in rectList:
                rect.update(cursor, length, length2=50)

    #this is for solid color:_________________________________-
    """for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        colorR = rect.colordata
        cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)"""


    #This is for Transparant color Alpha:______________________________-
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        colorR = rect.colordata
        cv2.rectangle(imgNew, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w// 2, cy - h// 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.2
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Hello.os", out)
    cv2.waitKey(1)
