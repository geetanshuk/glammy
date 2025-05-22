const canvas = new fabric.Canvas('tryon-canvas');
let clothingImg = null;

// Load avatar and detect pose via Flask
fabric.Image.fromURL(baseAvatarUrl, function(avatarImg) {
    avatarImg.set({
        left: 0,
        top: 0,
        selectable: false
    });
    avatarImg.scaleToWidth(canvas.width);
    canvas.add(avatarImg);

    // Send avatar image to Flask for pose detection
    sendImageToServer(avatarImg.getElement());
});

// Load clothing image
fabric.Image.fromURL(clothingUrl, function(img) {
    clothingImg = img;
    clothingImg.set({
        left: 120,
        top: 200,
        hasControls: false,
        hasBorders: false,
        selectable: true,
        originX: 'center',
        originY: 'center'
    });
    clothingImg.scale(0.4);
    canvas.add(clothingImg);
});

// Send image to Flask backend for pose detection
function sendImageToServer(imageElement) {
    const canvasTemp = document.createElement('canvas');
    canvasTemp.width = imageElement.naturalWidth;
    canvasTemp.height = imageElement.naturalHeight;
    const ctx = canvasTemp.getContext('2d');
    ctx.drawImage(imageElement, 0, 0);

    canvasTemp.toBlob((blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'avatar.png');

        fetch('/detect_pose', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.keypoints) {
                alignClothingFromServer(data.keypoints);
            } else {
                console.error("Pose detection failed:", data);
            }
        })
        .catch(err => console.error('Error sending image:', err));
    }, 'image/png');
}

// Align clothing based on shoulder landmarks from backend
function alignClothingFromServer(landmarks) {
    const lShoulder = landmarks[11];
    const rShoulder = landmarks[12];

    const midX = ((lShoulder.x + rShoulder.x) / 2) * canvas.width;
    const midY = ((lShoulder.y + rShoulder.y) / 2) * canvas.height;

    const angleRad = Math.atan2(
        rShoulder.y - lShoulder.y,
        rShoulder.x - lShoulder.x
    );
    const angleDeg = angleRad * (180 / Math.PI);

    const shoulderWidth = Math.abs(rShoulder.x - lShoulder.x) * canvas.width;

    if (clothingImg) {
        clothingImg.set({
            left: midX,
            top: midY,
            angle: angleDeg
        });

        clothingImg.scaleToWidth(shoulderWidth * 1.5); // adjust scale as needed
        canvas.requestRenderAll();
    }
}
