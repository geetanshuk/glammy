const base = document.getElementById('base-avatar');
let clothingImg = null;
const canvas = new fabric.Canvas('tryon-canvas');;
const ctx = canvas.getContext('2d');


// Load avatar and detect pose via Flask
fabric.Image.fromURL(baseAvatarUrl, function(avatarImg) {
    avatarImg.set({
        left: 0,
        top: 0,
        selectable: false
    });
    avatarImg.scaleToWidth(canvas.width);
    canvas.add(avatarImg);
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

