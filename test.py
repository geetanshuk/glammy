import cv2
import numpy as np
import mediapipe as mp
import os

def detect_key_landmarks(image_name):
    # Load the image with alpha channel preserved
    image_path = "app/static/images/" + image_name 
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)


    # Separate channels if alpha exists
    if image.shape[2] == 4:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]
    else:
        bgr = image
        alpha = None

    # Convert BGR to RGB for MediaPipe
    image_rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    mp_drawing = mp.solutions.drawing_utils

    # Process the image and detect pose landmarks
    results = pose.process(image_rgb)

    bgr = np.ascontiguousarray(bgr)

    # Draw landmarks on BGR image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            bgr,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # Recombine with alpha channel if it existed
    if alpha is not None:
        output = cv2.merge([bgr, alpha])
    else:
        output = bgr

    image_name = os.path.splitext(image_name)[0]
    # Save the result
    cv2.imwrite("app/static/images/" + image_name + "_result.png", output)

    return results, output, alpha

# def remove_background(image):
#     mp_selfie_segmentation = mp.solutions.selfie_segmentation
#     selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)

#     results = selfie_segmentation.process(image)
#     mask = results.segmentation_mask

#     h, w = image.shape[:2]
    
#     rgba_image = np.zeros((h, w, 4), dtype=np.uint8)
#     rgba_image[:, :, :3] = image

#     # Set alpha channel: 255 (opaque) where condition True, else 0 (transparent)
#     rgba_image[:, :, 3] = (mask > 0.5).astype(np.uint8) * 255

#     cv2.imwrite("app/static/images/no_background.png", rgba_image)
#     return rgba_image


def overlay_image(background, foreground):
    # Ensure 4 channels
    if background.shape[2] != 4:
        background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA)
    if foreground.shape[2] != 4:
        foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2BGRA)

    # Resize foreground to match background
    foreground = cv2.resize(foreground, (background.shape[1], background.shape[0]))

    # Extract alpha masks
    alpha_fg = foreground[:, :, 3] / 255.0
    alpha_bg = background[:, :, 3] / 255.0

    # Blend each channel
    result = np.zeros_like(background, dtype=np.uint8)
    for c in range(3):  # BGR channels
        result[:, :, c] = (
            foreground[:, :, c] * alpha_fg +
            background[:, :, c] * alpha_bg * (1 - alpha_fg)
        ).astype(np.uint8)

    # Blend alpha channel
    result[:, :, 3] = ((1 - (1 - alpha_fg) * (1 - alpha_bg)) * 255).astype(np.uint8)

    return result

if __name__ == "__main__":
    avatar_landmark, image_avatar, alpha_background = detect_key_landmarks("realistic_avatar_testing.webp")
    leather_jacket_landmark, image_jacket, alpha_foreground = detect_key_landmarks("leather_jacket_testing.png")
    
    #remove_background(image_jacket)

    # result = overlay_image(image_avatar, image_jacket)
    # cv2.imshow("result", result)

    
    
