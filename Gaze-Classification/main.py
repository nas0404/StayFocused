import mediapipe as mp
import cv2
import gaze

mp_face_mesh = mp.solutions.face_mesh  # initialize the face mesh model
screen_bounds = []


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
                # Record landmarks if 'r' is pressed
                if cv2.waitKey(1) and 0xFF == ord('r') and len(screen_bounds) < 4:
                    # Extract landmark coordinates as a list of (x, y, z) tuples
                    landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]
                    screen_bounds.append(landmarks)
                    print
                    print("Recorded landmarks to screen_bounds.")
                elif cv2.waitKey(1) & len(screen_bounds) == 4:
                    print(screen_bounds)
                    break
            except Exception as e:
                print(f"Error in gaze.gaze: {e}")

        cv2.imshow('output window', image)
        # Wait for ESC key to exit, otherwise continue
        if cv2.waitKey(2) & 0xFF == 27 or len(screen_bounds) > 4:
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
if len(screen_bounds) == 4:
    plot_screen_bounds(screen_bounds)
# filepath: c:\Users\bryan\OneDrive\Desktop\StayFocused\Gaze_estimation-master\main2.py

