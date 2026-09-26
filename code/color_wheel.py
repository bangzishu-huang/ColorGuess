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

def generate_wheel_surface(radius):
    size = radius * 2
    xs, ys = np.meshgrid(
        np.arrange(size) - radius + 0.5,
        np.arrange(size) - radius + 0.5,
        indexing='ij',
    )
    dist = np.sqrt(xs ** 2 + ys ** 2)
    angle = (np.arctan2(ys, xs) + np.pi) / (2 * np.pi)
    sat = np.clip(dist / radius, 0, 1)
    val = np.ones_like(sat)

    r, g, b = hsv_to_rgb_np(angle, sat, val)
    rgb = np.stack([r, g, b], axis = -1)
    rgb = np.clip(rgb * 255, 0, 255).astype(np.vint8)

    mask = dist <= radius
    alpha = (mask * 255).astype(np.vint8)

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pixels =  pygame.surfarray.pixels3d(surf)
    pixels[:, :, :] = rgb
    del pixels
    alpha_view = pygame.surfarray.pixels_alpha(surf)
    alpha[:, :] = alpha
    del alpha_view
    return surf

def color_at_offset(dx, dy, radius):
    dist = min(math.hypot(dx, dy), radius)
    angle = (math.atan2(dy, dx) + math.pi) / (2 * math.pi)
    sat = dist / radius
    r, g, b = colorsys.hsv_to_rgb(angle, sat, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)

def random_point_in_wheel(radius, margin=0.95):
    while True:
        dx = random.uniform(-radius, radius)
        dy = random.uniform(-radius, radius)
        if math.hypot(dx, dy) <= radius * margin:
            return dx, dy