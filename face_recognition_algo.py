import cv2
import numpy as np
import os 
from PIL import Image

def face_database_collection(images,face_id):
    # Opencv trained classifiers for detecting objects of a particular type, e.g. faces 
    # Availability: https://github.com/opencv/opencv/tree/3.4/data/haarcascades
    
    # Syntax of CascadeClassifier & detectMultiScale adapted from Opencv documentation and tutorials:
    # urls: 
    # https://docs.opencv.org/2.4/modules/objdetect/doc/cascade_classification.html
    # http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
    
    cascadePath = "./haarcascade_frontalface_default.xml"

    faceCascade = cv2.CascadeClassifier(cascadePath)
    for i in range(len(images)):
        gray = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,
            minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE )
        for (x,y,w,h) in faces:
            cv2.imwrite("dataset/User." + str(face_id) + '.' +  
                str(i) + ".jpg", gray[y:y+h,x:x+w])
        #cv2.imshow('image', images[i])
    print("Dataset collection completed!")
    print("Training the module. Please wait...")
    train_recognizer()
    print("Training on new Face completed!")
    return True

def getTrainingDataSet(imagePath):
    ## Everytime a new face is detected, we have to train the module again for it to recognize the new face.
    face_samples = []
    face_ids = []
    imagePaths = [os.path.join(imagePath,f) for f in os.listdir(imagePath)] 
    for img in imagePaths:
        ##convert('L') : added because of issue faced in case the dataset image is RGB and we need grayscale
        image = Image.open(img).convert('L')
        image = np.array(image, dtype=np.uint8)
        face_id = int(os.path.split(img)[-1].split(".")[1])
        face_samples.append(image)
        face_ids.append(face_id)
    return face_samples,face_ids

def train_recognizer():
    # Syntax for functions of face_recognizer referenced by Opencv FaceRecognizer documentation
    # url: https://docs.opencv.org/2.4/modules/contrib/doc/facerec/facerec_api.html
    #face_database_collection(face_id, gray)
    imagePath = "./dataset/"
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces,face_ids = getTrainingDataSet(imagePath)
    face_recognizer.train(faces, np.array(face_ids))
    face_recognizer.write('trainer/trainer.yml') 
    
def recognize_faces(cv2image):
    # Syntax for LBPHFaceRecognizer_create referenced by Opencv cv::face::LBPHFaceRecognizer Class Reference documentation
    # url: https://docs.opencv.org/3.4/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html
    # Syntax for functions of face_recognizer referenced by Opencv FaceRecognizer documentation
    # url: https://docs.opencv.org/2.4/modules/contrib/doc/facerec/facerec_api.html
    
    print("tring to recognize")
    #convert to grayscale for matching
    cascadePath = "./haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    gray = cv2.cvtColor(cv2image,cv2.COLOR_BGR2GRAY)
    
    ## Added face detection again because we are recieving a box frame 
    ## and without detecting the facial coordinates (x,y,w,h), the predict function does not operate accurately.
    faces = faceCascade.detectMultiScale(gray)
    
    if len(faces) == 0:
        #print("No faces!")
        return cv2image, None
    
    #face recognition module
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    #Read the trained faces
    try:
        face_recognizer.read('trainer/trainer.yml')
    except:
        print("No trained module!")
        return cv2image, str(0)
    
    face_id = 0
    for (x, y, w, h) in faces:
        face_id, prediction_score = face_recognizer.predict(gray[y:y+h,x:x+w])
    #print(face_id)
    if prediction_score < 70:
        print("Face recognized")
        return cv2image, str(face_id)
    else:
        return cv2image, str(0)
        