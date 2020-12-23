import numpy as np
from PIL import ImageGrab
import cv2
import time

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self,c):
         #initialize the shape name and approximate the contour
        shape = 'unindentified'
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.0000000001*peri, True)

         #if the shape has 4 vertices it is a rectangle
        if len(approx) == 4:
            #compute the bounding box of the contour and use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if ar <= 0.95 or ar >= 1.05:
                shape = 'person'
        return shape

import imutils

#Define the face cascade and timer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
last_time = time.time()

# Define the codec and create VideoWriter object
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*"XVID"), 5.0, (1920,1080))

while(True):
    #Get color and gray frame
    frame = np.array(ImageGrab.grab())
    resized = imutils.resize(frame, width=1600)
    ratio = frame.shape[0] / float(resized.shape[0])

    #blur the reiszed grayscale frame and threshold it
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3,3), 0)
    sharp = cv2.addWeighted(gray,4.0,blurred,-2.0,0)
    thresh = cv2.threshold(sharp, 0, 255, cv2.THRESH_BINARY)[1]

    #find contours in the thresholded frame and initialize the shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    
    for c in cnts:
        #compute the center of the contour then detect the name of the shapeusing the contour
        M = cv2.moments(c)
        if cv2.contourArea(c) < 3000:
            continue

        shape = sd.detect(c)
        #if shape != 'person':
        #    continue

        if M["m00"] != 0:
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
        else:
            cX = 10
            cY = 10

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
        
        # show the output image
        #cv2.imshow("Image", gray)
        out.write(frame)

        #Check for key press
        if cv2.waitKey(25) & 0xFF == ord('q'):
            out.release()
            cv2.destroyAllWindows()
            break

    #Loop duration
    #print('Loop took {} seconds'.format(time.time() - last_time))
    #last_time = time.time()
    
    #Write the frame to a file
    #out.write(frame_rgb)

    #Detect faces
    #faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    #for(x, y, w, h) in faces:
    #    cv2.rectangle(gray, (x,y), (x+w, y+h), (255, 0, 0), 2)

    #Show the frames
    #cv2.imshow('window', gray)

    #Check for key press
    #if cv2.waitKey(25) & 0xFF == ord('q'):
    #    out.release()
    #    cv2.destroyAllWindows()
    #    break


"""
#Define the face cascade and timer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
last_time = time.time()

# Define the codec and create VideoWriter object
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*"XVID"), 10.0, (1920,1080))

while(True):
    #Get color and gray frame
    frame = np.array(ImageGrab.grab())
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Loop duration
    print('Loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()
    
    #Write the frame to a file
    out.write(frame_rgb)

    #Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for(x, y, w, h) in faces:
        cv2.rectangle(gray, (x,y), (x+w, y+h), (255, 0, 0), 2)

    #Show the frames
    #cv2.imshow('window', gray)

    #Check for key press
    #if cv2.waitKey(25) & 0xFF == ord('q'):
    #    out.release()
    #    cv2.destroyAllWindows()
    #    break
"""