import colorsys
import math
import random
import numpy as np
import pygame 

def hsv_to_rgb_np(h, s, v):
    h = h % 1.0
    i = np.floor(h * 6.0)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 -  f) * s)
    i_mod = i.astype(int) % 6

    conditions = [i_mod == k for k in range(6)]
    r = np.select(conditions, [v, q, p, p, t, v])
    g = np.select(conditions, [t, v, v, q, p, p])
    b = np.select(conditions, [p, p, t, v, v, q])
    return r, g, b
