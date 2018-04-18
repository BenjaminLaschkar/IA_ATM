"""
Description :
This program train the dataset with all the image 
"""
import os # lib to work with some path
import cv2 # lib openCV
import numpy as np #lib for the pictures
from PIL import Image # lib for the pictures

recognizer=cv2.createLBPHFaceRecognizer(); #OpenCV algorithm to recognize a precise face from a database
path='dataset' #Path for the dataset folder where are the pictures

"""
This function take image from the dataset folder and convert it into an 2D-array where array[0] store Id and array[0][0] store pictures.
"""
def getImagesWithiD(path):
	imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
	faces=[]
	IDs=[]
	for imagePath in imagePaths:
		facesImg=Image.open(imagePath).convert('L');
		faceNp=np.array(facesImg,'uint8')
		ID=int(os.path.split(imagePath)[-1].split('.')[1])
		faces.append(faceNp)
		IDs.append(ID)
		print(ID)
		cv2.imshow("training",faceNp)
		cv2.waitKey(10)
	return np.array(IDs),faces

Ids,faces=getImagesWithiD(path)
recognizer.train(faces,Ids) #We train the recognizer 
recognizer.save('recognizer/trainingData.yml') #We save the .yml recognizer file 
cv2.destroyAllWindows() #Close all windows