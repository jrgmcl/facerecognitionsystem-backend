import os

dataset_path = '/home/pi/Desktop/FACIALRECOGNITION/DATASETS'
users = os.listdir(dataset_path)
sizes = [448, 320, 128]
count = 0

for newdir in users:
        #Get Every user dataset directories
        user_dataset_path = os.path.join(dataset_path, newdir).replace("\\","/")
        raw_dataset_path = os.path.join(user_dataset_path, "raw").replace("\\","/")
        list_image = os.listdir(raw_dataset_path)
        print (list_image)
        
        for imagePath in list_image:
            imageFPath = os.path.join(raw_dataset_path, imagePath).replace("\\","/")
            #print (imageFPath)
            
            
            for threesizes in sizes:
                    print("\n [INFO] Converted " + imagePath + " to " + newdir + '.' + str(count) + str(threesizes))
                    count += 1
