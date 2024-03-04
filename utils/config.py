from numba import njit
import numpy as np
import glm
import math

WINDOW_RESOLUTION = glm.vec2(1280, 720)
BACKGROUND_COLOR = glm.vec4(0.1, 0.1, 0.1, 1.0)