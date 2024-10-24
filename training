import face_recognition
import os
import pickle

# Path to your dataset folder containing the training images
TRAINING_IMAGES_DIR = "/home/pi/MagicMirror/MMM-Facial-Recognition/dataset"

# List to hold face encodings and corresponding user names
known_face_encodings = []
known_face_names = []

# Loop through all images in the dataset folder
for filename in os.listdir(TRAINING_IMAGES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Extract the user name based on the file (match to "Sona" and "Antony")
        if "sona" in filename.lower():
            user_name = "Sona"
        elif "antony" in filename.lower():
            user_name = "Antony"
        else:
            continue  # Skip files that don’t match "Sona" or "Antony"

        # Load the image
        image_path = os.path.join(TRAINING_IMAGES_DIR, filename)
        image = face_recognition.load_image_file(image_path)

        # Find the face encodings for the face in the image
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            # Use the first encoding found (for the first face detected in the image)
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(user_name)

        print(f"Processed {filename} for user {user_name}")

# Save the face encodings and names into a file (training.pkl)
with open('/home/pi/MagicMirror/MMM-Facial-Recognition/training.pkl', 'wb') as f:
    pickle.dump((known_face_encodings, known_face_names), f)

print("Training data saved to training.pkl")
