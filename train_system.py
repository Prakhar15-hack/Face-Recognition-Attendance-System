import cv2
import os
import numpy as np
from PIL import Image


path = 'Student_Data/Year 3/sem 6'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):
    
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.png', '.jpeg'))]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') 
        img_numpy = np.array(PIL_img, 'uint8')

        try:
            id = int(os.path.split(imagePath)[-1].split(".")[0])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        except Exception as e:
            print(f"Error processing {imagePath}: {e}")

    return faceSamples, ids

print("\n ")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))


if not os.path.exists('trainer'):
    os.makedirs('trainer')

recognizer.write('trainer/trainer.yml') 
print(f"\n [INFO] {len(np.unique(ids))} ")