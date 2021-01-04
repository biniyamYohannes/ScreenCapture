import numpy as np
from PIL import ImageGrab
import cv2
import time
import imutils
from skimage import metrics

#Define the face cascade and timer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
last_time = time.time()

# Define the codec and create VideoWriter object
first = True
num_faces = 0
frame_num = 0
outputs = []
init_faces = []


while True:
    #Grag the frame
    frame = np.array(ImageGrab.grab())
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #Find faces in the initial frame
    if first:
        for(x, y, w, h) in faces:
            face = frame_rgb[y:y+100, x:x+100]
            init_faces.append(face)
            out_name = "output" + str(num_faces+1) + ".avi"
            outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (100, 100)))
            outputs[num_faces].write(face)
            num_faces += 1
            frame_num += 1
            first = False
        print("I got here!")
        continue


    for(x, y, w, h) in faces:
        #print("Comparison loop.")
        found = False
        face = frame_rgb[y:y+100, x:x+100]
        #encoded_face = face_recognition.face_encodings(face)[0]
        for i in range(len(init_faces)):
            similarity = metrics.structural_similarity(face, init_faces[i], multichannel=True)
            print(i, similarity)
            if similarity > 0.5:                                 # if one of the faces on the current frame matches a face we already know
                outputs[i].write(face)                          # add a frame to the corresponding output file
                init_faces[i] = face
                found = True
                break                                           # just to be sure we don't match more than one face
        """
        if found == False:
            init_faces.append(face)
            out_name = "output" + str(num_faces+1) + ".avi"
            outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (100, 100)))
            outputs[num_faces].write(face)
            num_faces += 1
        """
    #Loop duration
    print('Loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()