import mediapipe as mp
import cv2
import gaze
from sklearn import svm
import numpy as np

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

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D plotting

def plot_screen_bounds(screen_bounds):
    """
    Plots 4 sets of xyz coordinates as a 3D shape using matplotlib.
    Each set in screen_bounds should be a list of (x, y, z) tuples.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, landmarks in enumerate(screen_bounds):
        xs = [pt[0] for pt in landmarks]
        ys = [pt[1] for pt in landmarks]
        zs = [pt[2] for pt in landmarks]
        ax.scatter(xs, ys, zs, label=f'Set {i+1}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()
if len(calibration_recordings) == NUM_CALIBRATION:
    # --- SVM Training ---
    # Example: Use the first 10 landmarks' (x, y, z) as features for each recording
    # You can change this to use more/different features as needed
    X = []
    y = []
    for i, landmarks in enumerate(calibration_recordings):
        # Flatten first 10 landmarks (x, y, z) into a feature vector
        features = []
        for lm in landmarks[:10]:
            features.extend([lm[0], lm[1], lm[2]])
        X.append(features)
        y.append(i)  # Dummy label: each recording gets a unique label (replace with real labels as needed)
    X = np.array(X)
    y = np.array(y)
    clf = svm.SVC(kernel='linear')
    clf.fit(X, y)
    print("SVM trained on calibration recordings.")

    plot_screen_bounds(calibration_recordings)


# Indices for iris centers
RIGHT_IRIS_CENTER = 468
LEFT_IRIS_CENTER = 473