import numpy as np
import time
from PIL import ImageGrab
import cv2
import pytesseract
import imutils
import jellyfish

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Some variables
outputs = []                # stores the VideoWriter objects
people = {}                 # stores the participant names and their corresponding indices
num_faces = 0               # number of participants recognized

# Loop over the video frames
while True:

    # Grab and process the frame
    frame = np.array(ImageGrab.grab())
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)              # the text is white
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(gray, kernel, iterations=1)                # thickened white lines
    negative = cv2.bitwise_not(dilated)
    ret, image_thresh = cv2.threshold(negative, 8, 255, cv2.THRESH_BINARY)

    # Extract names from the frame
    height, width = image_thresh.shape
    boxes = pytesseract.image_to_data(image_thresh)
    name = ''
    #print("I GOT HERE 1.")
    for x,b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                x,y,w,h= int(b[6]),int(b[7]),int(b[8]),int(b[9])
                string = b[11]
                
                # Get the full name and store the corresponding participant
                if len(string) > 2 and w > h and w*h < 3000 and w*h > 50:                   #Check if the string is a 'valid' word

                    # Get first word
                    if name == '':
                        name = string
                        start_x, start_y = x,y
                        X,Y,W,H = x,y,w,h
                        print("I GOT HERE 1.")
                    
                    # Check for the rest of a name
                    elif (abs((X+w)-x) < 75 and abs(Y-y) < 10):
                        name += string
                        X,Y,W,H = x,y,w,h
                        print("I GOT HERE 2.")
                    
                    # Store a complete name
                    else:
                        print("I GOT HERE 3.")
                        face = frame_rgb[start_y-200:start_y, start_x:start_x+400]

                        # Store the first name
                        if len(people) == 0 and len(name) > 5:
                            out_name = name + ".avi"
                            people[name] = num_faces
                            print(people[name])
                            outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (400, 200)))
                            outputs[num_faces].write(face)
                            num_faces += 1
                            name = string                                               # set name to the most recently detected string
                            start_x, start_y = x,y
                            X,Y,W,H = x,y,w,h

                        #Store other names (words) if they are at least 6 letters long
                        elif len(name) > 5 and num_faces < 50:
                            max_similarity = 0
                            max_similarity_index = 0
                            
                            for key in people.keys():                                   # find a person that matches the best
                                similarity = jellyfish.jaro_distance(name, key)
                                if similarity > max_similarity:
                                    max_similarity = similarity
                                    max_similarity_index = people[key]
                            print("The max similarity for this face is " + str(max_similarity) + " at index " + str(max_similarity_index))

                            if max_similarity > 0.8:                                   # the person is already on the list
                                try:
                                    outputs[max_similarity_index].write(face)
                                    name = string
                                    start_x, start_y = x,y
                                    X,Y,W,H = x,y,w,h
                                except:
                                    print("Something went wrong when trying to add frame to an existing file.")
                            else:                                                      # the person is not on the list
                                out_name = name + ".avi"
                                people[name] = num_faces
                                print(people[name])
                                outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (400, 200)))
                                outputs[num_faces].write(face)
                                num_faces += 1
                                name = string                                          # set name to the most recently detected string
                                start_x, start_y = x,y
                                X,Y,W,H = x,y,w,h



                                









