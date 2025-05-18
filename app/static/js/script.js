const canvas = document.getElementById('tryon-canvas');
const ctx = canvas.getContext('2d');

const avatar = new Image();
avatar.src = baseAvatarUrl;
avatar.onload = () => {
    ctx.drawImage(avatar, 0, 0, canvas.width, canvas.height);
};