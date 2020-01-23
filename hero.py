from __future__ import division
import time

import pygame
import hero_tools as ht

pygame.init()

ht.init_matrix()

ht.set_pixel((0,2))
ht.set_pixel_clr((0,2), ht.WS_GREEN)
