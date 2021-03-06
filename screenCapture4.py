import numpy as np
from PIL import ImageGrab
import cv2
import pytesseract
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
    gray = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)                                      # white text on black background
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(gray, kernel, iterations=1)                                       # thickened white lines
    negative = cv2.bitwise_not(dilated)                                                     # black text on white background
    ret, image_thresh = cv2.threshold(negative, 8, 255, cv2.THRESH_BINARY)

    # Extract names from the frame
    height, width = image_thresh.shape
    boxes = pytesseract.image_to_data(image_thresh)
    name = ''

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
                    
                    # Check for the rest of a name
                    elif (abs((X+w)-x) < 75 and abs(Y-y) < 10):
                        name += string
                        X,Y,W,H = x,y,w,h
                    
                    # Store a complete name
                    else:
                        face = frame_rgb[start_y-200:start_y, start_x:start_x+400]
                        name.replace("'", '')
                        name.replace('.','')
                        name.replace('-','')
                        print(name)

                        # Store the first name
                        if len(people) == 0 and len(name) > 5 and name[0].isupper() and name[1].isupper() == False:
                            out_name = name + ".avi"
                            people[name] = num_faces
                            outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (400, 200)))
                            outputs[num_faces].write(face)
                            num_faces += 1
                            name = string                                               # set name to the most recently detected string
                            start_x, start_y = x,y
                            X,Y,W,H = x,y,w,h

                        #Store other names (words) if they satisfy conditions
                        elif len(name) > 5 and name[0].isupper() and name[1].isupper() == False and num_faces < 50:           # can also check for letters only with isalpha() if everyone has only letters in their name   
                            max_similarity = 0
                            max_similarity_index = 0

                            for key in people.keys():                                   # find a person that matches the best
                                similarity = jellyfish.jaro_distance(name, key)
                                if similarity > max_similarity:
                                    max_similarity = similarity
                                    max_similarity_index = people[key]

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

                                outputs.append(cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*"XVID"), 5.0, (400, 200)))
                                outputs[num_faces].write(face)
                                num_faces += 1
                                name = string                                          # set name to the most recently detected string
                                start_x, start_y = x,y
                                X,Y,W,H = x,y,w,h