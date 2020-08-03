import tkinter as tk
import time
from PIL import Image, ImageTk
import PIL
import cv2
from database_operations import *
from face_recognition_algo import *
import numpy as np
import speech_recognition as sr
import threading
import pyttsx3

class MyDialog:
    ## UI dialog box implementation adapted as in:
    ## https://runestone.academy/runestone/books/published/thinkcspy/GUIandEventDrivenProgramming/02_standard_dialog_boxes.html  
    def __init__(self, master):

        top = self.top = tk.Toplevel(master)

        # UBID
        lbl_ubid = tk.Label(top, width=15, text="UB ID#", anchor='w')
        self.ent_ubid = tk.Entry(top)
        lbl_ubid.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_ubid.grid(row=0, column=1, padx=5, pady=5)

        # Name
        lab_name = tk.Label(top, width=15, text="Name", anchor='w')
        self.ent_name = tk.Entry(top)
        lab_name.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_name.grid(row=1, column=1, padx=5, pady=5)

        # Email
        lab_email = tk.Label(top, width=15, text="Email", anchor='w')
        self.ent_email = tk.Entry(top)
        lab_email.grid(row=2, column=0, padx=5, pady=5)
        self.ent_email.grid(row=2, column=1, padx=5, pady=5)

        # Label displays informative messages
        self.lbl_msg = tk.Label(top, text="Enter details.")
        self.lbl_msg.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Ok and Cancel buttons
        self.btn_ok = tk.Button(top, text="Ok", command=self.okaction)
        self.btn_cancel = tk.Button(top, text="Cancel", command=self.cancelaction)
        self.btn_ok.grid(row=4, column=0, padx=5, pady=5)
        self.btn_cancel.grid(row=4, column=1, padx=5, pady=5)

    # On ok button click
    def okaction(self):
        # Validate entries
        global detailsFromDialog
        n = self.ent_name.get()
        e = self.ent_email.get()
        id = self.ent_ubid.get()
        if n == "" or e == "" or id == "":
            # Update label to reenter details
            self.lbl_msg.configure(text="One or more entries are missing! Re-enter details")
        else:
            detailsFromDialog = (n, e, id)
            self.top.destroy()

    # On cancel button click
    def cancelaction(self):
        global detailsFromDialog
        detailsFromDialog = None
        self.top.destroy()


