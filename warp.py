import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import skimage as ski


def radial_distortion(xy, k1=0.9, k2=0.5):
    """Distort coordinates `xy` symmetrically around their own center."""
    xy_c = xy.max(axis=0) / 2
    xy = (xy - xy_c) / xy_c
    radius = np.linalg.norm(xy, axis=1)
    distortion_model = (1 + k1 * radius + k2 * radius**2) * k2
    xy *= distortion_model.reshape(-1, 1)
    xy = xy * xy_c + xy_c
    return xy


image = np.array(Image.open("C:/Users/kaushag/git/Glammy/glammy/app/static/images/black_skort_h&m_fitted.png"))
image = ski.transform.warp(image, radial_distortion, cval=0.5)


# Pick a few `src` points by hand, and move the corresponding `dst` points to their
# expected positions.
# fmt: off
src = np.array([ [100,  10], [177, 22], [190, 100], [177, 177], [100, 188],
                [22, 177], [ 10, 100], [ 66, 66], [133,  66], [ 66, 133], [133, 133]])
dst = np.array([ [100,   0], [200,  0], [200, 100], [200, 200], [100, 200],
                [ 0, 200], [  0, 100], [ 73, 73], [128,  73], [ 73, 128], [128, 128]])
# fmt: on

# Estimate the TPS transformation from these points and then warp the image.
# We switch `src` and `dst` here because `skimage.transform.warp` requires the
# inverse transformation!
tps = ski.transform.ThinPlateSplineTransform()
tps.estimate(dst, src)
warped = ski.transform.warp(image, tps)


# Plot the results
fig, axs = plt.subplots(1, 2)
axs[0].imshow(image, cmap='gray')
axs[0].scatter(src[:, 0], src[:, 1], marker='x', color='cyan')
axs[1].imshow(warped, cmap='gray', extent=(0, 200, 200, 0))
axs[1].scatter(dst[:, 0], dst[:, 1], marker='x', color='cyan')

point_labels = [str(i) for i in range(len(src))]
for i, label in enumerate(point_labels):
    axs[0].annotate(
        label,
        (src[:, 0][i], src[:, 1][i]),
        textcoords="offset points",
        xytext=(0, 5),
        ha='center',
        color='red',
    )
    axs[1].annotate(
        label,
        (dst[:, 0][i], dst[:, 1][i]),
        textcoords="offset points",
        xytext=(0, 5),
        ha='center',
        color='red',
    )

plt.show()