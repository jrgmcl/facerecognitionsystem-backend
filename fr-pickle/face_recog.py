import face_recognition
import cv2
import numpy as np
import os
import pickle
import time


cam = cv2.VideoCapture(0)

cam.set(3, 1280) #Camera Size
cam.set(4, 720)

width = 1280
height = 360
new_size = (width, height) #Camera size for 2 cameras


# Size for preview
preview_height = 640*0.5
preview_width = height*0.5

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
    
dataset_face_encodings = []
dataset_face_names = []
pickle_id = open_p["id"]

print(open_p)
print(check)
if check == False:
    #Every Folder
    for every_user in users:
        userimg_path = os.path.join(dataset_path, every_user).replace("\\","/")
        raw_userimg_path = os.path.join(userimg_path, "RAW").replace("\\","/")
        
        list_RAWimg = os.listdir(raw_userimg_path)
        list_RAWimg.sort()
        
        list_img = os.listdir(userimg_path)
        list_img.remove("RAW")
        append = bool(list_img)
        
        split_filename = every_user.split('.')
        name = str(split_filename[1]) + " " +str(split_filename[2])
        user_id =  split_filename[0]
        
        not_appendonly = bool(list_RAWimg)
        datacount = int(len(list_img)/3)
        
        if datacount > 0:
            datacount += 1
            
        if not_appendonly == True:
        #Every Image
            for everyuser_RAWimg in list_RAWimg:
                #print(everyuser_img)
                everyimg_path = os.path.join(raw_userimg_path, everyuser_RAWimg).replace("\\","/")
                
                #Read image
                if append == True:
                    for everyuser_img in list_img:
                        userimg_path = os.path.join(userimg_path, everyuser_img).replace("\\","/")
                        eachimg_file = face_recognition.load_image_file(userimg_path)
                        eachimgfaces = face_recognition.face_locations(eachimg_file)
                        img_encoding = face_recognition.face_encodings(eachimg_file, eachimgfaces)[0]
                        
                        pickle_id.append(user_id)
                        dataset_face_names.append(name)
                        dataset_face_encodings.append(img_encoding)
                        
                img_file = face_recognition.load_image_file(everyimg_path)
                faces = face_recognition.face_locations(img_file)
                
                for (top, right, bottom, left) in faces:
                    
                    #Every sizes
                    for threesizes in sizes:
                        fsize = (threesizes, threesizes)
                        img_output = cv2.resize(img_file[top:bottom, left:right], fsize, interpolation=cv2.INTER_AREA)
                        
                        
                        img_name = userimg_path + '/' + every_user + '.' + str(sizecount) + str(datacount) + ".jpg"
                        new_img_path = os.path.join(userimg_path, img_name).replace("\\","/")
                        cv2.imwrite(img_name, img_output)
                        
                        
                        eachimg_file = face_recognition.load_image_file(new_img_path)
                        eachimgfaces = face_recognition.face_locations(eachimg_file)
                        img_encoding = face_recognition.face_encodings(eachimg_file, eachimgfaces)[0]
                        
                        pickle_id.append(user_id)
                        dataset_face_names.append(name)
                        dataset_face_encodings.append(img_encoding)
                        sizecount += 1
                        
                        
                        
                    datacount += 1
                sizecount = 0
                if os.path.exists(everyimg_path):
                    os.remove(everyimg_path)
            
        else:
            for everyuser_img in list_img:
                usereachimg_path = os.path.join(userimg_path, everyuser_img).replace("\\","/")
                print (usereachimg_path)
                eachimg_file = face_recognition.load_image_file(usereachimg_path)
                eachimgfaces = face_recognition.face_locations(eachimg_file)
                img_encoding = face_recognition.face_encodings(eachimg_file, eachimgfaces)[0]
                
                pickle_id.append(user_id)
                dataset_face_names.append(name)
                dataset_face_encodings.append(img_encoding)
                    
        datacount = 0
        
    print(dataset_face_names)
    print(dataset_face_encodings)
    insert_to_pickle = {"id": pickle_id, "name": dataset_face_names, "face": dataset_face_encodings}
    p = open(pickle_file, "wb")
    p.write(pickle.dumps(insert_to_pickle))
    p.close()
    o_p = open(pickle_file, "rb")
    open_p= pickle.load(o_p)
    o_p.close()

else:
    p = open("/home/pi/Desktop/facerecognitionsystem-backend/fr-pickle/pickle/datasets.pickle", "rb")
    p.write(pickle.dumps(insert_to_pickle))
    p.close()
    
print(len(open_p["id"]))
print(len(open_p["name"]))
print(len(open_p["face"]))
          




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
            id = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(dataset_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                id = pickle_id[best_match_index]

            face_names.append(id)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), id in zip(face_locations, face_names):
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
        cv2.putText(img, id, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.namedWindow('camera0', cv2.WINDOW_GUI_NORMAL|cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow('camera0', 78, 182)
    cv2.imshow('camera0', img)


cam.release()
cv2.destroyAllWindows()
