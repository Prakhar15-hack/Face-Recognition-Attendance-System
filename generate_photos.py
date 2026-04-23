import cv2
import os

path = 'Student_Data/Year 3/sem 6'

print("")

for file in os.listdir(path):
    if file.endswith(('.jpg', '.png', '.jpeg')) and file.count('.') == 1:
        img_path = os.path.join(path, file)
        img = cv2.imread(img_path)
        
        if img is None:
            continue

        base_id = file.split('.')[0] 
        
      
        bright = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
        cv2.imwrite(os.path.join(path, f"{base_id}.1.jpg"), bright)
        
        
        dark = cv2.convertScaleAbs(img, alpha=0.8, beta=-30)
        cv2.imwrite(os.path.join(path, f"{base_id}.2.jpg"), dark)
        
       
        flip = cv2.flip(img, 1)
        cv2.imwrite(os.path.join(path, f"{base_id}.3.jpg"), flip)
        
       
        blur = cv2.GaussianBlur(img, (5,5), 0)
        cv2.imwrite(os.path.join(path, f"{base_id}.4.jpg"), blur)

        print(f" ID {base_id} ")
        
print("\n!")