import mediapipe as mp
import cv2
import gaze
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mp_face_mesh = mp.solutions.face_mesh  # initialize the face mesh model
calibration_recordings = []


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

        # Record landmarks if 'r' is pressed and less than 4 sets are recorded
        if key == ord('r') and results.multi_face_landmarks and len(calibration_recordings) < 4:
            landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]
            calibration_recordings.append(landmarks)
            print("Recorded landmarks to screen_bounds.")

        # Print and break if 4 sets are recorded
        if len(calibration_recordings) == 4:
            print(calibration_recordings)
            break

        # Wait for ESC key to exit
        if key == 27:
            break
cap.release()
cv2.destroyAllWindows()

def get_gaze_vector(landmarks, frame_shape):
    # Helper functions for relative and relativeT
    def relative(pt, shape):
        return (int(pt[0] * shape[1]), int(pt[1] * shape[0]))
    def relativeT(pt, shape):
        return (pt[0] * shape[1], pt[1] * shape[0], 0)

    # 2D image points
    image_points = np.array([
        relative(landmarks[4], frame_shape),    # Nose tip
        relative(landmarks[152], frame_shape),  # Chin
        relative(landmarks[263], frame_shape),  # Left eye left corner
        relative(landmarks[33], frame_shape),   # Right eye right corner
        relative(landmarks[287], frame_shape),  # Left Mouth corner
        relative(landmarks[57], frame_shape)    # Right mouth corner
    ], dtype="double")

    image_points1 = np.array([
        relativeT(landmarks[4], frame_shape),
        relativeT(landmarks[152], frame_shape),
        relativeT(landmarks[263], frame_shape),
        relativeT(landmarks[33], frame_shape),
        relativeT(landmarks[287], frame_shape),
        relativeT(landmarks[57], frame_shape)
    ], dtype="double")

    # 3D model points
    model_points = np.array([
        (0.0, 0.0, 0.0),  # Nose tip
        (0, -63.6, -12.5),  # Chin
        (-43.3, 32.7, -26),  # Left eye, left corner
        (43.3, 32.7, -26),  # Right eye, right corner
        (-28.9, -28.9, -24.1),  # Left Mouth corner
        (28.9, -28.9, -24.1)  # Right mouth corner
    ])

    # Eye ball center (3D) - only left
    Eye_ball_center_left = np.array([[29.05], [32.7], [-39.5]])

    # Camera matrix
    focal_length = frame_shape[1]
    center = (frame_shape[1] / 2, frame_shape[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )
    dist_coeffs = np.zeros((4, 1))

    # Solve PnP
    _, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )

    # 2d pupil location (only left)
    left_pupil = relative(landmarks[468], frame_shape)

    # Transformation between image point to world point
    _, transformation, _ = cv2.estimateAffine3D(image_points1, model_points)

    gaze_vectors = []
    origins = []

    if transformation is not None:
        # Left eye only
        pupil_world_cord = transformation @ np.array([[left_pupil[0], left_pupil[1], 0, 1]]).T
        origin_left = Eye_ball_center_left.flatten()
        direction_left = (pupil_world_cord[:3, 0] - origin_left)
        direction_left = direction_left / np.linalg.norm(direction_left)
        origins.append(origin_left)
        gaze_vectors.append(direction_left)
    return origins, gaze_vectors

def project_to_plane(points3d, plane_normal=np.array([0,0,1]), plane_point=None):
    """
    Projects 3D points onto a plane defined by plane_normal and plane_point.
    Returns 2D coordinates in the plane's basis.
    """
    points3d = np.array(points3d)
    if plane_point is None:
        plane_point = np.mean(points3d, axis=0)
    # Create orthonormal basis for the plane
    n = plane_normal / np.linalg.norm(plane_normal)
    # Find a vector not parallel to n
    not_n = np.array([1,0,0]) if abs(n[0]) < 0.9 else np.array([0,1,0])
    v = np.cross(n, not_n)
    v = v / np.linalg.norm(v)
    u = np.cross(n, v)
    # Project points onto plane and get 2D coordinates
    points2d = []
    for p in points3d:
        vec = p - plane_point
        x = np.dot(vec, u)
        y = np.dot(vec, v)
        points2d.append([x, y])
    return np.array(points2d)

