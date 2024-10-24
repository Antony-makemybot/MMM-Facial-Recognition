import pickle

# Load the training data from training.pkl
with open('/home/pi/MagicMirror/modules/MMM-Facial-Recognition/training.pkl', 'rb') as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Print the user names and number of encodings
print("Known face names:", known_face_names)
print("Number of face encodings:", len(known_face_encodings))
