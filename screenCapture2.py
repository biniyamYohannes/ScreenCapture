import numpy as np
from PIL import ImageGrab
import cv2
import time
import imutils

#Define the face cascade and timer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
last_time = time.time()

# Define the codec and create VideoWriter object
out1 = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc(*"XVID"), 5.0, (100,100))
out2 = cv2.VideoWriter('output2.avi', cv2.VideoWriter_fourcc(*"XVID"), 5.0, (1920,1080))
start_x,start_y = 0,0

while(True):
    #Get color and gray frame
    frame = np.array(ImageGrab.grab())
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for(x, y, w, h) in faces:
        if ((start_x == 0 and start_y == 0) or ((abs(start_x-x) < 20) and (abs(start_y-y) < 20))):
            sub_image = frame_rgb[y:y+100, x:x+100]
            out1.write(sub_image)
            cv2.rectangle(frame_rgb, (x,y), (x+w, y+h), (255, 0, 0), 2)
            out2.write(frame_rgb)
            start_x, start_y = x, y
        else:
            break
        break
        
    #Loop duration
    print('Loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()