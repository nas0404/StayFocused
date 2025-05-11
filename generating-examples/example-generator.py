

import cv2
import mediapipe as mp
import csv
import os
import time

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change to the target directory relative to the script's location
os.chdir(script_dir)

# Verify the current working directory
print("Current working directory:", os.getcwd())

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
 
# Initialize Mediapipe Drawing
mp_drawing = mp.solutions.drawing_utils
 
# Create folders if they don't exist
os.makedirs('captured_frames', exist_ok=True)
 
# Open webcam
cap = cv2.VideoCapture(0)
 
# Create separate CSV files for logits and coordinates
logits_file = 'logits.csv'
coordinates_file = 'coordinates.csv'

# Ensure headers are written for new files
logits_header_written = False
coordinates_header_written = False
 
# Open CSV files for logits and coordinates
with open(logits_file, mode='a', newline='') as logits_f, open(coordinates_file, mode='a', newline='') as coords_f:
    logits_writer = csv.writer(logits_f)
    coords_writer = csv.writer(coords_f)
 
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty frame.")
            continue
 
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
 
        # Display frame with landmarks for visualization only
        display_frame = frame.copy()
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                display_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
 
        cv2.imshow('Mediapipe Pose Detection', display_frame)
 
        key = cv2.waitKey(5) & 0xFF
 
        if key == ord('q'):
            break

        # Capture plain webcam image
        if key == ord('c'):
            timestamp = int(time.time() * 1000)  # milliseconds
            unique_id = f"plain_{timestamp}"
            plain_image_filename = f"captured_frames/{unique_id}.jpg"
            cv2.imwrite(plain_image_filename, frame)
            print(f"Captured plain image: {plain_image_filename}")
 
        if results.pose_landmarks:
            if key == ord('a'):
                label = 'ACTIVE'
            elif key == ord('i'):
                label = 'INACTIVE'
            else:
                label = None
 
            if label:
                # Save the plain frame (without landmarks) as an image
                timestamp = int(time.time() * 1000)  # milliseconds
                unique_id = f"{label.lower()}_{timestamp}"
                image_filename = f"captured_frames/{unique_id}.jpg"
                cv2.imwrite(image_filename, frame)  # Save the plain frame
                print(f"Saved plain image: {image_filename}")
 
                # Extract logits (example: visibility values as logits)
                logits = [lm.visibility for lm in results.pose_landmarks.landmark]
                logits_row = [unique_id] + logits + [label]

                if not logits_header_written:
                    logits_header = ['unique_id'] + [f'logit{i}' for i in range(len(logits))] + ['label']
                    logits_writer.writerow(logits_header)
                    logits_header_written = True

                logits_writer.writerow(logits_row)
                print(f"Appended logits to {logits_file} with label: {label}")

                # Extract coordinates
                coordinates = []
                for lm in results.pose_landmarks.landmark:
                    coordinates.extend([lm.x, lm.y, lm.z])
                coordinates_row = [unique_id] + coordinates + [label]

                if not coordinates_header_written:
                    coordinates_header = ['unique_id'] + [f'coord{i}' for i in range(len(coordinates))] + ['label']
                    coords_writer.writerow(coordinates_header)
                    coordinates_header_written = True

                coords_writer.writerow(coordinates_row)
                print(f"Appended coordinates to {coordinates_file} with label: {label}")
 
cap.release()
cv2.destroyAllWindows()