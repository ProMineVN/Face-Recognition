import cv2
import numpy as np
import os
from PIL import Image

def getImageWithCode():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path="dataSet"
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    ids=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert("L")
        faceNp=np.array(faceImg,"uint8")
        print(faceNp)
        Id=int(imagePath.split('.')[2])
        faces.append(faceNp)
        ids.append(Id)
        cv2.imshow('tranning',faceNp)
        cv2.waitKey(10)

    recognizer.train(faces, np.array(ids))
    if not os.path.exists('recoginzer'):
        os.makedirs('recoginzer')
    recognizer.save('recoginzer/trainningData.yml')
    cv2.destroyAllWindows()
