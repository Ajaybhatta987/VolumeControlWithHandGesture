import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)
# First step is to initialize the Hands class an store it in a variable
handsmodule =mp.solutions.hands
# Now second step is to set the hands function which will hold the landmarks points
hands = handsmodule.Hands()
# Last step is to set up the drawing function of hands landmarks on the image
mpDraw = mp.solutions.drawing_utils

#framerate
pTime = 0
cTIme = 0

while True:
    success, img = cap.read()#gives the frame
    #convert the image from the BGR format to the RGB format.
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #we are using the process function from the Mediapipe library to store the hand landmarks detection results in the variable
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    #multi_hand_landmarks is a mulitdim array
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            #landmark information and id number
            for id, lm in enumerate(handLandmarks.landmark):
                # print(id,lm)
                h, w ,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 5:
                    cv2.circle(img,(cx,cy),10,(115,0,255),cv2.FILLED)

            mpDraw.draw_landmarks(img, handLandmarks, handsmodule.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    #displaying fps on the screen
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX,1,
    (255,0,255),4)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
