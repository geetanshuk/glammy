import cv2
import numpy as np
import mediapipe as mp
import os
import json
from PIL import Image


def detect_key_landmarks(image_name):
    # Load the image with alpha channel preserved
    image = cv2.imread(image_name, cv2.IMREAD_UNCHANGED)

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

    landmarks = []

    # Draw landmarks on BGR image
    if results.pose_landmarks:
        for lm in results.pose_landmarks.landmark:
            landmarks.append({
            'x': lm.x,
            'y': lm.y,
            'z': lm.z,
            'visibility': lm.visibility
        })
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

    base_name = os.path.basename(image_name)

    # save json
    json_path = os.path.join("app/static/data", f"{base_name}_landmarks.json")
    with open(json_path, 'w') as f:
        json.dump(landmarks, f)

    # Save the result
    cv2.imwrite(image_name + "_result.png", output)

    return results, output, alpha, json_path


def overlay_top(avatar_json, clothing_json, avatar_img, clothing_img):
    with open(avatar_json) as f:
        avatar_landmark = json.load(f)
    with open(clothing_json) as f:
        clothing_landmark = json.load(f)
    
    # left shoulder is always 11 in mediapipe
    # getting the left shoulder of the avatar image
    left_shoulder_av = avatar_landmark[11]
    x_val_av = left_shoulder_av["x"]
    y_val_av = left_shoulder_av["y"]
    z_val_av = left_shoulder_av["z"]

    # getting the left shoulder of the clothing image
    left_shoulder_cl = clothing_landmark[11]
    x_val_cl = left_shoulder_cl["x"]
    y_val_cl = left_shoulder_cl["y"]
    z_val_cl = left_shoulder_cl["z"]

    # resize clothing image based on the avatar image
    width_av, height_av = avatar_img.size
    width_cl, height_cl = clothing_img.size

    factor = width_av / width_cl
    clothing_img = clothing_img.resize((width_av, int(factor * height_cl)))

    width_cl, height_cl = clothing_img.size

    # normalized * width gives you the pixel coordinates
    avatar_px_x = x_val_av * width_av
    avatar_px_y = y_val_av * height_av

    clothing_px_x = x_val_cl * width_cl
    clothing_px_y = y_val_cl * height_cl

    # Compute offset to align the landmarks
    offset_x = avatar_px_x - clothing_px_x
    offset_y = avatar_px_y - clothing_px_y
    
    # pasting the image on top of the other
    avatar_img.paste(clothing_img, (int(offset_x), int(offset_y)), mask = clothing_img)

    avatar_img.show()

def snapping():
    # define snapping areas close to the avatar
    snapping_area = 30
    # if avatar's left shoulder - clothing's left shoulder < snapping area
    # switch case to call appropriate overlay method
    
    return 0
 


if __name__ == "__main__":
    avatar_image_path = "app/static/images/realistic_avatar_testing.webp"
    clothing_image_path = "app/static/images/leather_jacket_testing.png"

    avatar_landmark, image_avatar, alpha_background, json_avatar = detect_key_landmarks(avatar_image_path)
    leather_jacket_landmark, image_jacket, alpha_foreground, json_clothing = detect_key_landmarks(clothing_image_path)

    avatar_img = Image.open(avatar_image_path)
    clothing_img = Image.open(clothing_image_path)

    overlay_top(json_avatar, json_clothing, avatar_img, clothing_img)


    
    
