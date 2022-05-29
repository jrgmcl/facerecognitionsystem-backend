import face_recognition
import cv2
import numpy as np
import os

cam = cv2.VideoCapture(0)

cam.set(3, 1280) #Camera Size
cam.set(4, 720)

width = 1280
height = 360
new_size = (width, height) #Camera size for 2 cameras


# Size for preview
preview_height = 640*0.5
preview_width = height*0.5

known_face_encodings = []
known_face_names = []

dataset_path = '/home/pi/Desktop/test/Advance-Face-Recognition--master/datasets'
users = os.listdir(dataset_path)
users.sort()
print(users)

for every_user in users:
    userimg_path = os.path.join(dataset_path, every_user).replace("\\","/")
    
    list_img = os.listdir(userimg_path)
    list_img.sort()
    print(list_img)
    for everyuser_img in list_img:
        #print(everyuser_img)
        everyimg_path = os.path.join(userimg_path, everyuser_img).replace("\\","/")
        print(everyimg_path)
        img_file = face_recognition.load_image_file(everyimg_path)
        img_encoding = face_recognition.face_encodings(img_file)[0]
        
        known_face_encodings.append(img_encoding)
        
        split_filename = every_user.split('.')
        name = str(split_filename[1]) + " " +str(split_filename[2])
        known_face_names.append(name)
        
print(known_face_names)
          




# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = cam.read()
    stretched = cv2.resize(frame, new_size, interpolation = cv2.INTER_AREA) #Set the new size
    crop1 = stretched[:360, :640] #Crop the camera 1
    crop2 = stretched[:360, 640:1280]
    
    img = cv2.rotate(crop1, cv2.cv2.ROTATE_90_CLOCKWISE) # Flip vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

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
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', img)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
cam.release()
cv2.destroyAllWindows()