import cv2
import mediapipe as mp
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,  # Set to True for processing single images
    model_complexity=1,      # 0, 1, or 2 (lower complexity is faster)
    smooth_landmarks=True,   # Reduce jitter in landmark movements
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Unpickle the SVM model and scaler
try:
    with open("svm_best_model.pkl", "rb") as f:
        svm_model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
except Exception as e:
    print("Error loading SVM model or scaler:", e)
    exit()

# Initialize MediaPipe drawing utils
mp_drawing = mp.solutions.drawing_utils

# Open the default webcam (camera index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Flip the frame horizontally for a mirror effect (optional)
    frame = cv2.flip(frame, 1)

    # Convert the BGR frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to get pose landmarks
    results = pose.process(rgb_frame)

    # If landmarks are detected, draw them on the frame
    if results.pose_landmarks:
        # Print the number of pose landmarks
        print("Number of pose landmarks:", len(results.pose_landmarks.landmark))
        # Extract xyz coordinates (33 landmarks * 3 = 99 values)
        xyz = []
        for landmark in results.pose_landmarks.landmark:
            xyz.extend([landmark.x, landmark.y, landmark.z])
        # Scale xyz coordinates using the loaded scaler
        xyz_scaled = scaler.transform([xyz])
        xyz_scaled_flat = xyz_scaled.flatten().tolist()
        print("Scaled XYZ coordinates:", xyz_scaled_flat)

        # SVM prediction
        prediction = svm_model.predict([xyz_scaled_flat])[0]
        print("SVM Prediction:", prediction)

        # Optionally, display prediction on the frame
        cv2.putText(frame, f'Prediction: {prediction}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the processed frame
    cv2.imshow('MediaPipe Pose Tracking', frame)

    # Wait for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()