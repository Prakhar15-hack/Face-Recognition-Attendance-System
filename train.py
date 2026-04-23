import cv2
import numpy as np
from PIL import Image
import os


path = 'Student_Data/Year 3/sem 6'


recognizer = cv2.face.LBPHFaceRecognizer_create()

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    print("\n wait")

    for imagePath in imagePaths:
        
        try:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            
            
            id = int(os.path.split(imagePath)[-1].split(".")[0])
            print(f"  ID: {id} | Photo: {imagePath}")
            
            
            faceSamples.append(img_numpy)
            ids.append(id)
            
        except Exception as e:
            print(f"Skipping file: {imagePath} due to error: {e}")
            continue

    return faceSamples,ids

print ("\n Reading")
faces,ids = getImagesAndLabels(path)

print(f"\n {len(faces)} ")

recognizer.train(faces, np.array(ids))

recognizer.write('trainer.yml') 

print(f"\n [INFO] Success! {len(np.unique(ids))} ")
print(" triner file ready !")