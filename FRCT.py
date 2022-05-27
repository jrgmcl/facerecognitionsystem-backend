import cv2
import os
import numpy as np
#from PIL import Image

dataset_path = '/home/pi/Desktop/facerecognitionsystem-backend/datasets'
users = os.listdir(dataset_path)

os.chdir("/home/pi/opencv/data/haarcascades")
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

sizes = [320, 120, 64]
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
    index = 0
    #list_image = os.listdir(user_dataset_path)
    for newdir in users:
        user_dataset_path = os.path.join(dataset_path, newdir).replace("\\","/")
        list_image = os.listdir(user_dataset_path)
        list_image.remove("RAW")

        split_filename = newdir.split('.')
        id = int(split_filename[0])

        for imagePath in list_image:
            imageFPath = os.path.join(user_dataset_path, imagePath).replace("\\","/")
            #print(imageFPath)
            img = cv2.imread(imageFPath, 0)
            img_numpy = np.array(img, 'uint8')
            
#            faces = detector.detectMultiScale(img_numpy)
            
#             for (x,y,w,h) in faces:
#                 faceSamples.append(img_numpy[y:y+h,x:x+w])
#                 ids.append(id)
            faceSamples.insert(index, img_numpy)
            ids.insert(index, id)
            index += 1
   
    return faceSamples, ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, ids = getImagesAndLabels(dataset_path)
recognizer.train(faces, np.array(ids))
recognizer.save('/home/pi/Desktop/facerecognitionsystem-backend/TRAINER/trainer.yml')
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
print(ids)


