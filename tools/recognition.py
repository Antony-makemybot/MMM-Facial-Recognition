import face_recognition
import pickle
import time
import cv2
import signal
import os
import numpy
import base64
from datetime import datetime
from utils.image import Image
from utils.arguments import Arguments
from utils.print import Print
from picamera2 import Picamera2

def signalHandler(signal, frame):
    global closeSafe
    closeSafe = True

signal.signal(signal.SIGINT, signalHandler)
closeSafe = False

# Prepare console arguments
Arguments.prepareRecognitionArguments()

# Load the known faces and embeddings along with OpenCV's Haar cascade for face detection
Print.printJson("status", "loading encodings + face detector...")
data = pickle.loads(open(Arguments.get("encodings"), "rb").read())
detector = cv2.CascadeClassifier(Arguments.get("cascade"))

# Initialize the video stream
Print.printJson("status", "starting video stream...")
processWidth = Arguments.get("processWidth")
resolution = Arguments.get("resolution").split(",")
resolution = (int(resolution[0]), int(resolution[1]))
Print.printJson("status", resolution)
Print.printJson("status", processWidth)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (resolution[0], resolution[1]), "format": "XRGB8888"}))
picam2.start()

# Variable for previous names
prevNames = []

# Create unknown path if needed
if Arguments.get("extendDataset") is True:
    unknownPath = os.path.dirname(Arguments.get("dataset") + "unknown/")
    try:
        os.stat(unknownPath)
    except:
        os.mkdir(unknownPath)

tolerance = float(Arguments.get("tolerance"))

# Loop over frames from the video file stream
while True:
    # Read the frame
    originalFrame = picam2.capture_array()
    
    # Adjust image brightness and contrast
    originalFrame = Image.adjust_brightness_contrast(
        originalFrame, Arguments.get("brightness"), Arguments.get("contrast")
    )

    if Arguments.get("rotateCamera") >= 0 and Arguments.get("rotateCamera") <= 2:
        originalFrame = cv2.rotate(originalFrame, Arguments.get("rotateCamera"))

    # Resize image if we want to process a smaller image
    if processWidth != resolution[0] and processWidth != 0:
        frame = Image.resize(originalFrame, width=processWidth)
    else:
        frame = originalFrame

    if Arguments.get("method") == "dnn":
        # Load the input image and convert it from BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=Arguments.get("detectionMethod"))
    elif Arguments.get("method") == "haar":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the grayscale frame
        rects = detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        # Reorder bounding box coordinates
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # Compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # Loop over the facial embeddings
    for encoding in encodings:
        distances = face_recognition.face_distance(data["encodings"], encoding)

        minDistance = 1.0
        if len(distances) > 0:
            minDistance = min(distances)

        if minDistance < tolerance:
            idx = numpy.where(distances == minDistance)[0][0]
            name = data["names"][idx]
        else:
            name = "unknown"

        names.append(name)

    # Loop over the recognized faces
    for (top, right, bottom, left), name in zip(boxes, names):
        # Draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        txt = name + " (" + "{:.2f}".format(minDistance) + ")"
        cv2.putText(
            frame, txt, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2
        )

        # Send the FACE_RECOGNIZED notification
        if name != "unknown":
            Print.printJson("FACE_RECOGNIZED", {"name": name})

    # Display the image to our screen
    if Arguments.get("output") == 1:
        cv2.imshow("Frame", frame)

    if Arguments.get("outputmm") == 1:
        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode()
        Print.printJson("camera_image", {"image": jpg_as_text})

    logins = []
    logouts = []
    # Check for new logins and logouts
    for n in names:
        if prevNames.__contains__(n) == False and n is not None:
            logins.append(n)

            # Save the picture if extending the dataset
            if Arguments.get("extendDataset") is True:
                path = os.path.dirname(Arguments.get("dataset") + "/" + n + "/")
                today = datetime.now()
                cv2.imwrite(
                    path + "/" + n + "_" + today.strftime("%Y%m%d_%H%M%S") + ".jpg",
                    originalFrame,
                )
    for n in prevNames:
        if names.__contains__(n) == False and n is not None:
            logouts.append(n)

    # Send information to prompt if something has changed
    if logins.__len__() > 0:
        Print.printJson("login", {"names": logins})

    if logouts.__len__() > 0:
        Print.printJson("logout", {"names": logouts})

    # Update previous names for the next iteration
    prevNames = names

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or closeSafe == True:
        break

    time.sleep(Arguments.get("interval") / 1000)

# Cleanup
picam2.stop()
cv2.destroyAllWindows()
