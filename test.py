import insightface
import cv2
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model
from PIL import Image
import numpy as np

# Get the model hub (automatically downloads and caches models)
model = insightface.app.FaceAnalysis(name='buffalo_l')  # 'buffalo_l' is a popular model pack
model.prepare(ctx_id=-1)  # 0 for GPU, -1 for CPU

# Load swapper model
swapper = get_model(r"C:Users\kaushag\.insightface\models\inswapper_128.onnx",
    download=False)

# Load images
source_img = cv2.cvtColor(cv2.imread("source.jpeg"), cv2.COLOR_BGR2RGB)
target_img = cv2.cvtColor(cv2.imread("target.png"), cv2.COLOR_BGR2RGB)

# Detect faces
source_face = model.get(source_img)[0]
target_face = model.get(target_img)[0]

# Perform face swap
result = swapper.get(target_img, target_face, source_face)

# Save output
cv2.imwrite("swapped.jpg", cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