def point_in_polygon(point, polygon):
    """
    Ray casting algorithm for 2D point-in-polygon.
    point: (x, y)
    polygon: Nx2 array of vertices
    """
    x, y = point
    poly = polygon
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if min(p1y, p2y) < y <= max(p1y, p2y):
            if x <= max(p1x, p2x):
                xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y+1e-12)+p1x if p2y != p1y else p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def is_gaze_within_bounds(current_origin, current_vector, bounds_origins, bounds_vectors, scale=50):
    """
    Projects the tips of the calibration vectors and the current gaze vector onto a plane,
    and checks if the current gaze tip is inside the polygon formed by the calibration tips.
    """
    # Use average calibration origin as plane point, and normal as z-axis
    plane_point = np.mean(np.array(bounds_origins), axis=0)
    plane_normal = np.array([0,0,1])  # You can use PCA for best-fit, but z=0 is usually fine

    # Compute tip points for calibration vectors
    cal_tips = [o + v * scale for o, v in zip(bounds_origins, bounds_vectors)]
    # Project calibration tips to plane
    cal_tips_2d = project_to_plane(cal_tips, plane_normal, plane_point)
    # Project current gaze tip to plane
    gaze_tip = current_origin + current_vector * scale
    gaze_tip_2d = project_to_plane([gaze_tip], plane_normal, plane_point)[0]
    # Point-in-polygon test
    return point_in_polygon(gaze_tip_2d, cal_tips_2d)

def plot_gaze_vectors(origins_list, vectors_list):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ['r', 'g', 'b', 'm', 'c', 'y']
    for i, (origins, vectors) in enumerate(zip(origins_list, vectors_list)):
        # Only left eye (index 0)
        o = origins[0]
        v = vectors[0]
        ax.quiver(o[0], o[1], o[2], v[0], v[1], v[2], length=50, color=colors[i%len(colors)], label=f'Set {i+1}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.title('Left Eye Gaze Vectors from Calibration')
    plt.show()

if len(calibration_recordings) == 4:
    # Assume a default frame shape (e.g., 480x640) for calculation
    frame_shape = (480, 640, 3)
    bounds_origins = []
    bounds_vectors = []
    for landmarks in calibration_recordings:
        origins, vectors = get_gaze_vector(landmarks, frame_shape)
        bounds_origins.append(origins[0])
        bounds_vectors.append(vectors[0])

    # --- Rolling buffer for gaze vectors and origins ---
    from collections import deque
    buffer_size = 10
    gaze_origin_buffer = deque(maxlen=buffer_size)
    gaze_vector_buffer = deque(maxlen=buffer_size)
    # ---------------------------------------------------

    # Start live classification
    cap = cv2.VideoCapture(0)
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for processing
            results = face_mesh.process(image_rgb)
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)  # Convert back to BGR for display
            label = "No face"
            if results.multi_face_landmarks:
                landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]
                origins, vectors = get_gaze_vector(landmarks, frame_shape)
                if origins and vectors:
                    # --- Add current origin/vector to buffer ---
                    gaze_origin_buffer.append(origins[0])
                    gaze_vector_buffer.append(vectors[0])
                    # --- Compute rolling average if buffer is full ---
                    if len(gaze_origin_buffer) == buffer_size:
                        avg_origin = np.mean(np.array(gaze_origin_buffer), axis=0)
                        avg_vector = np.mean(np.array(gaze_vector_buffer), axis=0)
                        avg_vector = avg_vector / np.linalg.norm(avg_vector)  # Normalize
                        # Draw left eye gaze vector in image coordinates
                        left_pupil = (
                            int(landmarks[468][0] * image.shape[1]),
                            int(landmarks[468][1] * image.shape[0])
                        )
                        inside = is_gaze_within_bounds(avg_origin, avg_vector, bounds_origins, bounds_vectors)
                        label = "Looking at screen" if inside else "Looking away from screen"
                    else:
                        label = "Calibrating..."
            cv2.putText(image, label, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0) if label=="Looking at screen" else (0,0,255), 2)
            # Make text smaller, font size 20
            cv2.putText(image, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0) if label=="Looking at screen" else (0,0,255), 1)
            cv2.imshow('output window', image)
            key = cv2.waitKey(2) & 0xFF
            if key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()


# Indices for iris centers
RIGHT_IRIS_CENTER = 468
LEFT_IRIS_CENTER = 473