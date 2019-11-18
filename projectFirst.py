import picamera
import os
import cv2
import numpy as np
import faceRecognition as fr
from time import sleep
import datetime

namesAndPath = {1:"Ayush Kumar",2:"Harsh",3:"Varun",4:"Varun Chowdahry",5:"Shubham Kumar"}
db = {}

#take photos and create folder and make entry in dictinary file
def take_picture(name,i,numDirs):
    print("About to take a Picture")
    path = "/home/pi/Desktop/Project3/trainingImages/"+str(numDirs)+"/"+name+str(i)+".jpeg"
    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.capture(path)
    print("Picture taken.")


def saveDetails(name):
    
    path = '/home/pi/Desktop/Project3/trainingImages/'
    for i,j,k in os.walk(path):
        number_of_dirs = len(j)
        break
    number_of_dirs += 1
    p1 = '/home/pi/Desktop/Project3/trainingImages/'+str(number_of_dirs)
    os.mkdir(p1)
    #namesAndPath[len(namesAndPath)+1] = name 
    #print(namesAndPath)
    print(name+" get ready for 10 pictures to be taken")
    print("Also as you are ready for next shot, please press 's' ")
    for i in range(10):
        j = raw_input("Ready, press 's': ")
        if j=='s':
            take_picture(name,i,number_of_dirs)
        else:
            print("Sorry wrong key is pressed")
            i -= 2
            
    print("Thanks "+name)
    print("Now classifier is running on the taken images")
    #use for training data if new images are introduced:-
    try:
        faces,faceId=fr.labels_for_training_data('/home/pi/Desktop/Face Recognition/trainingImages')
        face_recognizer = fr.train_classifier(faces,faceId)
        face_recognizer.save('trainingData.yml')
    except:
        print("Something is wrong with the captured Image")
        return
    print("Face classified Successfully")
    return


def checkIn(name):
    global db
    print("About to take a Picture")
    path = "/home/pi/Downloads/"+name+".jpg"
    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.capture(path)
    print("Picture taken.")
    test_img = cv2.imread("/home/pi/Desktop/Face Recognition/TestImages/"+name+".jpg")
    faces_detected,gray_img = fr.faceDetection(test_img)
    print("faces detected: ", faces_detected)
    #use for testing purpose:-
    face_recognizer = cv2.createLBPHFaceRecognizer()
    face_recognizer.load('/home/pi/Desktop/Project3/trainingData.yml')
    predicted_name = ""
    for face in faces_detected:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+h,x:x+h]
        label,confidence=face_recognizer.predict(roi_gray)
        print("confidence: ", confidence)
        print("label: ", label)
        fr.draw_rect(test_img,face)
        predicted_name =namesAndPath[label]
        fr.put_text(test_img,predicted_name,x,y)
    
    print(predicted_name+" You are checked-in successfully")
    db[predicted_name] =  datetime.datetime.utcnow()
    return 


def checkOut(name):
    global db
    if name in db.keys():
        dt_ended = datetime.datetime.utcnow()
        dt_started = db[name]
        print("You were "+str((dt_ended - dt_started).total_seconds())+" seconds present")
        return
    else:
        print("Details not Found")
        return


if __name__ == "__main__":
    print("Check-In Check-Out Project")
    
    while True:
        print("##################################################")
        name = raw_input("Enter your Name: ")
        print("Choose option:-")
        print("Save New Entry, enter 1")
        print("Check In, enter 2")
        print("Check Out, enter 3")
        print("For Exit, enter 9")
        choice = int(raw_input("Enter your choice: "))
        if choice==1:
            saveDetails(name)
        elif choice==2:
            checkIn(name)
        elif choice==3:
            checkOut(name)
        elif choice==9:
            print("Exiting....")
            break
        else:
            print("Entered wrong choice, exiting....")
            break

