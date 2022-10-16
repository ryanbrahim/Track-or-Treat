import numpy as np
import cv2
import math
import time
import os

os.system("cat /dev/null > ./timestamp-logs")

# time for which face must be in frame before getting counted as a true positive
SECONDS_TO_CREDIT = 2
# time before which an undetected face gets killed, as it is assumed not coming back
SECONDS_TO_DIE = 0.3
# maximum radius to allow movement for faces
MAX_RADIUS = 50;

# array to store active faces in frame
activeFaces = []
# structure: [(x,y), spawn time, last seen time]

# open video camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, img = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        # draw box (turn off when solved)
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # TODO check existence
        found = False
        for activeFace in activeFaces:
            ax = activeFace[0][0]
            ay = activeFace[0][1]
            if(math.hypot(ax-x, ay-y) < MAX_RADIUS):
                found = True
                activeFace[2] = time.time() # face found so reset last seen time
                activeFace[0] = (x, y) # give found face updated location
                if(time.time() - activeFace[1] > SECONDS_TO_CREDIT and time.time() - activeFace[1] < 100):
                    # FILE LOGGING COMMANDS
                    os.system('date | grep -e "[0-9][0-9]:[0-9][0-9]:[0-9][0-9]" -o >> ./timestamp-logs')
                    os.system('echo 1 > dirtybit')  # set dirtybit so site knows to request data update
                    activeFace[1] -= 150
                break
        
        if(not found):
            activeFaces.append([(x,y), time.time(), time.time()]) # add new face

    for face in activeFaces:
        if(time.time() - face[2] > SECONDS_TO_DIE):
            activeFaces.remove(face)

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()