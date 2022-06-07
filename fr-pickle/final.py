import face_recognition
import cv2
import numpy as np
import os
import pickle
import time

video_capture = cv2.VideoCapture(0)

sizes = [320, 120, 64]
sizecount = 0

pickle_file = "/home/pi/Desktop/facerecognitionsystem-backend/fr-pickle/pickle/datasets.pickle"
pickle_path = "/home/pi/Desktop/facerecognitionsystem-backend/fr-pickle/pickle/"
dataset_path = '/home/pi/Desktop/facerecognitionsystem-backend/fr-pickle/datasets'
users = os.listdir(dataset_path)
users.sort()

check = bool(os.listdir(pickle_path))


try:
    o = open(pickle_file, "rb")
    open_p= pickle.load(o)
    o.close()
    
except FileNotFoundError:
    o = open(pickle_file, "wb")
    o.write(pickle.dumps({"id": []}))
    o.close()
    o_r = open(pickle_file, "rb")
    open_p= pickle.load(o_r)
    o_r.close()
except EOFError:
    o = open(pickle_file, "wb")
    o.write(pickle.dumps({"id": []}))
    o.close()
    o_r = open(pickle_file, "rb")
    open_p= pickle.load(o_r)
    o_r.close()

# Create arrays of known face encodings and their names
known_id = open_p['id']
known_face_encodings = open_p['face']
known_face_names = open_p['name']

print(known_id)
print(known_face_encodings)
print(known_face_names)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

width = 1280
height = 360
new_size = (width, height) #Camera size for 2 cameras

while True:
    # Grab a single frame of video
    ret, img = video_capture.read()
    stretched = cv2.resize(img, new_size, interpolation = cv2.INTER_AREA)
    crop1 = stretched[:360, :640] #Crop the camera 1
    crop2 = stretched[:360, 640:1280]
    frame = cv2.rotate(crop1, cv2.cv2.ROTATE_90_CLOCKWISE)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    preview = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_id[best_match_index]

            face_names.append(name)

    #process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(preview, (left, top), (right, bottom), (0, 0, 255), 1)

        # Draw a label with a name below the face
        cv2.rectangle(preview, (left, bottom + 20), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(preview, name, (left + 6, bottom + 15), font, 0.5, (255, 255, 255), 1)
        print(name)
    # Display the resulting image
    cv2.namedWindow('Video', cv2.WINDOW_GUI_NORMAL|cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow('Video', 78, 182)
    cv2.imshow('Video', preview)



# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()