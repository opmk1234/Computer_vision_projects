import cv2
import os
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import time

BrushThickness = 15
EraserThickness = 50

# Hand detector
handdetector = htm.HandDetector(maxHands=1)

# Load header images
folderPath = "images"
overlayList = []
for imPath in sorted(os.listdir(folderPath)):
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]
drawColor = (0, 0, 255)  # Default red color

# Setup camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Canvas for drawing
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

xp, yp = 0, 0
ptime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Overlay header
    img[0:125, 0:1280] = header

    # Find hand
    img = handdetector.findhands(img)
    lmList = handdetector.findposition(img, draw=False)

    if lmList:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:] # Middle finger tip

        fingers = handdetector.fingerup()

        # Selection mode (2 fingers up)
        if fingers[1] == 1 and fingers[2] == 1:
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)

            if y1 < 125:  # Only in header area
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (0, 0, 255)  # Red
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (0, 255, 0)  # Green
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (255, 0, 0)  # Blue
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)  # Eraser
                elif 1200 < x1 < 1280:  # Clear canvas
                    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        # Drawing mode (index finger up)
        if fingers[1] == 1 and fingers[2] == 0:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            thickness = EraserThickness if drawColor == (0, 0, 0) else BrushThickness
            cv2.line(img, (xp, yp), (x1, y1), drawColor, thickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)

            xp, yp = x1, y1

    # Merge canvas with webcam feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # FPS Counter
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}', (50, 70),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Virtual Painter", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
