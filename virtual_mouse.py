# import cv2
# import numpy as np
# import handtrackingModule as htm
# import time
# import pyautogui

# wcam, hcam = 640, 488
# frameR = 100  # Frame reduction
# smoothening = 5

# ########################
# pTime = 0
# plocX, plocY = 0, 0
# clocX, clocY = 0, 0
# cap = cv2.VideoCapture(0)
# cap.set(3, wcam)
# cap.set(4, hcam)
# cTime = 0

# detector = htm.handDetector(maxhands=1)
# wscr, hscr = pyautogui.size()
# print(wscr, hscr)

# while True:
#     success, img = cap.read()
#     img = detector.findhands(img)
#     lmlist, bbox = detector.findPosition(img)

#     if len(lmlist) != 0:
#         x1, y1 = lmlist[8][1:]
#         x2, y2 = lmlist[12][1:]

#         print(x1, y1, x2, y2)
        
#         # Check which fingers are up
#         fingers = detector.fingersUp()
#         cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 2)
        
#         # Only index finger is moving: Moving mode
#         if fingers[1] == 1 and fingers[2] == 0:
#             # Convert coordinates
#             x3 = np.interp(x1, (frameR, wcam - frameR), (0, wscr))
#             y3 = np.interp(y1, (frameR, hcam - frameR), (0, hscr))
            
#             # Smooth the values
#             clocX = plocX + (x3 - plocX) / smoothening
#             clocY = plocY + (y3 - plocY) / smoothening
            
#             # Move mouse
#             pyautogui.moveTo(wscr - clocX, clocY)
#             cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#             plocX, plocY = clocX, clocY
        
#         # Both the index and middle fingers are up: Clicking mode
#         if fingers[1] == 1 and fingers[2] == 1:
#             # Find the distance between fingers
#             length, img, lineinfo = detector.findDistance(8, 12, img)
            
#             # Click mouse if distance is short
#             if length < 40:
#                 cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 255), cv2.FILLED)
#                 pyautogui.click()

#     # Frame rate
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime

#     cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
#     # Display
#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
import cv2
import numpy as np
import time
import pyautogui
import threading
import handtrackingModule as htm  # Assuming this is your custom hand tracking module

# Parameters
wcam, hcam = 640, 488
frameR = 100  # Frame reduction
smoothening = 2  # Lower smoothening value for faster response
clickDebounceTime = 0.3  # 300ms debounce time

# Variables
plocX, plocY = 0, 0
clocX, clocY = 0, 0
lastClickTime = 0  # Initialize lastClickTime
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

detector = htm.handDetector(maxhands=1, detectioncon=0.7, trackcon=0.7)  # Increased detection and tracking confidence
wscr, hscr = pyautogui.size()

# Flag to control the loop
running = True

def start_virtual_mouse():
    global running, plocX, plocY, clocX, clocY, lastClickTime  # Declare lastClickTime as global
    pTime = 0  # Initialize pTime here inside the function
    while running:
        success, img = cap.read()
        if not success:
            break

        img = detector.findhands(img)
        lmlist, bbox = detector.findPosition(img)

        if len(lmlist) != 0:
            x1, y1 = lmlist[8][1:]  # Index finger tip
            x2, y2 = lmlist[12][1:]  # Middle finger tip

            # Check which fingers are up
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 2)

            # Only index finger is moving: Moving mode
            if fingers[1] == 1 and fingers[2] == 0:
                # Convert coordinates
                x3 = np.interp(x1, (frameR, wcam - frameR), (0, wscr))
                y3 = np.interp(y1, (frameR, hcam - frameR), (0, hscr))

                # Smooth the values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # Move mouse
                pyautogui.moveTo(wscr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            # Both index and middle fingers are up: Clicking mode
            if fingers[1] == 1 and fingers[2] == 1:
                # Find the distance between fingers
                length, img, lineinfo = detector.findDistance(8, 12, img)

                # Click mouse if distance is short and within debounce time
                if length < 40:
                    currentTime = time.time()
                    if currentTime - lastClickTime > clickDebounceTime:
                        cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 255), cv2.FILLED)
                        pyautogui.click()
                        lastClickTime = currentTime

        # Frame rate
        cTime = time.time()
        
        # Avoid division by zero by checking if pTime is not zero
        if pTime != 0:
            fps = 1 / (cTime - pTime)
        else:
            fps = 0  # Set fps to 0 for the first frame or before pTime is updated

        pTime = cTime

        # Display FPS
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Optionally display the image if running locally
        # cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def stop_virtual_mouse():
    global running
    running = False
