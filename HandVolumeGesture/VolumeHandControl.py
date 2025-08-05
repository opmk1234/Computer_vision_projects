import HandTrackingModule as ht
import cv2
import os
import time 
import numpy as np
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Get default audio device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Get the volume interface
volume = interface.QueryInterface(IAudioEndpointVolume)

# Print volume range
volrange =volume.GetVolumeRange()  # (minVolume, maxVolume, increment)
minvol = volrange[0]
maxvol = volrange[1]
# Set volume level (for example -20.0 dB)
volu = 0
#front end gui
volbar=400
ch,cw = 640,480

cap = cv2.VideoCapture(0)
cap.set(3,ch)
cap.set(4,cw)
detector = ht.HandDetector(Detectioncon=0.4,maxHands=1)
ptime = 0
while (True):
    suc,frame = cap.read()
    frame=detector.DetectHand(frame)
    
    lmlist = detector.findposition(frame,draw = False)
    if len(lmlist)!=0:
     #print(lmlist[4],lmlist[8])
     x1,y1 = lmlist[4][1],lmlist[4][2]
     x2,y2=lmlist[8][1],lmlist[8][2]
     cv2.circle(frame,(x1,y1),15,(255,255,255),cv2.FILLED)
     cv2.circle(frame,(x2,y2),15,(255,255,255),cv2.FILLED)
     #// to convert to the integer
     xc,yc = (x1+x2)//2,(y1+y2)//2
     cv2.circle(frame,(xc,yc),15,(255,255,255),cv2.FILLED)
     cv2.line(frame,(x1,y1),(x2,y2),(255,255,255),4)
     length = math.hypot((x2-x1),(y2-y1))
     #print(length)

     #finger (130-9) 360 19
     #vol(-65,0)
     vol = np.interp(length,[50,200],[minvol,maxvol])
     volbar = np.interp(length,[50,200],[400,150])
     
     volume.SetMasterVolumeLevel(vol, None)
     print(vol)
     if length<50:
      cv2.circle(frame,(xc,yc),15,(0,255,0),cv2.FILLED)
        
    cv2.rectangle(frame,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(frame,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)

    ctime=time.time()
    if ctime!=ptime:
     fps=1/(ctime-ptime)
     ptime = ctime
     cv2.putText(frame,f'FPS:{int(fps)}',(50,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    cv2.imshow("window",frame)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
