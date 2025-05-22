from flask import Flask, render_template, request, jsonify
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/detect_pose", methods=['POST'])
def detect_pose():
    file = request.files['image']
    image = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
        return jsonify({'error': 'No landmarks detected'}), 400

    # Get coordinates
    keypoints = {}
    for idx, landmark in enumerate(results.pose_landmarks.landmark):
        keypoints[idx] = {'x': landmark.x, 'y': landmark.y, 'z': landmark.z}

    return jsonify({'keypoints': keypoints})

if __name__ == '__main__':
    app.run(debug=True)
