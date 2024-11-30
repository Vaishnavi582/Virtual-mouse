import cv2
from cvzone.HandTrackingModule import HandDetector
import mouse
import numpy as np
import threading
import time



detector = HandDetector(maxHands=1)

cap = cv2.VideoCapture(0)

cam_w, cam_h = 645, 485
cap.set(3, cam_w)
cap.set(4, cam_h)

frameR = 100
l_delay = 0


def l_clk_delay():
    global l_delay
    global l_clk_thread
    time.sleep(1)
    l_delay = 0
    l_clk_thread = threading.Thread(target=l_clk_delay)


def r_clk_delay():
    global r_delay
    global r_clk_thread
    time.sleep(1)
    r_delay = 0
    r_clk_thread = threading.Thread(target=r_clk_delay)


def double_clk_delay():
    global double_delay
    global double_clk_thread
    time.sleep(1)
    double_delay = 0
    double_clk_thread = threading.Thread(target=double_clk_delay)



l_clk_thread = threading.Thread(target=l_clk_delay)
r_clk_thread = threading.Thread(target=r_clk_delay)
double_clk_thread = threading.Thread(target=double_clk_delay)



while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)



    if hands:
        print(hands)

        lmlist = hands[0]['lmList']
        ind_x, ind_y = lmlist[8][0], lmlist[8][1]
        mid_x, mid_y = lmlist[12][0], lmlist[12][1]

        cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2)



        fingers = detector.fingersUp(hands[0])
        print(fingers)


        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1:
            conv_x = int(np.interp(ind_x, (frameR, cam_w - frameR), (0, 1278)))
            conv_y = int(np.interp(ind_y, (frameR, cam_h - frameR), (0, 720)))
            mouse.move(conv_x, conv_y)


        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
            if abs(ind_x - mid_x) < 25:
                if fingers[3] == 0 and l_delay == 0:
                    mouse.click(button="left")
                    l_delay = 1
                    l_clk_thread.start()


                if fingers[3] == 1 and l_delay == 0:
                    mouse.click(button="right")
                    l_delay = 1
                    l_clk_thread.start()


        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[4] == 0:
            if abs(ind_x - mid_x) < 25:
                mouse.wheel(delta=-1)



        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[4] == 1:
            if abs(ind_x - mid_x) < 25:
                mouse.wheel(delta=+1)



        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[4] == 0:
            mouse.double_click(button="left")



    cv2.imshow("Camera Feed", img)
    cv2.waitKey(1)


#5 finger close=>scroll up
#liitle finger close =>scroll down
#index,middle,ring finger up=>right click
#index,middle=>left click                                                  
