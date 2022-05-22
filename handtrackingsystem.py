import cv2
import mediapipe as mp
import time
import handtrackingModule as htm



pTime = 0
cTIme = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while True:
    success, img = cap.read()  # gives the frame
    img = detector.handsFinder(img)
    lmList = detector.postionFinder(img)
    if len(lmList) != 0:
        print(lmList[4])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # displaying on the screen
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (40, 40, 40), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)