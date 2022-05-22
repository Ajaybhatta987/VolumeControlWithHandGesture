import cv2
import time
import numpy as np
import math
import handtrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0


while True:
    success, img = cap.read()
    img = detector.handsFinder(img)
    lmList = detector.postionFinder(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4],lmList[8])
        x1, y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1],lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1, y1),7,(108, 184, 177),cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (108, 184, 177), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(115, 153, 149),3)
        cv2.circle(img,(cx,cy),7,(106, 94, 173),cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        vol = np.interp(length,[30, 250],[minVol,maxVol])
        volBar = np.interp(length,[30, 250],[400,150])
        volPer = np.interp(length,[30, 250],[0,100])

        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<30:
            cv2.circle(img, (cx, cy), 7, (255, 255, 255), cv2.FILLED)

    cv2.rectangle(img,(50,150), (85,400),(227, 168, 73),3)
    cv2.rectangle(img,(50,int(volBar)), (85,400),(227, 168, 73), cv2.FILLED)
    cv2.putText(img, f'{str(int(volPer))} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (227, 168, 73), 4)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # displaying on the screen
    cv2.putText(img,f'fps:{ str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (227, 168, 73), 4)
    cv2.imshow("Image", img)
    cv2.waitKey(1)