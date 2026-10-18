import cv2
import numpy as np
import sqlite3
import os
from tkinter import *
from tkinter import messagebox
import time
import train_image

def saveImages(code):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    sampleNum = 0

    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(frame,(x, y),(x + w, y + h),(0, 255, 0), 2)
            
            if not os.path.exists("dataSet"):
                os.makedirs("dataSet")
            sampleNum += 1
            cv2.imwrite("dataSet/student." + str(sampleNum) + "." + str(code) + ".jpg", gray[y: y+h, x: x+w])
        cv2.imshow("Save image student", frame)
        cv2.waitKey(1)
        if sampleNum > 499:
            break
        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()
    return True

def insertOrUpdate():
    print(code_student.get())
    conn = sqlite3.connect("data_student.db")
    query = "SELECT * FROM students WHERE id=" + "'" + str(code_student.get()) + "'"
    cusror = conn.execute(query)
    isRecordExist = 0
    for row in cusror:
        isRecordExist = 1
    if(isRecordExist == 0):
        messagebox.showerror(
            title='Lỗi mã học sinh',
            message='Mã học sinh không tồn tại vui lòng kiểm tra lại!'
        )
    else:
        check = messagebox.askquestion(
            title='lưu ảnh',
            message='Bạn có chắc chắn muốn lưu ảnh học sinh ' + row[4] + '?'
        )
        print(check)
        if check == 'yes':
            save = saveImages(int(code_student.get()))
            if save:
                train_image.getImageWithCode()
    conn.execute(query)
    conn.commit()
    conn.close()

window = Tk()
window.title("Save student photo")
window.geometry('350x200')
global code_student
code_student = StringVar()
code_label = Label(window, text="Nhập id học sinh:", font=("Arial Bold", 12))
code_label.grid(column=0, row=0)
code_entry = Entry(window, textvariable = code_student)
code_entry.grid(column=1, row=0)
code_button = Button(window, text="Lưu Ảnh", command = insertOrUpdate, font=("Arial Bold", 12))
code_button.grid(column=0, row=1)

window.mainloop()


