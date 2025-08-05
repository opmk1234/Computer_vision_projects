import cv2
import time
import HandTrackingModule as ht
import numpy as np
import autopy
wcam,hcam = 640,480
smoothning =6
plocx,plocy = 0,0
clocx,clocy = 0,0
cap = cv2.VideoCapture(0)
frameR = 100
cap.set(3,wcam)
cap.set(4,hcam)
detector =ht.HandDetector(maxHands=1)
ptime = 0
wscr ,hscr = autopy.screen.size()
#print(wscr,hscr)
while(True):
    suc,frame = cap.read()
    #print(wscr,hscr)
    frame = detector.findhands(frame)
    lmlist =detector.findposition(frame)
    if len(lmlist)!= 0:
        x1,y1=lmlist[8][1:]
        x2,y2 =lmlist[12][1:]
        fingers = detector.fingerup()
        #print(fingers)
        cv2.rectangle(frame,(frameR,frameR),(wcam-frameR,hcam-frameR),(0,255,0),2)
        if fingers[1]==1 and fingers[2]== 0:
            #print("moving mode")
            x3 = np.interp(x1,(frameR,wcam-frameR),(0,wscr))
            y3 = np.interp(y1,(frameR,hcam-frameR),(0,hscr))
            clocx = plocx+(x3-plocx)/smoothning
            clocy = plocy+(y3-plocy)/smoothning
            autopy.mouse.move(wscr-clocx,clocy)
            cv2.circle(frame,(x1,y1),15,(255,255,255),cv2.FILLED)
            plocx,plocy=clocx,clocy
        if fingers[1]==1 and fingers[2]==1 :
            #print('click mode')
            length,frame,lineinfo= detector.findDistance(8,12,frame)
            #print(length)
            if length<40:
             cv2.circle(frame,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
             autopy.mouse.click()
    ctime= time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(frame,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    cv2.imshow('frame',frame)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        cv2.destroyAllWindows()
        break
        
     