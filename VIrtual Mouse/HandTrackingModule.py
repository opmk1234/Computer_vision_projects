import cv2
import os
import mediapipe as mp
import time
import math
from matplotlib import pyplot as plt
class HandDetector():
   #maybe self class me dhundega or not self bahr
  def __init__(self,mode=False,maxHands=2,Detectioncon=0.5,trackcon=0.5):
      self.mode = mode
      self.maxHands = maxHands
      self.Detectioncon = Detectioncon
      self.trackcon = trackcon
      
      self.mphands = mp.solutions.hands
      self.hands = self.mphands.Hands( static_image_mode=self.mode,
    max_num_hands=self.maxHands,
    min_detection_confidence=self.Detectioncon,
    min_tracking_confidence=self.trackcon)
      self.mpdraw = mp.solutions.drawing_utils
      self.tipls=[4,8,12,16,20]
    
  def findhands(self,img,draw = True):
    framergb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #so result also a type of something 
    self.result = self.hands.process(framergb)
    #print(self.result.multi_hand_landmarks)
    if self.result.multi_hand_landmarks:
        for multihls in self.result.multi_hand_landmarks:
              if draw:
               self.mpdraw.draw_landmarks(img,multihls,self.mphands.HAND_CONNECTIONS)
    return img
  def findposition(self,img,handno=0,draw=True):
      self.lmlist=[]
      if self.result.multi_hand_landmarks:
       for multihls in self.result.multi_hand_landmarks:
        for id,lm in enumerate(multihls.landmark):
         #print(id,lm)
         h ,w ,c = img.shape
         cx,cy = int(lm.x*w),int(lm.y*h)
         self.lmlist.append([id,cx,cy])
         #print(id,cx,cy)

      return self.lmlist  
  def fingerup(self):
     if len(self.lmlist)!= 0:
      finger =[]
     if self.lmlist[self.tipls[0]][1]>self.lmlist[(self.tipls[0]-1)][1]:
            finger.append(1)
     else:
            finger.append(0)

     for id in range(1,5):
         if self.lmlist[self.tipls[id]][2]<self.lmlist[(self.tipls[id]-2)][2]:
            finger.append(1)
         else:
            finger.append(0)
     return finger 
  def findDistance(self,p1,p2,img,draw=True,r=15,t=3):
     x1, y1 = self.lmlist[p1][1:]
     x2, y2 = self.lmlist[p2][1:]
     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
     if draw:
      cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
      cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
      cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
      cv2.circle(img, (cx,cy),r, (0, 0, 255), cv2.FILLED)
     length = math.hypot(x2 - x1, y2-y1)
     return length, img, [x1, y1, x2, y2, cx, cy]    

     
     
     
     
     
     
     
     
     
        
       
      
      
    
   


   
def main():
    ptime = 0
    ctime = 0
    detector = HandDetector()
    cap = cv2.VideoCapture(0)
    while(True):
     #cap.read() is our friend
     ret,frame = cap.read()
     img =detector.findhands(frame)
       
     lmList = detector.findposition(img)
     if len(lmList)!= 0:
        print(lmList[4])
     ctime = time.time()
     fps = 1/(ctime-ptime)
     ptime = ctime
     cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)        
     cv2.imshow("Image",frame)
     cv2.waitKey(1)        

if __name__ =="__main__":
    main()


