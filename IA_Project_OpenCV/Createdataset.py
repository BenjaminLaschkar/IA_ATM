"""
Description :
This program take 20 picture of someone and add it to the dataset.
"""

import cv2 #lib openCV
import numpy as np #lib for the pictures
import sqlite3 #lib for the database

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); #The xml file contain 34K line to detect every face.
cam=cv2.VideoCapture(0); #Launch the camera

"""
This function can insert or update name and id into the database
If the id exist, it is updated.
else it is created
"""
def insertOrUpdate(id,name):
    con=sqlite3.connect("FaceBase.db")
    cmd="SELECT ID,Name FROM People WHERE ID=\'"+str(id)+"\'"
    cursor=con.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name="+str(name)+"WHERE ID=\'"+str(id)+"\'"
    else:
        cmd="INSERT INTO People(ID,Name) Values(\'"+str(id)+"\',\'"+str(name)+"\')"
    con.execute(cmd)
    con.commit()
    con.close()

id=raw_input("enter user id") #User enter id
name=raw_input('enter name') #User enter name ! Don't forget the quote !
insertOrUpdate(id,name)

sampleNum=0; #Number of pictures the program has to take for the database
while(True):
    ret,img=cam.read(); #Read img from the camera
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convert the picture into a gray picture
    faces=faceDetect.detectMultiScale(gray,1.3,5); #Detect the face in the gray picture
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1; #Incrementation
        resized_image = cv2.resize(gray[y:y+h,x:x+w], (100, 100))
        cv2.imwrite("dataset/User."+str(id)+"."+str(sampleNum)+".jpg", resized_image) #Add the face into the dataset, the path is : dataset/User.id_User.id_Sample.jpg
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) #Put a rectangle where the face is.
        cv2.waitKey(100); #wait 100 millisecond
    cv2.imshow("Face",img); # show the picture
    if sampleNum==20: #In this program we take 20 pictures for one face.
        break
cam.release() #Free the cam
cv2.destroyAllWindows()  #Close all windows
