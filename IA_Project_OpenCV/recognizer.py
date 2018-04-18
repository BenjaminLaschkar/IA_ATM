"""
----------------------------------------------------------------------------------------------------
Description :

This program recognize faces based on the trainer file.
It generate session if a face is hightly recognized during 2.5 sec. This session keep in memory the associated person.
The session is lost if there is no face or if the face is unknow during 1 sec.
The previous session are keep in memory and necessitate only 1 sec recognization.

You can freely change this variable to play with the code

DURATION_TO_SESSION_VALIDATE=X
DURATION_TO_SESSION_DEVALIDATE=X
DURATION_TO_PREVIOUS_SESSION_VALIDATE=X

----------------------------------------------------------------------------------------------------
"""

def get_profile(id):
    """ This function get the full profile from database """
    con = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE ID="+str(id)
    cursor = con.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    con.close()
    return profile

"""" This function set the id to Unknow if the confidence is low """
def SetToUnknow(id):
    if(confidence>100):
        id=0
    return id

"""" This function compute the time """
def AddTimeToDuration(duration):
    timestamp_end = time.time()
    duration=duration+(timestamp_end-timestamp_start)
    return duration

""" This function update the duration of the actual session """
def UpdateSessionDuration():
    global session_duration
    if(confidence<50 and session_validate == False and previous_session_profile[0]==session_profile[0] and len(faces)==1 ): #if the session isn't validate and we get a good confidence about the face (under 50)
        no_session_duration=0                                                                                               #the no session time is reset to 0
        session_duration=AddTimeToDuration(session_duration)                                                                #Add some time
        print "Session duration for : "+str(session_profile[1])+" is "+str(session_duration)+" s"                           #Print the current session time
    else:
        session_duration=0

""" This function check if the session is valid (with the definited time) """
def IsSessionIsValid():
    global session_validate,session_profile_validate
    if(session_validate == False and session_duration>DURATION_TO_SESSION_VALIDATE or session_duration>DURATION_TO_PREVIOUS_SESSION_VALIDATE and session_profile==previous_session_profile_validate): #If the session is not validate and the session time can validate it
        session_profile_validate=session_profile;                                   #The session profile is in memory
        session_validate = True                                                     #session is validate
        print str(session_profile_validate[1])+" is validate"                       #Print that the user session is validated


""" This function draw green square if there is a valid session"""
def SessionIsValid():
    global no_session_duration,AfficherInterface
    if(session_validate==True and len(faces)==1):                                                           #if the session is validate
        no_session_duration=0                                                                               #the no session time is reset to 0
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)                                                      #Draw a green rectangle for the face
        cv2.cv.PutText(cv2.cv.fromarray(img),str(session_profile_validate[1]),(x,y+h+30),font,(0,255,0));   #We place a text under with the session_name which is validate
        cv2.cv.PutText(cv2.cv.fromarray(img),"age : "+str(profile[2]),(x,y+h+60),font,(0,255,0));
        AfficherInterface=True



""" This function draw red square if there is no session"""
def ThereIsNoSession():
    if(profile!=None and session_validate!=True):                                                           #If we determine a profile (even as Unknow)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)                                                      #Draw Red rectangle
        cv2.cv.PutText(cv2.cv.fromarray(img),"confidence : "+str(confidence),(x,y+h+30),font,(0,0,255));    #We place a text under with the confidence
        cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+60),font,(0,0,255));                    #We place a text under with the name
        cv2.cv.PutText(cv2.cv.fromarray(img),"age : "+str(profile[2]),(x,y+h+90),font,(0,0,255));           #We place a text under with the age

""" This function update the duration of the actual no_session """
def UpdateNoSessionDuration():
    global no_session_duration,session_validate,previous_session_profile_validate,session_duration
    if(id==0 or len(faces)==0 or len(faces)>1):                                 #If there is no face or if the persone is unknow or if there is multiple face
        no_session_duration=AddTimeToDuration(no_session_duration)              #Compute the time and add it to the no_session
        print "No session during : "+str(no_session_duration)+" s"              #Print the current no session time
        session_duration=0                                                      #the session time is reset to 0
        if(no_session_duration>DURATION_TO_SESSION_DEVALIDATE):                 #if the no session time exceed the time to unvalidate
            session_validate=False                                              #session is unvalidate
            previous_session_profile_validate=session_profile_validate          #Declare a previous session

