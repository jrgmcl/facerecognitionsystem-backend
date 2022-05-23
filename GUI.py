# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import datetime
import cv2
import numpy as np
import os
import sys

from images import image_source
from images import rsrc

dt = datetime.datetime.now()

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


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    def run(self):
        cam = cv2.VideoCapture(0)
        #Camera Size
        cam.set(3, 1280) 
        cam.set(4, 720)
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
                    print("\n [Recognized] " + str(id) + str(confidence))
                else:
                    id = first_name[0]
                    confidence = "  {0}%".format(round(100 - confidence))
            if ret:
                self.change_pixmap_signal.emit(preview_cam)
                
class Ui_MainWindow(QWidget):
        
    def __init__(self):
        super().__init__()
        #Shadows
        shadow0 = QGraphicsDropShadowEffect()
        shadow1 = QGraphicsDropShadowEffect()
        shadow2 = QGraphicsDropShadowEffect()
        shadow3 = QGraphicsDropShadowEffect()
        shadow0.setBlurRadius(25)
        shadow1.setBlurRadius(25)
        shadow2.setBlurRadius(25)
        shadow3.setBlurRadius(25)
        
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
        self.setStyleSheet("")
        self.setInputMethodHints(QtCore.Qt.ImhNone)
 
        #self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("System")
        font.setBold(True)
        font.setWeight(75)
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
        self.frame0 = QtWidgets.QFrame(self.screen0)
        self.frame0.setGeometry(QtCore.QRect(40, 134, 520, 850))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setBold(True)
        font.setWeight(75)
        self.frame0.setFont(font)
        self.frame0.setStyleSheet("border-radius: 25px;\n"
"")
        self.frame0.setFrameShape(QtWidgets.QFrame.Box)
        self.frame0.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame0.setLineWidth(2)
        self.frame0.setGraphicsEffect(shadow0)
        self.frame0.setMidLineWidth(0)
        self.frame0.setObjectName("frame0")
        self.fr_title = QtWidgets.QLabel(self.frame0)
        self.fr_title.setGeometry(QtCore.QRect(0, 10, 520, 50))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.fr_title.setFont(font)
        self.fr_title.setMouseTracking(True)
        self.fr_title.setStyleSheet("")
        self.fr_title.setTextFormat(QtCore.Qt.RichText)
        self.fr_title.setScaledContents(False)
        self.fr_title.setAlignment(QtCore.Qt.AlignCenter)
        self.fr_title.setWordWrap(False)
        self.fr_title.setObjectName("fr_title")
        
        
        #Camera
        self.camera_0 = QtWidgets.QLabel(self.frame0)
        self.camera_0.setGeometry(QtCore.QRect(40, 80, 180, 320))
        #self.camera_0.setStyleSheet("background-color: rgb(129, 129, 129);\n"
#"border-radius: 0px;")
        self.camera_0.setObjectName("camera_0")
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_video)
        self.thread.start()
        
        # create the label that holds the image
        self.image_label = QtWidgets.QLabel(self.frame0)
        self.image_label.resize(self.disply_width, self.display_height)
        self.image_label.setGeometry(QtCore.QRect(40, 80, 180, 320))
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        
        
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
        self.qr_descrip = QtWidgets.QLabel(self.frame0)
        self.qr_descrip.setGeometry(QtCore.QRect(50, 510, 421, 81))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.qr_descrip.setFont(font)
        self.qr_descrip.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:9pt; font-weight:600; color:#ffffff;\">DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION </span></p></body></html>")
        self.qr_descrip.setWordWrap(True)
        self.qr_descrip.setIndent(0)
        self.qr_descrip.setObjectName("qr_descrip")
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
        self.datetime = QtWidgets.QWidget(self.screen0)
        self.datetime.setGeometry(QtCore.QRect(40, 20, 520, 94))
        
        font = QtGui.QFont()
        font.setPointSize(16)
        self.datetime.setFont(font)
        self.datetime.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
"border-radius: 25px;\n"
"")
        self.datetime.setGraphicsEffect(shadow1)
        self.datetime.setObjectName("datetime")
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
        self.frame0_2 = QtWidgets.QFrame(self.screen1)
        self.frame0_2.setGeometry(QtCore.QRect(40, 134, 520, 850))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setBold(True)
        font.setWeight(75)
        self.frame0_2.setFont(font)
        self.frame0_2.setStyleSheet("border-radius: 25px;\n"
"")
        self.frame0_2.setGraphicsEffect(shadow2)
        self.frame0_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame0_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame0_2.setLineWidth(2)
        self.frame0_2.setMidLineWidth(0)
        self.frame0_2.setObjectName("frame0_2")
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
        self.temp_2 = QtWidgets.QLabel(self.frame0_2)
        self.temp_2.setGeometry(QtCore.QRect(260, 260, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        self.temp_2.setFont(font)
        self.temp_2.setStyleSheet("background-color: rgb(229, 229, 229);\n"
"border-style: solid;\n"
"border-radius: 10px;\n"
"")
        self.temp_2.setObjectName("temp_2")
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
        self.temp_2.raise_()
        self.qr_title_2.raise_()
        self.status_2.raise_()
        self.instruct_2.raise_()
        self.datetime_2 = QtWidgets.QWidget(self.screen1)
        self.datetime_2.setGeometry(QtCore.QRect(40, 20, 520, 94))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.datetime_2.setFont(font)
        self.datetime_2.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
"border-radius: 25px;\n"
"")
        self.datetime_2.setGraphicsEffect(shadow3)
        self.datetime_2.setObjectName("datetime_2")
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fr_title.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt;\">Face Recognition</span></p></body></html>"))
        self.name.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Jorge Michael Galang</span></p></body></html>"))
        self.course.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">&lt;Course&gt;</span></p></body></html>"))
        self.temp.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">&lt;Temperature&gt;</span></p></body></html>"))
        self.qr_title.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt; color:#ffffff;\">QR Code</span></p></body></html>"))
        self.status.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">No face detected!</span></p></body></html>"))
        self.Date.setText(_translate("MainWindow", str(dt.strftime("%a, %b %d, %Y"))))
        self.Time.setText(_translate("MainWindow", str(dt.strftime("%I:%M%p"))))
        self.fr_title_2.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt;\">Face Recognition</span></p></body></html>"))
        self.name_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Jorge Michael Galang</span></p></body></html>"))
        self.course_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">&lt;Course&gt;</span></p></body></html>"))
        self.temp_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">&lt;Temperature&gt;</span></p></body></html>"))
        self.qr_title_2.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat SemiBold\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Montserrat\'; font-size:28pt; color:#ffffff;\">QR Code</span></p></body></html>"))
        self.status_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">No face detected!</span></p></body></html>"))
        self.Date_2.setText(_translate("MainWindow", str(dt.strftime("%a, %b %d, %Y"))))
        self.Time_2.setText(_translate("MainWindow", str(dt.strftime("%I:%M%p"))))
        
    @pyqtSlot(np.ndarray)
    def update_video(self, raw):
        qt_img = self.convert_cv_qt(raw)
        self.camera_0.setPixmap(qt_img)
        
    def convert_cv_qt(self, preview_cam):
        h, w, ch = preview_cam.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(preview_cam, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(640, 360, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
        
    def update_label(self):
        dt = datetime.datetime.now()
        self.Date.setText(str(dt.strftime("%a, %b %d, %Y")))
        self.Time.setText(str(dt.strftime("%I:%M%p")))
        
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = Ui_MainWindow()
    a.show()
    sys.exit(app.exec_())
    
    
    
    
    
