import cv2
import pandas as pd
from datetime import datetime
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
if os.path.exists('trainer.yml'):
    recognizer.read('trainer.yml')
else:
    print("[ERROR] trainer.yml not found!")
    exit()

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")

try:
    df_details = pd.read_csv('student_details.csv', dtype={'ID': str})
except Exception as e:
    df_details = None

attendance_list = [] 
cam = cv2.VideoCapture(1) 

blink_frames = 0
blink_detected = False
attendance_marked = False

while True:
    ret, img = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if len(faces) == 0:
        blink_detected = False
        blink_frames = 0

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+int(h/2), x:x+w] 
        eyes = eyeCascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=8, minSize=(20, 20))
        
        if len(eyes) == 0:
            blink_frames += 1
            cv2.putText(img, "Eyes: CLOSED", (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        else:
            cv2.putText(img, "Eyes: OPEN", (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            if 3 <= blink_frames <= 20: 
                blink_detected = True
            blink_frames = 0 
            
        if blink_detected:
            cv2.putText(img, "Blink: YES (LIVE)", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            id_num, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            
            if confidence < 45:
                search_id = str(id_num)
                name = "Unknown"
                course = "N/A"
                details = "CSV Error"
                
                if df_details is not None:
                    user_data = df_details[df_details['ID'] == search_id]
                    if not user_data.empty:
                        name = user_data.iloc[0]['Name']
                        course_name = user_data.iloc[0]['Course']
                        year = user_data.iloc[0]['Year']
                        
                      
                        course = f"{course_name} - {year}" 
                        details = course
                    else:
                        details = "Data not in CSV"
                
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(img, details, (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                now = datetime.now()
                time_str = now.strftime('%H:%M:%S')
                date_str = now.strftime('%d-%m-%Y')
               
                attendance_list.append([search_id, name, course, date_str, time_str])
                
                attendance_marked = True 
                
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(img, "WAITING FOR BLINK...", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow('Live Face Recognition', img)

    if attendance_marked:
        cv2.waitKey(1500)
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

if len(attendance_list) > 0:
    new_entries = pd.DataFrame(attendance_list, columns=['ID', 'Name', 'Course', 'Date', 'Time'])
    new_entries = new_entries.drop_duplicates(subset=['ID'], keep='first')
    try:
        old_data = pd.read_csv('Attendance_Log.csv', dtype={'ID': str})
        final_df = pd.concat([old_data, new_entries]).drop_duplicates(subset=['ID', 'Date'], keep='last')
    except:
        final_df = new_entries
    final_df.to_csv('Attendance_Log.csv', index=False) 
    print("\n[SUCCESS] Attendance log saved successfully!")