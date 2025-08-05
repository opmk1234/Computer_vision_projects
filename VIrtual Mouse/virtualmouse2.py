import cv2
import time
import HandTrackingModule as ht
import numpy as np
import autopy

wcam, hcam = 640, 480
frameR = 100  # Frame Reduction
smoothning = 6

plocx, plocy = 0, 0
clocx, clocy = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

detector = ht.HandDetector(maxHands=1)
ptime = 0
wscr, hscr = autopy.screen.size()  # Get screen size

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror view for camera

    # Find hand landmarks
    frame = detector.findhands(frame)
    lmlist = detector.findposition(frame)

    if len(lmlist) != 0:
        # Get tip of index, middle and thumb fingers
        x1, y1 = lmlist[8][1:]   # Index tip
        x2, y2 = lmlist[12][1:]  # Middle tip
        x_thumb, y_thumb = lmlist[4][1:]  # Thumb tip

        fingers = detector.fingerup()

        cv2.rectangle(frame, (frameR, frameR), (wcam - frameR, hcam - frameR), (0, 255, 0), 2)

        # 🖱️ Moving Mode: Index finger up
        if fingers[1] == 1 and fingers[2] == 0:
            # Map hand coordinates to screen coordinates
            x3 = np.interp(x1, (frameR, wcam - frameR), (0, wscr))
            y3 = np.interp(y1, (frameR, hcam - frameR), (0, hscr))

            # Smooth movement
            clocx = plocx + (x3 - plocx) / smoothning
            clocy = plocy + (y3 - plocy) / smoothning

            # Invert horizontal movement
            try:
                autopy.mouse.move(clocx, clocy)  # Horizontal inverted
            except Exception as e:
                print("Mouse move error:", e)

            cv2.circle(frame, (x1, y1), 15, (255, 255, 255), cv2.FILLED)
            plocx, plocy = clocx, clocy

        # 🖱️ Left Click: Index and middle finger close together
        if fingers[1] == 1 and fingers[2] == 1:
            length, frame, lineinfo = detector.findDistance(8, 12, frame)
            if length < 40:
                cv2.circle(frame, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                time.sleep(0.2)  # prevent multiple clicks

        # 🖱️ Right Click: Thumb and index finger close together
        if fingers[0] == 1 and fingers[1] == 1:
            length_thumb_index, frame, lineinfo = detector.findDistance(4, 8, frame)
            if length_thumb_index < 40:
                cv2.circle(frame, (lineinfo[4], lineinfo[5]), 15, (0, 0, 255), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
                time.sleep(0.2)  # prevent multiple right clicks

    # FPS Counter
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(frame, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
