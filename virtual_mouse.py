import cv2
from cvzone.HandTrackingModule import HandDetector

import pyautogui
import numpy as np
import math
import time

number = 1

#declare the variables to store the screen width and height(width=2560, height=1440)
screenSize=pyautogui.size()
screenWidth=screenSize[0]
screenHeight=screenSize[1]
# print(screenSize)

#declare the variables to store the camera width, height, & fps
width=640
height=480
frameR=100

#smoothing factor
smoothing=1

#previous coords
prevX=0
prevY=0

#current coords
currX=0
currY=0

cap=cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)

detector = HandDetector(detectionCon=0.8)

while True:
    try:
        check,cameraFeedImg=cap.read()
        cameraFeedImg_flipped=cv2.flip(cameraFeedImg,1)
        handsDetector=detector.findHands(cameraFeedImg_flipped,flipType=False)
        # print("handsDetector", handsDetector)

        hands=handsDetector[0]
        cameraFeedImg_flipped=handsDetector[1]
        # print(hands)

        if hands:
            hand1=hands[0]
            lmList=hand1['lmList']
            handType1=hand1["type"]

            # print(handType1)
            #identifying the fingers
            fingers=detector.fingersUp(hand1)
            # print(fingers)

            #get the index finger tip x & y
            if(len(lmList)>0):
                indexFingerTipX=lmList[8][0]
                indexFingerTipY=lmList[8][1]
                #index finger is up and others are down
                if fingers[1] == 1 and fingers[2] == 0:
                    x3=np.interp(indexFingerTipX,(frameR,width-frameR),(0,screenWidth))
                    y3=np.interp(indexFingerTipY,(frameR,height-frameR),(0,screenHeight))

                    currX=prevX+(x3-prevX)/smoothing
                    currY=prevY+(y3-prevY)/smoothing


                    #moving the cursor
                    pyautogui.moveTo(currX,currY)

                    #draw circle
                    cv2.circle(cameraFeedImg_flipped,(indexFingerTipX,indexFingerTipY),15,(0,255,0),cv2.FILLED)

                    prevX=currX
                    prevY=currY

                if fingers[1] == 1 and fingers[2] == 1:
                    distance=math.dist(lmList[8],lmList[12])

                    indexFingerTipX=lmList[8][0]
                    indexFingerTipY=lmList[8][1]
                    middleFingerTipX=lmList[12][0]
                    middleFingerTipY=lmList[12][1]

                    #draw the center point of the 2 fingers
                    cx=(indexFingerTipX+middleFingerTipX)//2
                    cy=(indexFingerTipY+middleFingerTipY)//2

                    cv2.line(cameraFeedImg_flipped,(indexFingerTipX,indexFingerTipY),(middleFingerTipX,middleFingerTipY),(255,0,0),2)

                    if distance<20:
                        print("D: ",distance)
                        cv2.circle(cameraFeedImg_flipped, (cx,cy), 15,(255,0,0),cv2.FILLED)
                        #perform to click
                        pyautogui.click()
                #thumb is down and other fingers are up
                if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    time.sleep(.1)
                    pyautogui.scroll(300)
                #thumb is up and other fingers are down
                if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    time.sleep(.1)
                    pyautogui.scroll(-300)
                #screenshots
                if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    screenShotPath=f'screenshots/pics_{number}.png'
                    pyautogui.screenshot(screenShotPath)
                    number+=1
                    print('screenshot done')
                    time.sleep(1)



    except Exception as e:
        print(e)

    # cv2.imshow("MyVideo", cameraFeedImg)
    cv2.imshow("MyVideo_flip", cameraFeedImg_flipped)

    if cv2.waitKey(1) == 32:
        break

cap.release()