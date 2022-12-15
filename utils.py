from matplotlib import pyplot
import numpy as np


def distanceEuclidienne(v1, v2):
    u1 = np.linalg.norm(v1)
    u2 = np.linalg.norm(v2)
    d = np.linalg.norm((v1/u1)-(v2/u2))
    return d

def norming(v):
    return v/np.linalg.norm(v)

def maximum(v):
    max = 0
    ind = 0
    for i in range(len(v)):
        if v[i] > max:
            ind = i
            max = v[i]
    return (max, ind)


def minimum(v):
    min = v[0]
    ind = 0
    for i in range(len(v)):
        if v[i] < min:
            ind = i
            min = v[i]
    return (min, ind)