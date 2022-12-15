import numpy as np
from matplotlib import pyplot

# à un array n*m*p (image colorée) associe un array nm (image grise)


def to_grey(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    gray = gray.astype(int)
    return gray


def grayscale(img):
    G = np.zeros(img.shape[:2])
    G = img[:, :, 0] * 0.3 + img[:, :, 1] * 0.59 + img[:, :, 2] * 0.11
    G = G.astype(int)
    pyplot.imshow(G)
    pyplot.show()


# à un array en BGR associe un array en RGB (et vice versa après)
def BRtoRB(bgr):
    rgb = np.zeros(bgr.shape)
    rgb[:, :, 0] = bgr[:, :, 2]
    rgb[:, :, 1] = bgr[:, :, 1]
    rgb[:, :, 2] = bgr[:, :, 0]
    return rgb
