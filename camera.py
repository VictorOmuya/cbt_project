import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import ImageGrab


def classname():
    
    path = 'images'
    images = []
    classNames = []
    myList = os.listdir(path)
    
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        print(classNames)
    return classNames, images
 
def findEncodings(images):
    
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
      
    return encodeList
 
 
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
def captureScreen(bbox=(300,300,690+300,530+300)):
    capScr = np.array(ImageGrab.grab(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr

def capture():
    classNames, images = classname()
    encodeListKnown = findEncodings(images)
     
    cap = cv2.VideoCapture(0)
     
    while True:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
     
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
     
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #for i in faceDis:
             #   print(faceDis)
              #  if i >= 0.86:
            matchIndex = np.argmin(faceDis)
         
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                        
                        #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,"face detected",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            else:
                name = 'face not detected'
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
         
     
        cv2.imshow('Webcam',img)
        cv2.waitKey(1)
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            
                break
    cap.release()    
    cv2.destroyAllWindows()
    
    
        
    return name, classNames, matchIndex
#classn, imgs = classname()
#findEncodings(imgs)


def detectface():     
    try:

        name, classn, matchIndex = capture()
                
        if name == classn[matchIndex].upper():
            
            res = 'authentication successful'      
            print('authentication successful')
                
        elif name == 'Authentication Failed':
            res = 'authentication failed'
            print('authentication failed...')
                    
        else:
            res = 'authentication failed'
            print('authentication failed...')
        return name, res
    except:
        print('Fatal Error!')
    
   