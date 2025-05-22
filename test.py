import cv2
import mediapipe as mp

# Load the image
image_path = "app/static/images/realistic_avatar_testing.webp"
image = cv2.imread(image_path)

# Convert BGR (OpenCV) to RGB (MediaPipe)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)  # Static image mode = better for photos
mp_drawing = mp.solutions.drawing_utils

# Process the image and detect pose landmarks
results = pose.process(image_rgb)

# Draw landmarks if any detected
if results.pose_landmarks:
    mp_drawing.draw_landmarks(
        image,  # Use original BGR image for drawing
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS
    )

# Show the image
cv2.imshow("Pose Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
