import cv2
import mediapipe as mp

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,  # Set to True for processing single images
    model_complexity=1,      # 0, 1, or 2 (lower complexity is faster)
    smooth_landmarks=True,   # Reduce jitter in landmark movements
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

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