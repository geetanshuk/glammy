import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.transform import ThinPlateSplineTransform, warp

# --- Load Avatar Image and Detect Pose ---
image = Image.open("C:/Users/kaushag/git/Glammy/glammy/app/static/images/real_model.png").convert("RGBA")
image_np = np.array(image)
h, w = image_np.shape[:2]

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
results = pose.process(cv2.cvtColor(np.array(image)[..., :3], cv2.COLOR_RGBA2RGB))

if not results.pose_landmarks:
    print("No pose landmarks found.")
    exit()

landmarks = results.pose_landmarks.landmark

# --- Define Destination Points (on avatar) ---
dst = np.array([
    [landmarks[23].x * w, landmarks[23].y * h],  # Left hip
    [landmarks[24].x * w, landmarks[24].y * h],  # Right hip
    [((landmarks[23].x + landmarks[24].x) / 2) * w, ((landmarks[23].y + landmarks[24].y) / 2 + 0.12) * h]  # Bottom center, slightly below hips
], dtype=np.float32)

# --- Load Clothing Image with Transparency ---
clothing = Image.open("C:/Users/kaushag/git/Glammy/glammy/app/static/images/grey_cargo_testing.jpg").convert("RGBA")
clothing_np = np.array(clothing)
h_c, w_c = clothing_np.shape[:2]

# --- Define Source Points (on clothing) ---
src = np.array([
    [0.1 * w_c, 0.7 * h_c],   # Left waist
    [0.9 * w_c, 0.7 * h_c],   # Right waist
    [0.5 * w_c, 0.95 * h_c],  # Bottom center of skort
], dtype=np.float32)

# --- Separate RGB and Alpha channels ---
clothing_rgb = clothing_np[..., :3] / 255.0
clothing_alpha = clothing_np[..., 3] / 255.0

# --- Estimate TPS transform and warp ---
tps = ThinPlateSplineTransform()
tps.estimate(src, dst)

warped_rgb = warp(clothing_rgb, tps, output_shape=(h, w))
warped_alpha = warp(clothing_alpha, tps, output_shape=(h, w))

# --- Merge back RGBA ---
warped_rgba = np.dstack((warped_rgb, warped_alpha))

# --- Show the Results ---
plt.figure(figsize=(10, 5))
plt.imshow(image_np)
plt.imshow(warped_rgba, alpha=warped_alpha)
plt.title("Fitted Skort on Avatar")
plt.axis("off")
plt.show()