class GUI:

    def __init__(self):
        self.main_window = None
        self.video_frame = None
        self.label_img = None
        self.details_frame = None
        self.mbox_frame = None
        self.textarea = None
        self.cur_img = None
        self.name = None
        self.email = None
        self.ubid = None
        self.enrollTime = None
        self.detected = False
        self.btn_enroll = None
        self.states = {}
        self.btn_donotenroll = None
        self.toBeEnrolledImg = []
        self.feed_img = None
        self.currentFrame = None
        self.previousFrame = None
        self.static_back = None
        self.infocus = False
        self.enrollDlg = None
        self.motionInterval = None
        self.width, self.height = 400, 300
        self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def speakSentence(self, sentence):
        speaker = pyttsx3.init()
        speaker.say(sentence)
        speaker.runAndWait()
        speaker.stop()

    def initializeSpeechModule(self):
        ## Speech synthesis module adapted as given in:
        ## https://realpython.com/python-speech-recognition/
        r = sr.Recognizer()
        mic = sr.Microphone(0)

        print(sr.Microphone.list_microphone_names())
        with mic as source:
            while True:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                # set up the response object
                response = {
                    "success": True,
                    "error": None,
                    "transcription": None
                }

                # try recognizing the speech in the recording
                # if a RequestError or UnknownValueError exception is caught,
                #     update the response object accordingly
                try:
                    response["transcription"] = r.recognize_google(audio)
                except sr.RequestError:
                    # API was unreachable or unresponsive
                    response["success"] = False
                    response["error"] = "API unavailable"
                except sr.UnknownValueError:
                    # speech was unintelligible
                    response["error"] = "Unable to recognize speech"

                if response["transcription"] == "yes" or response["transcription"] == "no":
                    print(response["transcription"])
                    self.textarea.insert(tk.END, response["transcription"])
                    self.speakSentence("Spoke " + response["transcription"])
                    # break

    def createVideoStreamFrame(self):
        self.video_frame = tk.Frame(self.main_window)
        self.video_frame.grid(row=0, column=0, padx=5, pady=5)
        self.label_img = tk.Label(self.video_frame, borderwidth=2, relief="solid")
        self.label_img.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    def createDetailsFrame(self):
        self.details_frame = tk.Frame(self.main_window, borderwidth=2, relief="solid")
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.ubid = tk.StringVar()

        # UBID
        lbl_ubid = tk.Label(self.details_frame, width=15, text="UB ID#", anchor='w')
        ent_ubid = tk.Label(self.details_frame, textvariable=self.ubid)
        lbl_ubid.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ent_ubid.grid(row=0, column=1, padx=5, pady=5)

        # Name
        lab_name = tk.Label(self.details_frame, width=15, text="Name:", anchor='w')
        ent_name = tk.Label(self.details_frame, textvariable=self.name)
        lab_name.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ent_name.grid(row=1, column=1, padx=5, pady=5)

        # Email
        lab_email = tk.Label(self.details_frame, width=15, text="Email:", anchor='w')
        ent_email = tk.Label(self.details_frame, textvariable=self.email)
        lab_email.grid(row=2, column=0, padx=5, pady=5)
        ent_email.grid(row=2, column=1, padx=5, pady=5)

        # Enroll and do not enroll buttons
        self.btn_enroll = tk.Button(self.details_frame, text="Enroll", state=tk.DISABLED, command=self.enrollUser)
        self.btn_donotenroll = tk.Button(self.details_frame, text="Do not Enroll", state=tk.DISABLED, command=self.resetState)
        self.btn_enroll.grid(row=4, column = 0, padx=5, pady=5)
        self.btn_donotenroll.grid(row=4, column=1, padx=5, pady=5)
        self.details_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

    def createTextAreaFrame(self):
        self.mbox_frame = tk.Frame(self.main_window)
        self.textarea = tk.StringVar()
        txtBox = tk.Message(self.mbox_frame, width=400, anchor=tk.NW, justify=tk.LEFT, textvariable=self.textarea)
        self.textarea.set("Please position your face within the green rectangle seen in the camera feed.")
        txtBox.grid(row=0, column=0, padx=5, pady=5)
        self.mbox_frame.grid(row=1, column=0, sticky=tk.W, columnspan=2, padx=5, pady=5)

    def initializeStates(self):
        self.states["detected"] = False
        self.states["enroll"] = False

    def setup(self):
        ## Video cam implementation adapted as in:
        ## https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
        self.main_window = tk.Tk()
        self.main_window.wm_title("Visual Welcome Center")

        # Initialize GUI Elements
        self.createVideoStreamFrame()
        self.createDetailsFrame()
        self.createTextAreaFrame()
        self.initializeStates()

        # Set the window size. Do not allow resizing
        self.main_window.geometry("800x400")
        self.main_window.resizable(0, 0)

        # Speech recognition thread
        spchModule = threading.Thread(target=self.initializeSpeechModule, args=())
        spchModule.start()

        # Camera feed thread
        # Camera updates self.feed_image from the thread.
        # self.feed_image is read by the load image function for further processing.
        camModule = threading.Thread(target=self.cameraFeed, args=())
        camModule.daemon = True
        camModule.start()

    def enrollUser(self):
        # Update the label to prompt user to enter details
        # Enable the approprite buttons, Enroll and save
        success = False
        while not success:
            self.enrollDlg = MyDialog(self.main_window)
            self.main_window.wait_window(self.enrollDlg.top)
            if detailsFromDialog is not None:   # Ok action
                #print(detailsFromDialog[0])
                # If duplicate UBID, just capture image
                # else add all details
                face_database_collection(self.toBeEnrolledImg, int(detailsFromDialog[2]))
                insert_rows(int(detailsFromDialog[2]), detailsFromDialog[0], detailsFromDialog[1])
                self.textarea.set("Enrolment completed.\nHave a nice day!")
                success = True
            else:   # Cancel action
                success = True
        self.states["enroll"] = False
        self.states["detected"] = False
        self.toBeEnrolledImg = None
        self.resetState()

    def resetState(self):
        print("Reset")
        self.removeDetailsFromForm()
        self.btn_enroll['state'] = tk.DISABLED
        self.btn_donotenroll['state'] = tk.DISABLED
        self.toBeEnrolledImg = []
        self.states["enroll"] = False
        self.states["detected"] = False
        self.textarea.set("Please position your face within the green rectangle seen in the camera feed.")
        # Update label to default vale : Please position your face within the rectangle

    def cameraFeed(self):
        while True:
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            self.feed_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #self.feed_img = cv2.resize(self.feed_img, (0, 0), fx=0.5, fy=0.5)

    def startEnrolling(self):
        self.states["enroll"] = True
        self.states["detected"] = False
        self.btn_enroll['state'] = tk.NORMAL
        self.btn_donotenroll['state'] = tk.NORMAL
        self.textarea.set("Do you wish to enroll yourself?"
                          + "\nClick Enroll button if you wish to enroll.\nClick Do Not Enroll otherwise."
                          + "\n We will capture your image and save your UB#, Name and Email during enrollment.")
        self.enrollTime = time.time()

    def addDetailsToForm(self):
        self.ubid.set("22222")
        self.email.set("2@2.com")
        self.name.set("Vinay")

    def removeDetailsFromForm(self):
        self.ubid.set("")
        self.email.set("")
        self.name.set("")

    def displayKnownUserData(self, ubit):
        self.states["detected"] = True
        self.states["enroll"] = False
        # TO DO
        #print("Getting ")
        userdata = get_data(ubit)
        #userdata = []
        #print(userdata)
        if len(userdata) >= 1:
            spkSntnce = "Welcome, " + userdata[0][0]
            self.speakSentence(spkSntnce)
            self.textarea.set(spkSntnce)
            self.name.set(userdata[0][0])
            self.email.set(userdata[0][4])
            self.ubid.set(userdata[0][3])

    def processCroppedSection(self, cropped_for_face):
        cand_image = cropped_for_face
        ubit = None

        cand_image, ubit = recognize_faces(cropped_for_face)

        if not self.states["detected"] and self.states["enroll"]:
            print("In F T condition with ubit: ", ubit)
            # Save user's images.
            # If needed, give a timer. If user never finishes, reset the system
            if ubit is None:
                if self.enrollDlg is None:
                    self.states["enroll"] = False
                    self.toBeEnrolledImg = []
                    self.resetState()
                    print("Stopping enrollment since face is out of focus.")
                print("Please make sure your face is inside the box!")
            elif ubit == "0":
                if time.time() - self.enrollTime > 60:
                    self.resetState()
                    self.states["enroll"] = False
                    self.toBeEnrolledImg = []
                elif len(self.toBeEnrolledImg) < 30:
                    self.toBeEnrolledImg.append(cropped_for_face)
            elif ubit != "0":
                self.displayKnownUserData(ubit)
                print("Person recognized: ", ubit)

        elif not self.states["detected"] and not self.states["enroll"]:
            print("In F F condition with ubit:", ubit)
            # print("Nothing seen yet")
            if ubit is None:
                print("No faces detected")
                self.resetState()
            elif ubit != "0":
                self.displayKnownUserData(ubit)
                print("Person recognized: ", ubit)
            elif ubit == "0":
                self.toBeEnrolledImg.append(cropped_for_face)
                self.startEnrolling()

        elif self.states["detected"] and not self.states["enroll"]:
            # print("Last iteration, a face was detected.")
            print("In T F condition with ubit:", ubit)
            if ubit is None:
                # No face in the image. Reset everything.
                self.states["detected"] = False
                self.resetState()
            elif ubit == "0":
                self.states["detected"] = False
                self.toBeEnrolledImg.append(cropped_for_face)
                self.startEnrolling()
            elif ubit != "0":
                self.displayKnownUserData(ubit)
                print("Person recognized: ", ubit)

        elif self.states["detected"] and self.states["enroll"]:
            print("Does not really come to this state!")
            self.resetState()

    def checkForMotion(self, cropped_section):

        stat_crop = cv2.matchTemplate(self.static_back, cropped_section, cv2.TM_CCORR_NORMED)
        #print(stat_crop)
        #print(self.infocus)
        # Value greater than 0.94: No motion
        # Value less than that, detect motion
        if not  self.infocus and stat_crop >= 0.95:
            return False
        elif not self.infocus and stat_crop < 0.95:
            self.infocus = True
            return True
        elif self.infocus and stat_crop >= 0.95:
            self.infocus = False
            return True
        elif self.infocus and stat_crop < 0.95:
            return False

    def loadImage(self):
        if self.feed_img is None:
            self.label_img.after(1, self.loadImage)
        cv2image = self.feed_img
        cv2image_copy = np.copy(cv2image)
        c_top = int(cv2image.shape[0] * 0.15)
        c_left = int(cv2image.shape[1] * 0.30)
        c_bottom = int(cv2image.shape[0] * 0.85)
        c_right = int(cv2image.shape[1] * 0.70)
        cv2.rectangle(cv2image_copy, (c_left, c_top), (c_right, c_bottom), (0, 255, 0), 3)
        cropped_for_face = cv2image[c_top:c_bottom, c_left:c_right]


        # When program starts
        if self.static_back is None:
            self.static_back = cropped_for_face
            self.motionInterval = time.time()

        # Check motion in the image every 2 seconds
        if time.time() - self.motionInterval > 3:
            if self.checkForMotion(cropped_for_face):
                self.processCroppedSection(cropped_for_face)
            self.motionInterval = time.time()

        if self.states["enroll"]:
            if time.time() - self.enrollTime > 60:
                self.resetState()
                self.states["enroll"] = False
                self.toBeEnrolledImg = []
            elif len(self.toBeEnrolledImg) < 30:
                self.toBeEnrolledImg.append(cropped_for_face)

        img = PIL.Image.fromarray(cv2image_copy)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label_img.imgtk = imgtk
        self.cur_img = imgtk
        self.label_img.configure(image=imgtk)
        self.label_img.after(200, self.loadImage)


gui = GUI()
gui.setup()
detailsFromDialog = None
print("Hello")
time.sleep(5)
gui.loadImage()
gui.main_window.mainloop()