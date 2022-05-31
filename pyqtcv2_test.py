#Delete "from PyQt5.QtGui import QPixmap"
#Delete "from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread"
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import datetime
import os
import sys
import cv2
import MySQLdb
import pickle
import face_recognition
from images import rsrc
import serial


#Connect to Database
db = MySQLdb.connect("localhost",   #Host 
                     "phpmyadmin",  #Username
                     "frpi",       #Password
                     "fr")   #Database
cur = db.cursor()

    
#Get Date & Time before starting the application
dt = datetime.datetime.now()

d_name1 = "Name"
d_name2 = "Name"
d_course1 = "Course"
d_course2 = "Course"
d_temp1 = "Temperature"
d_status1 = "No registered user recognized!"
d_status2 = "No registered user recognized!"

class VideoThread0(QThread):
        change_pixmap_signal2 = pyqtSignal(np.ndarray)

class VideoThread(QThread):
    #Declare elements should be updated
    change_pixmap_signal1 = pyqtSignal(np.ndarray)
    change_pixmap_signal2 = pyqtSignal(np.ndarray)
    signal_name1 = pyqtSignal(str)
    signal_name2 = pyqtSignal(str)
    signal_course1 = pyqtSignal(str)
    signal_course2 = pyqtSignal(str)
    signal_temp1 = pyqtSignal(float)
    signal_status1 = pyqtSignal(str)
    signal_status2 = pyqtSignal(str)

    def run(self):
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
        known_face_encodings = []
        known_face_names = []

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
                                                        
                                                        known_id.append(user_id)
                                                        known_face_names.append(name)
                                                        known_face_encodings.append(img_encoding)
                                                
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
                                                        
                                                        known_id.append(user_id)
                                                        known_face_names.append(name)
                                                        known_face_encodings.append(img_encoding)
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
                                        
                                        known_id.append(user_id)
                                        known_face_names.append(name)
                                        known_face_encodings.append(img_encoding)
                                        
                                datacount = 0
                        
                insert_to_pickle = {"id": known_id, "name": known_face_names, "face": known_face_encodings}
                p = open(pickle_file, "wb")
                p.write(pickle.dumps(insert_to_pickle))
                p.close()
                o_p = open(pickle_file, "rb")
                open_p= pickle.load(o_p)
                o_p.close()
        else:
                known_id = open_p['id']
                known_face_encodings = open_p['face']
                known_face_names = open_p['name']


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
                                        cur.execute("SELECT * FROM rgstrd_users WHERE id = " + str(name) + ";")
                                        row = cur.fetchone()
                                        d_name1 = (row[1], row[2])
                                        d_course1 = row[4]
                                        

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
                        d_name1 = name
                        print(name)

                # Display the resulting image
                cv2.namedWindow('Video', cv2.WINDOW_GUI_NORMAL|cv2.WINDOW_AUTOSIZE)
                cv2.moveWindow('Video', 78, 182)
                cv2.imshow('Video', preview)    
            
        self.signal_name1.emit(d_name1)
        self.signal_course1.emit(d_course1)
        self.signal_status1.emit(d_status1)


        #self.signal_course2.emit(d_course2)
        #self.signal_temp1.emit(d_temp1)
            

        if ret:
                self.change_pixmap_signal1.emit(preview)
                #self.change_pixmap_signal2.emit(cv_img2)


