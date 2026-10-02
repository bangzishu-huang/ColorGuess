import colorsys
import math
import random
import pygame 
from easing import ease_out_back, ease_out_cubic

class Particle:
    __slots__ = ('x', 'y', 'vx', 'color', 'age', 'life', 'size')

    def __init__(self, x, y, color, burst_strength=1.0):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(60, 240) * burst_strength
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.age = 0.0
        self.life = random.uniform(0.5, 1.0)
        self.size = random.uniform(2.5, 5.5)

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 260 * dt
        self.vx *= 0.985
        self.vy *= 0.99

    def alive(self):
        return self.age < self.life

    def draw(self, surf):
        t = self.age / self.life
        alpha = max(0, int(255 * (1 - t)))
        size = max(1, self.size * (1 - t * 0.6))
        col = (*self.color, alpha)
        pygame.draw.circle(surf, col, (int(self.x), int(self.y)), int(size))

class FloatingText:
    def __init__(self, x, y, text, color, size=30, rise=70, life=0.9):
        self.x = x
        self.y = y
        self.text = text 
        self.color = color
        self.size = size
        self.rise = rise
        self.age = 0.0
        self.life = life 

    def update(self, dt):
        self.age += dt

    def alive(self):
        return self.age < self.life

    def draw(self, surf, font):
        t = self.age / self.life 
        eased = ease_out_cubic(t)
        y = self.y - self.rise * eased
        alpha = int(255 * (1 - t) ** 1.5)
        pop = 1.0 + 0.25 * (1 - ease_out_cubic(min(1.0, t * 2.2))) if t < 0.45 else 1.0
        img = font.render(self.text, True, self.color)
        if pop != 1.0:
            w, h = img.get_size()
            img = pygame.transform.smoothscale(img, (max(1, int(w * pop)), max(1, int(h * pop))))
            img.set_alpha(alpha)
            rect = img.get_rect(center=(self.x, y))
            surf.blit(img, rect)

class Blob:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.r = random.uniform(120, 220)
        self.speed = random.uniform(0.05, 0.15)
        self.phase = random.uniform(0, math.tau)
        self.hue = random.random()

    def draw(self, surf, t):
        x = self.x + math.sin(t * self.speed + self.phase) * 80
        y = self.y + math.cos(t * self.speed + self.phase) * 60
        hue = (self.hue + t * 0.01) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 0.35)
        col = (int(r * 255), int(g * 255), int(b * 255), 18)
        pygame.draw.circle(surf, col, (int(x), int(y)), int(self.r))