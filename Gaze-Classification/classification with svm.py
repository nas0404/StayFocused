import mediapipe as mp
import cv2
import gaze
from sklearn import svm
import numpy as np
import time  # <-- already present

mp_face_mesh = mp.solutions.face_mesh  # initialize the face mesh model
calibration_recordings = []

NUM_CALIBRATION = 9  # Number of calibration samples

# camera stream:
cap = cv2.VideoCapture(0)  # chose camera index (try 1, 2, 3)
with mp_face_mesh.FaceMesh(
        max_num_faces=1,  # number of faces to track in each frame
        refine_landmarks=True,  # includes iris landmarks in the face mesh model
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:  # no frame input
            print("Ignoring empty camera frame.")
            continue
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # frame to RGB for the face-mesh model
        results = face_mesh.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # frame back to BGR for OpenCV

        if results.multi_face_landmarks:
            try:
                gaze.gaze(image, results.multi_face_landmarks[0])  # gaze estimation
            except Exception as e:
                print(f"Error in gaze.gaze: {e}")

        cv2.imshow('output window', image)
        key = cv2.waitKey(2) & 0xFF  # Get key press

        # Record landmarks if 'r' is pressed and less than NUM_CALIBRATION sets are recorded
        if key == ord('r') and results.multi_face_landmarks and len(calibration_recordings) < NUM_CALIBRATION:
            landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]
            calibration_recordings.append(landmarks)
            print(f"Recorded landmarks {len(calibration_recordings)}/{NUM_CALIBRATION}.")

        # Print and break if NUM_CALIBRATION sets are recorded
        if len(calibration_recordings) == NUM_CALIBRATION:
            print("Collected all calibration recordings.")
            break

        # Wait for ESC key to exit
        if key == 27:
            break
cap.release()
cv2.destroyAllWindows()

time.sleep(0.5)  # <-- Add a short delay to let OS release the camera

if len(calibration_recordings) == NUM_CALIBRATION:
    # --- SVM Training ---
    X = []
    y = []
    for i, landmarks in enumerate(calibration_recordings):
        features = []
        for lm in landmarks[:10]:
            features.extend([lm[0], lm[1], lm[2]])
        X.append(features)
        y.append(i)  # Each calibration gets a unique label
    X = np.array(X)
    y = np.array(y)
    clf = svm.SVC(kernel='linear')
    clf.fit(X, y)
    print("SVM trained on calibration recordings.")

    # --- Classification mode ---
    print("Entering classification mode...")  # DEBUG
    cap = cv2.VideoCapture(0)  # <-- create a new VideoCapture object here
    if not cap.isOpened():
        print("Error: Could not open camera for classification mode.")
    else:
        print("Camera opened for classification mode.")  # DEBUG
        with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:
            while True:  # <-- Use while True for classification loop
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame in classification mode.")
                    time.sleep(0.1)  # Add a short delay before retrying
                    continue
                # print("Read a frame in classification mode.")  # DEBUG (optional, can comment out)
                image.flags.writeable = False
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image_rgb)
                image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
                label = "No face"
                if results.multi_face_landmarks:
                    # Overlay face mesh landmarks (optional)
                    for landmark in results.multi_face_landmarks[0].landmark:
                        x = int(landmark.x * image.shape[1])
                        y = int(landmark.y * image.shape[0])
                        cv2.circle(image, (x, y), 1, (255, 0, 0), -1)
                    # Extract features for SVM (same as calibration)
                    landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]
                    features = []
                    for lm in landmarks[:10]:
                        features.extend([lm[0], lm[1], lm[2]])
                    features = np.array(features).reshape(1, -1)
                    pred = clf.predict(features)[0]
                    # If prediction matches any calibration label, it's "Looking at screen"
                    if pred in y:
                        label = "Looking at screen"
                    else:
                        label = "Not looking at screen"
                cv2.putText(image, label, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0) if label=="Looking at screen" else (0,0,255), 2)
                cv2.imshow('output window', image)
                key = cv2.waitKey(2) & 0xFF
                if key == 27:
                    print("ESC pressed, exiting classification mode.")  # DEBUG
                    break
        cap.release()
        cv2.destroyAllWindows()


# Indices for iris centers
RIGHT_IRIS_CENTER = 468
LEFT_IRIS_CENTER = 473