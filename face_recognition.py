import cv2
import face_recognition
import numpy as np
import pickle
import time

# Load the trained face encodings and names
with open('modules/MMM-Facial-Recognition/training.pkl', 'rb') as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Load the DNN face detector model from OpenCV
prototxt = "modules/MMM-Facial-Recognition/deploy.prototxt"
model = "modules/MMM-Facial-Recognition/res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# Access the webcam
video_capture = cv2.VideoCapture(0)

logout_delay = 15  # seconds
last_recognition_time = time.time()

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Prepare the frame for DNN face detection
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    face_found = False
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face_roi = frame[startY:endY, startX:endX]
            rgb_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)

            # Use face_recognition to recognize faces
            face_encodings = face_recognition.face_encodings(rgb_face)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    print(f"USER:{name}")
                    face_found = True
                    last_recognition_time = time.time()

    # If no face is found, check if enough time has passed for logout
    if not face_found and time.time() - last_recognition_time > logout_delay:
        print("LOGOUT")

    time.sleep(1)

video_capture.release()
cv2.destroyAllWindows()
