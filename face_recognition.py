import cv2
import numpy as np
import os
import sqlite3
from PIL import ImageFont, ImageDraw, Image
import time
import AI_recognition
import threading
import time
from datetime import date
from datetime import datetime

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recoginzer/trainningData.yml")
def getProfile(id):
    conn = sqlite3.connect("D:\Python\product\data_student.db")
    query = "SELECT * FROM students WHERE ID="+ str(id)
    cursor = conn.execute(query)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile
cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX

def chatting(name, id, check):
    AI_recognition.chatting(name, id, check)

student_id = None
profile = None

def check_in(id):
    ngay_hom_nay = date.today()	
    ngay_bat_dau = ngay_hom_nay.strftime("%Y/%m/%d")
    print(ngay_hom_nay)
    conn = sqlite3.connect("D:\Python\product\data_student.db")
    query = "SELECT * FROM lesson WHERE id_hoc_sinh=" + "'" + str(id) + "'" + " and ngay_bat_dau=" + "'" + str(ngay_bat_dau) + "'"
    cusror = conn.execute(query)

    isRecordExist = 0
            
    for row in cusror:
        isRecordExist = 1
            
    if(isRecordExist == 1):
        CPU = "Today you have class at " + row[8] + " hours"
        gio_hoc = row[8].split(':', 1)
        now = datetime.now()
        gio_hien_tai = now.strftime("%H")
        if int(gio_hoc[0]) < int(gio_hien_tai):
            query = "UPDATE lesson SET tinh_trang = 1, hours_check_in = " + "'" + now.strftime("%H:%M") + "'" + " WHERE id=" + str(row[0])
            cusror = conn.execute(query)
            conn.commit()
    conn.close()
    if isRecordExist == 1:
        return row[8]
    else:
        return None

check = None
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 225, 0) , 2)
        roi_gray = gray[y:y + h, x: x + w]
        id,confidence = recognizer.predict(roi_gray)
        if confidence > 70:
            profile = getProfile(id)
            if(profile != None):
                cv2.putText(frame, ""+str(profile[1]), (x+ 10, y+h+ 30) ,cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                check = check_in(id)
        else:
            cv2.putText(frame, "", (x+ 10, y+h+ 30) , fontface, 1, (0,0, 255), 2)
    cv2.imshow('image', frame)
    if profile != None and profile[0] != student_id:
        student_id = profile[0]
        th = threading.Thread(target=chatting, args=[profile[1], profile[0], check])
        # Start the thread
        th.start()
    if(cv2.waitKey(1) == ord('e')):
        break;
    check = None
cap.release()
cv2.destroyAllWindows()
