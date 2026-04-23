import cv2
import os
import csv

if not os.path.exists('images'):
    os.makedirs('images')

cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n Enter Student ID ( e.g., 109): ')
face_name = input(' Enter Student Name: ') 

try:
    with open('student_details.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([face_id, face_name])
    print(f"\n [INFO]  Success! {face_name} of data saved in 'student_details.csv'!")
except Exception as e:
    print(f"\n  Error file banane mein: {e}")

print("smile")

count = 0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        
       
        cv2.imwrite("images/" + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 60:
         break

print("camera closed")
cam.release()
cv2.destroyAllWindows()