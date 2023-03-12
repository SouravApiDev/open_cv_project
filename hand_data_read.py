import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
#dector = HandDetector(detectionCon=0.8, maxHands=6)


while True:
    Success, img = cap.read()
    img = cv2.flip(img)
    #hand, img = dector.findHands(img, flipType=True)

    cv2.imshow("Image", img)
    cv2.waitKey(1)