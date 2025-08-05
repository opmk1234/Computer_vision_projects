import cv2
import os 
import time
import HandTrackingModule as ht
import autopy
wcam,hcam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
paths = "Fingers"
mylist =os.listdir(paths)
print(mylist)
overlaylist=[]
overlay_resized=[]
for imgpath in mylist:
    image =cv2.imread(f'{paths}/{imgpath}')
    overlaylist.append(image)
    #overlay_resized.append(cv2.resize(overlaylist[0], (200, 200)))

for img in overlaylist:
    overlay_resized.append(cv2.resize(img, (200, 200)))
detector =ht.HandDetector(maxHands=1,Detectioncon=0.7)
ptime = 0
tipls=[4,8,12,16,20]
while(True):
    suc,frame = cap.read()
    frame = detector.findhands(frame)
    lmlist =detector.findposition(frame,draw=False)
    #frame[0:200,0:200]=overlay_resized[0]
    if len(lmlist)!= 0:
     finger = []
     if lmlist[tipls[0]][1]>lmlist[(tipls[0]-1)][1]:
            finger.append(1)
     else:
            finger.append(0)

     for id in range(1,5):
         if lmlist[tipls[id]][2]<lmlist[(tipls[id]-2)][2]:
            finger.append(1)
         else:
            finger.append(0)
     #print(finger)
     totalfinger=finger.count(1)
     print(totalfinger)
     frame[0:200,0:200]=overlay_resized[totalfinger-1]
                
    ctime= time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(frame,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)

    cv2.imshow('frame',frame)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        cv2.destroyAllWindows()
        break
        
     