class App(QWidget):
    def __init__(self):
        
        super().__init__()
        
        self.setObjectName("MainWindow")
        self.resize(1200, 1024)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(1200, 1024))
        self.setMaximumSize(QtCore.QSize(1200, 1024))
        self.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.setAutoFillBackground(False)
        
        #Initialize Shadows
        shadow1 = QGraphicsDropShadowEffect()
        shadow2 = QGraphicsDropShadowEffect()
        shadow3 = QGraphicsDropShadowEffect()
        shadow4 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(15)
        shadow2.setBlurRadius(15)
        shadow3.setBlurRadius(15)
        shadow4.setBlurRadius(15)
        
        #1st Background
        font = QtGui.QFont()
        font.setFamily("System")
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.screen0 = QtWidgets.QWidget(self.centralwidget)
        self.screen0.setGeometry(QtCore.QRect(0, 0, 600, 1024))
        self.screen0.setObjectName("screen0")
        self.bg = QtWidgets.QGraphicsView(self.screen0)
        self.bg.setGeometry(QtCore.QRect(0, 0, 600, 1024))
        self.bg.setMaximumSize(QtCore.QSize(600, 1024))
        self.bg.setMouseTracking(False)
        self.bg.setAutoFillBackground(False)
        self.bg.setStyleSheet("background-image: url(:/bg/resizedbg.jpg);\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg.setForegroundBrush(brush)
        self.bg.setObjectName("bg")
        
        #1st Frame
        self.frame0 = QtWidgets.QFrame(self.screen0)
        self.frame0.setGeometry(QtCore.QRect(40, 134, 520, 850))
        self.frame0.setStyleSheet("border-radius: 25px;\n"
"")
        self.frame0.setFrameShape(QtWidgets.QFrame.Box)
        self.frame0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame0.setLineWidth(2)
        self.frame0.setMidLineWidth(0)
        self.frame0.setObjectName("frame0")
        self.frame0.setGraphicsEffect(shadow1)
        
        #Face Recognition Title on the 1st Frame
        self.fr_title = QtWidgets.QLabel(self.frame0)
        self.fr_title.setGeometry(QtCore.QRect(10, 10, 520, 50))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.fr_title.setFont(font)
        self.fr_title.setMouseTracking(True)
        self.fr_title.setStyleSheet("")
        #self.fr_title.setTextFormat(QtCore.Qt.RichText)
        #self.fr_title.setScaledContents(False)
        self.fr_title.setAlignment(QtCore.Qt.AlignCenter)
        self.fr_title.setWordWrap(False)
        self.fr_title.setObjectName("fr_title")
        
        #Camera shape on the 1st Frame
        self.camera_0 = QtWidgets.QGraphicsView(self.frame0)
        self.camera_0.setGeometry(QtCore.QRect(40, 80, 180, 320))
        self.camera_0.setStyleSheet("background-color: rgb(129, 129, 129);\n"
"border-radius: 0px;")
        self.camera_0.setObjectName("camera_0")
        
        
        self.bg_0 = QtWidgets.QGraphicsView(self.frame0)
        self.bg_0.setGeometry(QtCore.QRect(0, 0, 520, 850))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg_0.sizePolicy().hasHeightForWidth())
        self.bg_0.setSizePolicy(sizePolicy)
        self.bg_0.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_0.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_0.setForegroundBrush(brush)
        self.bg_0.setObjectName("bg_0")
        
        #Name Label on the 1st Frame "name"
        self.name = QtWidgets.QLabel(self.frame0)
        self.name.setGeometry(QtCore.QRect(260, 180, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(8)
        self.name.setFont(font)
        self.name.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.name.setObjectName("name")
        
        #QR Description on the 1st Frame "qr_descript
        self.qr_descrip = QtWidgets.QLabel(self.frame0)
        self.qr_descrip.setGeometry(QtCore.QRect(50, 510, 421, 81))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.qr_descrip.setFont(font)
        self.qr_descrip.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:9pt; font-weight:600; color:#ffffff;\">DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION </span></p></body></html>")
        self.qr_descrip.setWordWrap(True)
        self.qr_descrip.setIndent(0)
        self.qr_descrip.setObjectName("qr_descrip")
        
        #QR Shape on the 1st Frame "qr"
        self.qr = QtWidgets.QGraphicsView(self.frame0)
        self.qr.setGeometry(QtCore.QRect(160, 600, 200, 200))
        self.qr.setStyleSheet("background-color: rgb(131, 131, 131);")
        self.qr.setObjectName("qr")
        
        self.bg_1 = QtWidgets.QGraphicsView(self.frame0)
        self.bg_1.setGeometry(QtCore.QRect(0, 425, 520, 425))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg_1.sizePolicy().hasHeightForWidth())
        self.bg_1.setSizePolicy(sizePolicy)
        self.bg_1.setStyleSheet("background-color: rgb(93, 177, 185);\n"
"\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_1.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_1.setForegroundBrush(brush)
        self.bg_1.setObjectName("bg_1")
        self.bg_11 = QtWidgets.QGraphicsView(self.frame0)
        self.bg_11.setGeometry(QtCore.QRect(0, 425, 520, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg_11.sizePolicy().hasHeightForWidth())
        self.bg_11.setSizePolicy(sizePolicy)
        self.bg_11.setStyleSheet("background-color: rgb(93, 177, 185);\n"
"border-radius: 0px;\n"
"\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_11.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_11.setForegroundBrush(brush)
        self.bg_11.setObjectName("bg_11")
        
        #Course Label on the 1st Frame "course"
        self.course = QtWidgets.QLabel(self.frame0)
        self.course.setGeometry(QtCore.QRect(260, 220, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.course.setFont(font)
        self.course.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.course.setObjectName("course")
        
        #Temperature Label on the 1st Frame "temp"
        self.temp = QtWidgets.QLabel(self.frame0)
        self.temp.setGeometry(QtCore.QRect(260, 260, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.temp.setFont(font)
        self.temp.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.temp.setObjectName("temp")
        
        #QR Title on the 1st Frame
        self.qr_title = QtWidgets.QLabel(self.frame0)
        self.qr_title.setGeometry(QtCore.QRect(0, 460, 520, 50))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.qr_title.setFont(font)
        self.qr_title.setMouseTracking(True)
        self.qr_title.setStyleSheet("")
        self.qr_title.setTextFormat(QtCore.Qt.RichText)
        self.qr_title.setScaledContents(False)
        self.qr_title.setAlignment(QtCore.Qt.AlignCenter)
        self.qr_title.setWordWrap(False)
        self.qr_title.setObjectName("qr_title")
        
        #Status Label on the 1st Frame "status"
        self.status = QtWidgets.QLabel(self.frame0)
        self.status.setGeometry(QtCore.QRect(260, 315, 220, 70))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.status.setFont(font)
        self.status.setStyleSheet("background-color: rgba(255, 0, 2, 75);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.status.setObjectName("status")
        
        #Instruction on the 1st Frame "instruct"
        self.instruct = QtWidgets.QLabel(self.frame0)
        self.instruct.setGeometry(QtCore.QRect(260, 80, 220, 80))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(8)
        self.instruct.setFont(font)
        self.instruct.setStyleSheet("background-color: rgba(0, 255, 0, 50);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.instruct.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Please position your face on the middle of the camera!</span></p></body></html>")
        self.instruct.setScaledContents(False)
        self.instruct.setAlignment(QtCore.Qt.AlignCenter)
        self.instruct.setWordWrap(True)
        self.instruct.setObjectName("instruct")
        
        self.bg_0.raise_()
        self.bg_11.raise_()
        self.bg_1.raise_()
        self.fr_title.raise_()
        self.camera_0.raise_()
        self.name.raise_()
        self.qr_descrip.raise_()
        self.qr.raise_()
        self.course.raise_()
        self.temp.raise_()
        self.qr_title.raise_()
        self.status.raise_()
        self.instruct.raise_()
        
        #1st Date & Time frame
        self.datetime = QtWidgets.QWidget(self.screen0)
        self.datetime.setGeometry(QtCore.QRect(40, 20, 520, 94))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.datetime.setFont(font)
        self.datetime.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
"border-radius: 25px;\n"
"")
        self.datetime.setObjectName("datetime")
        self.datetime.setGraphicsEffect(shadow2)
        
        self.Date = QtWidgets.QLabel(self.datetime)
        self.Date.setGeometry(QtCore.QRect(160, 10, 200, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.Date.setFont(font)
        self.Date.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.Date.setAlignment(QtCore.Qt.AlignCenter)
        self.Date.setObjectName("Date")
        self.Time = QtWidgets.QLabel(self.datetime)
        self.Time.setGeometry(QtCore.QRect(160, 35, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.Time.setFont(font)
        self.Time.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.Time.setAlignment(QtCore.Qt.AlignCenter)
        self.Time.setObjectName("Time")
        self.Logo = QtWidgets.QFrame(self.screen0)
        self.Logo.setGeometry(QtCore.QRect(-3, -14, 160, 160))
        self.Logo.setAutoFillBackground(False)
        self.Logo.setStyleSheet("\n"
"image: url(:/logo/logo.png);\n"
"")
        self.Logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Logo.setObjectName("Logo")
        self.screen1 = QtWidgets.QWidget(self.centralwidget)
        self.screen1.setGeometry(QtCore.QRect(600, 0, 600, 1024))
        self.screen1.setObjectName("screen1")
        self.bg_2 = QtWidgets.QGraphicsView(self.screen1)
        self.bg_2.setGeometry(QtCore.QRect(0, 0, 600, 1024))
        self.bg_2.setMaximumSize(QtCore.QSize(600, 1024))
        self.bg_2.setMouseTracking(False)
        self.bg_2.setAutoFillBackground(False)
        self.bg_2.setStyleSheet("background-image: url(:/bg/resizedbg.jpg);\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_2.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_2.setForegroundBrush(brush)
        self.bg_2.setObjectName("bg_2")
        self.Logo_2 = QtWidgets.QFrame(self.screen1)
        self.Logo_2.setGeometry(QtCore.QRect(-3, -14, 160, 160))
        self.Logo_2.setAutoFillBackground(False)
        self.Logo_2.setStyleSheet("\n"
"image: url(:/logo/logo.png);\n"
"")
        self.Logo_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Logo_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Logo_2.setObjectName("Logo_2")
        
        #2nd Frame
        self.frame0_2 = QtWidgets.QFrame(self.screen1)
        self.frame0_2.setGeometry(QtCore.QRect(40, 134, 520, 850))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setBold(True)
        font.setWeight(75)
        self.frame0_2.setFont(font)
        self.frame0_2.setStyleSheet("border-radius: 25px;\n"
"")
        self.frame0_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame0_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame0_2.setLineWidth(2)
        self.frame0_2.setMidLineWidth(0)
        self.frame0_2.setObjectName("frame0_2")
        self.frame0_2.setGraphicsEffect(shadow3)
        
        self.fr_title_2 = QtWidgets.QLabel(self.frame0_2)
        self.fr_title_2.setGeometry(QtCore.QRect(0, 10, 520, 50))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.fr_title_2.setFont(font)
        self.fr_title_2.setMouseTracking(True)
        self.fr_title_2.setStyleSheet("")
        self.fr_title_2.setTextFormat(QtCore.Qt.RichText)
        self.fr_title_2.setScaledContents(False)
        self.fr_title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.fr_title_2.setWordWrap(False)
        self.fr_title_2.setObjectName("fr_title_2")
        self.camera_1 = QtWidgets.QGraphicsView(self.frame0_2)
        self.camera_1.setGeometry(QtCore.QRect(40, 80, 180, 320))
        self.camera_1.setStyleSheet("background-color: rgb(129, 129, 129);\n"
"border-radius: 0px;")
        self.camera_1.setObjectName("camera_1")
        self.bg_3 = QtWidgets.QGraphicsView(self.frame0_2)
        self.bg_3.setGeometry(QtCore.QRect(0, 0, 520, 850))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg_3.sizePolicy().hasHeightForWidth())
        self.bg_3.setSizePolicy(sizePolicy)
        self.bg_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_3.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_3.setForegroundBrush(brush)
        self.bg_3.setObjectName("bg_3")
        self.name_2 = QtWidgets.QLabel(self.frame0_2)
        self.name_2.setGeometry(QtCore.QRect(260, 180, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(8)
        self.name_2.setFont(font)
        self.name_2.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.name_2.setObjectName("name_2")
        self.qr_descrip_2 = QtWidgets.QLabel(self.frame0_2)
        self.qr_descrip_2.setGeometry(QtCore.QRect(50, 510, 421, 81))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.qr_descrip_2.setFont(font)
        self.qr_descrip_2.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:9pt; font-weight:600; color:#ffffff;\">DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION </span></p></body></html>")
        self.qr_descrip_2.setWordWrap(True)
        self.qr_descrip_2.setIndent(0)
        self.qr_descrip_2.setObjectName("qr_descrip_2")
        self.qr_2 = QtWidgets.QGraphicsView(self.frame0_2)
        self.qr_2.setGeometry(QtCore.QRect(160, 600, 200, 200))
        self.qr_2.setStyleSheet("background-color: rgb(131, 131, 131);")
        self.qr_2.setObjectName("qr_2")
        self.bg_4 = QtWidgets.QGraphicsView(self.frame0_2)
        self.bg_4.setGeometry(QtCore.QRect(0, 425, 520, 425))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg_4.sizePolicy().hasHeightForWidth())
        self.bg_4.setSizePolicy(sizePolicy)
        self.bg_4.setStyleSheet("background-color: rgb(93, 177, 185);\n"
"\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_4.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_4.setForegroundBrush(brush)
        self.bg_4.setObjectName("bg_4")
        self.bg_12 = QtWidgets.QGraphicsView(self.frame0_2)
        self.bg_12.setGeometry(QtCore.QRect(0, 425, 520, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg_12.sizePolicy().hasHeightForWidth())
        self.bg_12.setSizePolicy(sizePolicy)
        self.bg_12.setStyleSheet("background-color: rgb(93, 177, 185);\n"
"border-radius: 0px;\n"
"\n"
"")
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_12.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.bg_12.setForegroundBrush(brush)
        self.bg_12.setObjectName("bg_12")
        self.course_2 = QtWidgets.QLabel(self.frame0_2)
        self.course_2.setGeometry(QtCore.QRect(260, 220, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.course_2.setFont(font)
        self.course_2.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.course_2.setObjectName("course_2")
        
    
        self.qr_title_2 = QtWidgets.QLabel(self.frame0_2)
        self.qr_title_2.setGeometry(QtCore.QRect(0, 460, 520, 50))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.qr_title_2.setFont(font)
        self.qr_title_2.setMouseTracking(True)
        self.qr_title_2.setStyleSheet("")
        self.qr_title_2.setTextFormat(QtCore.Qt.RichText)
        self.qr_title_2.setScaledContents(False)
        self.qr_title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.qr_title_2.setWordWrap(False)
        self.qr_title_2.setObjectName("qr_title_2")
        self.status_2 = QtWidgets.QLabel(self.frame0_2)
        self.status_2.setGeometry(QtCore.QRect(260, 315, 220, 70))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.status_2.setFont(font)
        self.status_2.setStyleSheet("background-color: rgba(255, 0, 2, 75);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.status_2.setObjectName("status_2")
        self.instruct_2 = QtWidgets.QLabel(self.frame0_2)
        self.instruct_2.setGeometry(QtCore.QRect(260, 80, 220, 80))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(8)
        self.instruct_2.setFont(font)
        self.instruct_2.setStyleSheet("background-color: rgba(0, 255, 0, 50);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.instruct_2.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Please position your face on the middle of the camera!</span></p></body></html>")
        self.instruct_2.setScaledContents(False)
        self.instruct_2.setAlignment(QtCore.Qt.AlignCenter)
        self.instruct_2.setWordWrap(True)
        self.instruct_2.setObjectName("instruct_2")
        self.bg_3.raise_()
        self.bg_4.raise_()
        self.fr_title_2.raise_()
        self.camera_1.raise_()
        self.name_2.raise_()
        self.qr_descrip_2.raise_()
        self.qr_2.raise_()
        self.bg_12.raise_()
        self.course_2.raise_()
        self.qr_title_2.raise_()
        self.status_2.raise_()
        self.instruct_2.raise_()
        
        #2nd Date & Time frame
        self.datetime_2 = QtWidgets.QWidget(self.screen1)
        self.datetime_2.setGeometry(QtCore.QRect(40, 20, 520, 94))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.datetime_2.setFont(font)
        self.datetime_2.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
"border-radius: 25px;\n"
"")
        self.datetime_2.setObjectName("datetime_2")
        self.datetime_2.setGraphicsEffect(shadow4)
        
        self.Date_2 = QtWidgets.QLabel(self.datetime_2)
        self.Date_2.setGeometry(QtCore.QRect(160, 10, 200, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.Date_2.setFont(font)
        self.Date_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.Date_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Date_2.setObjectName("Date_2")
        self.Time_2 = QtWidgets.QLabel(self.datetime_2)
        self.Time_2.setGeometry(QtCore.QRect(160, 35, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.Time_2.setFont(font)
        self.Time_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.Time_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Time_2.setObjectName("Time_2")
        self.bg_2.raise_()
        self.frame0_2.raise_()
        self.datetime_2.raise_()
        self.Logo_2.raise_()
        #self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        
        # create the label that holds the image
        self.camera1_view = QtWidgets.QLabel(self.frame0)
        self.camera2_view = QtWidgets.QLabel(self.frame0_2)
        #self.image_label.resize(180, 320)
        self.camera1_view.setGeometry(QtCore.QRect(40, 80, 180, 320))
        self.camera2_view.setGeometry(QtCore.QRect(40, 80, 180, 320))
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal1.connect(self.update_image1)
        self.thread.change_pixmap_signal2.connect(self.update_image2)

        # Connect to update texts
        self.thread.signal_name1.connect(self.update_name1)
        self.thread.signal_name2.connect(self.update_name2)
        self.thread.signal_course1.connect(self.update_course1)
        self.thread.signal_course2.connect(self.update_course2)
        self.thread.signal_temp1.connect(self.update_temp1)
        self.thread.signal_status1.connect(self.update_status1)
        self.thread.signal_status2.connect(self.update_status2)
        # start the thread
        self.thread.start()
        


    @pyqtSlot(np.ndarray)
    def update_image1(self, cv_img1):
        #Updates the image_label with a new opencv image
        qt_img1 = self.convert_cv_qt1(cv_img1)
        self.camera1_view.setPixmap(qt_img1)
        d_name1 = first_name[id] + " " + last_name[id]
        
    def update_image2(self, cv_img2):
        #Updates the image_label with a new opencv image
        qt_img2 = self.convert_cv_qt2(cv_img2)
        self.camera2_view.setPixmap(qt_img2)
    
    def convert_cv_qt1(self, cv_img1):
        #Convert from an opencv image to QPixmap
        rgb_image1 = cv2.cvtColor(cv_img1, cv2.COLOR_BGR2RGB)
        h1, w1, ch1 = rgb_image1.shape
        bytes_per_line1 = ch1 * w1
        convert_to_Qt_format1 = QtGui.QImage(rgb_image1.data, w1, h1, bytes_per_line1, QtGui.QImage.Format_RGB888)
        p1 = convert_to_Qt_format1.scaled(180, 320, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p1)
    
    def convert_cv_qt2(self, cv_img2):
        #Convert from an opencv image to QPixmap
        rgb_image2 = cv2.cvtColor(cv_img2, cv2.COLOR_BGR2RGB)
        h2, w2, ch2 = rgb_image2.shape
        bytes_per_line2 = ch2 * w2
        convert_to_Qt_format2 = QtGui.QImage(rgb_image2.data, w2, h2, bytes_per_line2, QtGui.QImage.Format_RGB888)
        p2 = convert_to_Qt_format2.scaled(180, 320, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p2)
    
    def update_name1(self, d_name1):
        #print ("TEST!")
        _translate = QtCore.QCoreApplication.translate
        self.name.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_name1) + "</span></p></body></html>"))
    def update_name2(self, d_name2):
        _translate = QtCore.QCoreApplication.translate
        self.name_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_name2) + "</span></p></body></html>"))
    def update_course1(self, d_course1):
        _translate = QtCore.QCoreApplication.translate
        self.course.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_course1) + "</span></p></body></html>"))
    def update_course2(self, d_course2):
        _translate = QtCore.QCoreApplication.translate
        self.course_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_course2) + "</span></p></body></html>"))
    def update_temp1(self, d_temp1):
        _translate = QtCore.QCoreApplication.translate
        self.temp.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_temp1) + "</span></p></body></html>"))
    def update_status1(self, d_status1):
        _translate = QtCore.QCoreApplication.translate
        self.status.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_status1) + "</span></p></body></html>"))
    def update_status2(self, d_status2):
        _translate = QtCore.QCoreApplication.translate
        self.status_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_status2) + "</span></p></body></html>"))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fr_title.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt;\">Face Recognition</span></p></body></html>"))
        
        #Labels on the 1st frame
        self.name.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_name1) + "</span></p></body></html>"))
        self.course.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_course1) + "</span></p></body></html>"))
        self.temp.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_temp1) + "</span></p></body></html>"))
        self.status.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_status1) + "</span></p></body></html>"))
        
        self.qr_title.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt; color:#ffffff;\">QR Code</span></p></body></html>"))
        
        
        #Date and Time on the 1st frame
        self.Date.setText(_translate("MainWindow", str(dt.strftime("%a, %m/%d/%y"))))
        self.Time.setText(_translate("MainWindow", str(dt.strftime("%I:%M%p"))))
        
        self.fr_title_2.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt;\">Face Recognition</span></p></body></html>"))
        
        #Labels on the 2nd frame
        self.name_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_name2) + "</span></p></body></html>"))
        self.course_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_course2) + "</span></p></body></html>"))
        self.status_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">" + str(d_status2) + "</span></p></body></html>"))
        
        self.qr_title_2.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt; color:#ffffff;\">QR Code</span></p></body></html>"))
        
        
        #Date and Time on the 2nd frame
        self.Date_2.setText(_translate("MainWindow", str(dt.strftime("%a, %m/%d/%y"))))
        self.Time_2.setText(_translate("MainWindow", str(dt.strftime("%I:%M%p"))))
        
    def update_label(self):
        #Update Date & Time every frame
        dt = datetime.datetime.now()
        self.Date.setText(str(dt.strftime("%a, %m/%d/%y")))
        self.Time.setText(str(dt.strftime("%I:%M%p")))
        self.Date_2.setText(str(dt.strftime("%a, %m/%d/%y")))
        self.Time_2.setText(str(dt.strftime("%I:%M%p")))

        
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    timer = QtCore.QTimer()
    timer.timeout.connect(a.update_label)
    timer.start()
    a.show()
    sys.exit(app.exec_())