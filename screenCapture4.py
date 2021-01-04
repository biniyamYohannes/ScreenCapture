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