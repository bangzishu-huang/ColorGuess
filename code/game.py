import math
import random
import sys
import pygame

from config import (WIDTH, HEIGHT, FPS, WHEEL_RADIUS, WHEEL_CENTER, ROUND_TIME, STARTING_LIVES, PERFECT_PX, GREAT_PX, GOOD_PX, POINTS, BG_TOP, BG_BOTTOM, TEXT_COLOR, MUTED_TEXT, JUDGEMENT_COLORS)
from easing import ease_out_cubic, ease_out_back, lerp, lerp_color
from color_wheel import generate_wheel_surface, color_at_offset, random_point_in_wheel