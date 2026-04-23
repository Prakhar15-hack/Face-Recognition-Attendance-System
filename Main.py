import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
import csv 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml') 
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

names = {} 
try:
    with open('student_details.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                names[int(row[0])] = row[1] 
except FileNotFoundError:
    print("[WARNING] student_details.csv .")

def markAttendance(name):
    if name == "Unknown": 
        return
        
    filename = 'attendance.csv'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Name,Time,Date\n')

    try:
        df = pd.read_csv(filename)
    except:
         with open(filename, 'w') as f:
            f.write('Name,Time,Date\n')
         df = pd.read_csv(filename)

    now = datetime.now()
    dateString = now.strftime('%Y-%m-%d')
    timeString = now.strftime('%H:%M:%S')

    attendance = df[(df['Name'] == name) & (df['Date'] == dateString)]
    
    if attendance.empty:
        with open(filename, 'a') as f:
            f.write(f'\n{name},{timeString},{dateString}')
        print(f" Attendance done: {name}")


cam = cv2.VideoCapture(0)
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

print("\n ")

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

    
        if (confidence < 55):
            
            name = names.get(id, "Unknown") 
        else:
            name = "Unknown"
            
     
        cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
        
        markAttendance(name)

    cv2.imshow('Face Recognition Attendance', img) 

    k = cv2.waitKey(10) & 0xff 
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()