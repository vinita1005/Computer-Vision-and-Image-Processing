# Computer-Vision-and-Image-Processing
**Implementation of various computer vision and image processing algorithms

**For this project, we have used the combination of Haar cascade classifiers and local binary patterns recognizer (LBPH).

Abstract
Lot of people visit the Davis Hall at the University of Buffalo’s North campus. The lobby of the building is completely packed with visitors and lot of the time 
it becomes difficult to enroll people for certain visits or events.
To ease this process, we have created a system which will enable people to attend and enroll themselves to such events and direct them to the particular hall/room.
This system consists of a combination of robust face recognition algorithms and an easy to use user interface. The system will welcome you and guide you through the 
enrollment. If you are already enrolled, it will gather your information and let you know the details of your event.
A part of the enhancement! The system also has a speech synthesis module available. It will recognize the user and welcome him warmly. 
If user is not registered to our backend system, it will ask if they want to register. 
It will then take photos of the user for storage in our database and will train itself to recognize the user henceforth.



Working of the system
A simple use case:
1. A faculty/student stands in front of the designated area of the camera.
2. The camera captures the user's face and runs face recognition.
3. The system checks if the user is present in DB.
4. User's details are present in the database and recognition is successful.
5. The details are retrieved and populated on the UI.
6. The message 'Welcome user' is displayed in the message box and spoken out by the system.
7. The user walks past the camera.
4.1 User's details are not present in the database and recognition is unsuccessful.
4.2 The system enables the Enroll and Do Not Enroll buttons with instructions to enroll message.
4.3 The user responds by clicking on Enroll button.
4.4 The system captures the image and requests the user's details through a dialog.
4.5 The system stores the user's details in the database including face recognition details, name, email ID.
4.6 The user walks past the camera.
4.3.1 The user clicks Do Not Enroll.
4.3.2 The UI disables the Enroll and Do Not Enroll buttons
4.3.3 The user walks past the camera.
6.1. Sample images are taken of the user for better accuracy and stored in the system.
