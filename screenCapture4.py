import numpy as np
import time
from PIL import ImageGrab
import cv2
import pytesseract
import imutils
from skimage import metrics


#Define the face cascade and timer
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# last_time = time.time()

#Tesseract location
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Define the codec and create VideoWriter object
first = True
outputs = []


while True:
    #Grab the frame
    frame = np.array(ImageGrab.grab())
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)              # the text is white
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(gray, kernel, iterations=1)           # thickened white lines
    negative = cv2.bitwise_not(dilated)
    ret, image_thresh = cv2.threshold(negative, 8, 255, cv2.THRESH_BINARY)

    ### Detecting names in the initial frame
    if first:
        height, width = image_thresh.shape
        boxes = pytesseract.image_to_data(image_thresh)
        names = []
        num_names = 0
        start_y, start_x = 0, 0
        for x,b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    x,y,w,h= int(b[6]),int(b[7]),int(b[8]),int(b[9])

                    cv2.rectangle(image_thresh,(x,y),(w+x, h+y),(0,0,255),2)
                    if len(b[11]) > 2 and w > h and w*h < 3000 and w*h > 50:
                        if len(names) == 0:
                            names.append(b[11])
                            face = frame_rgb[start_y-200:start_y, start_x:start_x+400]
                            out_name = names[-1] + ".avi"
                            outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (400, 200)))
                            outputs[num_names-1].write(face)
                            start_x, start_y = x, y
                            X,Y,W,H = x,y,w,h
                            num_names += 1
                        elif (abs((X+w)-x) < 75 and abs(Y-y) < 10):
                            names[num_names-1] = names[num_names-1] + b[11]
                            X,Y,W,H = x,y,w,h
                        else:
                            names.append(b[11])
                            face = frame_rgb[start_y-200:start_y, start_x:start_x+400]
                            out_name = names[-1] + ".avi"
                            outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (400, 200)))
                            outputs[num_names-1].write(face)
                            start_x, start_y = x, y
                            X,Y,W,H = x,y,w,h
                            num_names += 1
                        print(names)
        first = False

    #if first != True:


cv2.imshow('Image', frame_rgb[start_y-200:start_y, start_x:start_x+400])   
cv2.waitKey(0)