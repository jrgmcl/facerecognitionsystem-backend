import cv2
import numpy as np
import os

dataset_path = '/home/pi/Desktop/FACIALRECOGNITION/DATASETS'
users = os.listdir(dataset_path)
os.chdir("/home/pi/opencv/data/haarcascades")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Desktop/FACIALRECOGNITION/TRAINER/trainer.yml')
detector = cv2.CascadeClassifier("/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

#Generate the names on the dataset
dataset_path = '/home/pi/Desktop/FACIALRECOGNITION/DATASETS'
users = os.listdir(dataset_path)


#Put the user's name in array
first_name = ['Unknown']
last_name = ['Unknown']
for newdir in users:
    split_filename = newdir.split('.')
    first_name.append(split_filename[1])
    last_name.append(split_filename[2])

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 1280) #Camera Size
cam.set(4, 720)

width = 1280
height = 360
new_size = (width, height) #Camera size for 2 cameras

# Define min window size to be recognized as a face
minW = 640*0.4
minH = height*0.4

# Size for preview
preview_height = 640*0.5
preview_width = height*0.5

sizes = [448, 320, 128]
sizecount = 0
datacount = 0

faceSamples=[]
ids = []

for newdir in users:
    #Get Every user dataset directories
    user_dataset_path = os.path.join(dataset_path, newdir).replace("\\","/")
    raw_dataset_path = os.path.join(user_dataset_path, "RAW").replace("\\","/")
    list_image = os.listdir(raw_dataset_path)
    
    for imagePath in list_image:
        imageFPath = os.path.join(raw_dataset_path, imagePath).replace("\\","/")
        img = cv2.imread(imageFPath, 0)
        faces = detector.detectMultiScale(img, 1.05, 50)

        for (x,y,w,h) in faces:
            
            for threesizes in sizes:
                fsize = (threesizes, threesizes)
                resized = cv2.resize(img[y:y+h,x:x+w], fsize, interpolation = cv2.INTER_AREA)
                cv2.imwrite(user_dataset_path + '/' + newdir + '.' + str(sizecount) + str(datacount) + ".jpg", resized)
                print("\n [INFO] Converted " + imagePath + " to " + newdir + '.' + str(sizecount) + str(datacount) + ".jpg")
                sizecount += 1

            datacount += 1
            
        sizecount = 0
        if os.path.exists(imageFPath):
            os.remove(imageFPath)
            
    datacount = 0
    
                
print ("\n [INFO] Conversion completed. Generating 'Trainer.yml'...")

def getImagesAndLabels(dataset_path):

    #list_image = os.listdir(user_dataset_path)
    for newdir in users:
        user_dataset_path = os.path.join(dataset_path, newdir).replace("\\","/")
        list_image = os.listdir(user_dataset_path)
        list_image.remove("RAW")
        for imagePath in list_image:
            imageFPath = os.path.join(user_dataset_path, imagePath).replace("\\","/")

            #print(imageFPath)
            img = cv2.imread(imageFPath, 0)
            img_numpy = np.array(img, 'uint8')
            split_filename = newdir.split('.')
            id = int(split_filename[0].lstrip('0'))
            faces = detector.detectMultiScale(img_numpy)
            
#             for (x,y,w,h) in faces:
#                 faceSamples.append(img_numpy[y:y+h,x:x+w])
#                 ids.append(id)
            faceSamples.append(img_numpy)
            ids.append(id)
   
    return faceSamples, ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, ids = getImagesAndLabels(dataset_path)
recognizer.train(faces, np.array(ids))
recognizer.save('/TRAINER/trainer.yml')
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))


while True:
    ret, raw =cam.read()
    stretched = cv2.resize(raw, new_size, interpolation = cv2.INTER_AREA) #Set the new size
    crop1 = stretched[:360, :640] #Crop the camera 1
    crop2 = stretched[:360, 640:1280]
    
    img = cv2.rotate(crop1, cv2.cv2.ROTATE_90_CLOCKWISE) # Flip vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Preview
    preview_cam = cv2.resize(gray, (int(preview_width), int(preview_height)), interpolation = cv2.INTER_AREA)
    
    faces = detector.detectMultiScale(
        gray,
        scaleFactor = 1.11,
        minNeighbors = 20,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        x = int(x * 0.5)
        y = int(y * 0.5)
        w = int(w * 0.5)
        h = int(h * 0.5)
        cv2.rectangle(preview_cam, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = first_name[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = first_name[0]
            confidence = "  {0}%".format(round(100 - confidence))

    cv2.namedWindow('camera0', cv2.WINDOW_GUI_NORMAL|cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow('camera0', 78, 182)
    cv2.imshow('camera0', preview_cam)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()