""" This function setup the program, configure the camera, launch it , create a recognizer and charge data for the recognizer """
def setup():
    global font,faceDetect,cam,recognizer
    font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,1,1,0,1)          #Configure text police
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');    #The xml file contain 34K line to detect every face.
    cam=cv2.VideoCapture(0);                                                    #Launch the camera
    recognizer=cv2.createLBPHFaceRecognizer();                                  #OpenCV algorithm to recognize a precise face from a database, if you need more info search for : "Local Binary Pattern histogram Fourier" (LBPHF)
    recognizer.load('recognizer\\trainingData.yml')                             #Charge the trainingdata from the path

""" This function close the program """
def Quit():
    cam.release()           #free the camera
    cv2.destroyAllWindows() #Close all windows

""" This function get the faces from the camera """
def getFacesFromCamera():
    global img, img_gray,timestamp_start,faces
    timestamp_start = time.time()                           #Select the time at this moment We would use it to compute time for session
    ret,img=cam.read();                                     #Read img from the camera
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)           #Convert the picture into a gray picture
    faces=faceDetect.detectMultiScale(img_gray,1.3,5);      #Detect the face in the gray picture

""" This function declare globals variables """
def declareGlobalsVariable():
    global id,no_session_duration,no_session_duration,previous_session_profile,session_profile,previous_session_profile_validate,session_profile_validate,session_validate, OnlyOnce, AfficherInterface
    id, session_duration, no_session_duration = 0 , 0 , 0
    previous_session_profile , session_profile = [3] , [3]
    previous_session_profile[0] , session_profile[0] = 0 , 0
    previous_session_profile_validate, session_profile_validate= None, None
    session_validate=False
    OnlyOnce = True
    AfficherInterface = False

""" This function check if there is more than one face on the camera"""
def atLeastOneFaceIsDetected(faces):
    if(len(faces)>0):
        return True

""" This function recognize face from the gray image and call other usefull fonction"""
def tryToRecognizeFace():
    global id,confidence,recognizer,profile,session_profile,pr
    id,confidence=recognizer.predict(img_gray[y:y+h,x:x+w])         #Get the confidence and the id of the detected face
    profile=get_profile(SetToUnknow(id))                             #We get the full profile from database, if the confidence is low the id is marked as "Unknow"
    session_profile=profile                                         #we create a session for the user profile
    UpdateSessionDuration()                                         #Update the duration of the actual session
    IsSessionIsValid()                                              #Check if the session is valid

"""Draw rectangle, green or red"""
def drawRectangleAroundDetectedFace():
    SessionIsValid()                        #If the session is valid draw green rectangle
    ThereIsNoSession()                      #If there is no session, draw red rectangle

"""Update necessary data"""
def update():
    global previous_session_profile,session_profile
    UpdateNoSessionDuration()                           #If there is no session, update no_session_duration
    previous_session_profile=session_profile            #we keep in memory the previous session

"""Show the image from the camera"""
def renderView():
    cv2.imshow("Face",img);                             #We show the picture

def callback():
    payload = {'sendcommand': 'retirerArgent'}
    r = requests.post("http://192.168.43.176:8888/sendcommand/", json=payload)
    print r

def displayInterface():
    global OnlyOnce, session_profile_validate
    if(OnlyOnce and AfficherInterface):
        fenetre = Tk()
        hello_text="Bonjour "+session_profile_validate[1]
        champ_label = Label(fenetre, text=hello_text)
        champ_label_2 = Label(fenetre, text="Combien voulez vous retirez ?")
        bouton_retirer_argent = Button(fenetre, text="annuler", command = fenetre.destroy)
        bouton_annuler = Button(fenetre, text="20$", command = callback)
        champ_label.pack()
        champ_label_2.pack()
        bouton_annuler.pack()
        bouton_retirer_argent.pack()
        fenetre.mainloop()
        OnlyOnce = False


import requests
from Tkinter import *
import cv2              #Lib openCV
import numpy as np      #Lib for pictures
import sqlite3          #Lib for database
import time             #Lib time for the session
DURATION_TO_SESSION_VALIDATE, DURATION_TO_SESSION_DEVALIDATE, DURATION_TO_PREVIOUS_SESSION_VALIDATE=2.5 , 1 , 1
declareGlobalsVariable()
setup()
while(cv2.waitKey(1)!=ord('q')):
    getFacesFromCamera()
    if atLeastOneFaceIsDetected(faces):
        for(x,y,w,h) in faces:
            tryToRecognizeFace()
            drawRectangleAroundDetectedFace()
    update()
    renderView()
    displayInterface()
Quit()
