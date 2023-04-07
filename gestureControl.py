import HandTrackignModule as htm
import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import math
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(0.0, None)

minVol=volRange[0]
maxVol=volRange[1]

wCam , hCam = 1280, 720
cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime=0

detector = htm.handDetector(detectionCon=0.8, maxHands=1)
vol=0
volBar=300
volPer=0
length=0
while True:
    success, img =  cap.read()
    img = detector.findHands(img)
    lms = detector.findPosition(img,draw = False)
    if len(lms) != 0:
        # print(lms[2])
        xt, yt = lms[4][1], lms[4][2]
        xp, yp = lms[8][1], lms[8][2]
        if lms[8][2] > lms[6][2] and lms[12][2] < lms[10][2] and lms[16][2] > lms[14][2] and lms[20][2] > lms[18][2]:
            exit()
        if lms[12][2]>lms[9][2] and lms[16][2]>lms[13][2] and lms[20][2]>lms[17][2] and lms[4][2]<lms[1][2]:
            cv.circle(img, (xt, yt), 12, (255, 0, 255), cv.FILLED)
            cv.circle(img, (xp, yp), 12, (255, 0, 255), cv.FILLED)

            cv.line(img, (xp, yp), (xt, yt), (255, 0, 255), 2)
            cv.circle(img, (int((xp + xt) // 2), int((yp + yt) // 2)), 8, (255, 0, 255), cv.FILLED)
            length = math.hypot(xp - xt , yp - yt)
            # print(length)

            vol = np.interp(length,[10,100],[minVol,maxVol])
            volBar = np.interp(length,[10,100],[300,150])
            volPer = np.interp(length,[10,100],[0,100])
            print(vol)
            volume.SetMasterVolumeLevel(vol, None)
            if length < 40:
                cv.circle(img, (int((xp + xt) // 2), int((yp + yt) // 2)), 8, (0, 255, 0), cv.FILLED)
            cv.rectangle(img, (50, 150), (85, 300), (255, 0, 255), 2)
            cv.rectangle(img, (50, int(volBar)), (85, 300), (255, 0, 255), cv.FILLED)
            cv.putText(img, f'{int(volPer)} %', (50, 350), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv.putText(img , f'FPS: {int(fps)}' , (20,70),cv.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
    cv.imshow("img",img)
    cv.waitKey(1)