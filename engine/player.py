import pygame as pg
from engine.camera import *
from utils.config import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POSITION, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * PLAYER_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * PLAYER_SENSITIVITY)

    def keyboard_control(self):
        keys = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        if keys[pg.K_w]:
            self.move_forward(vel)
        if keys[pg.K_s]:
            self.move_back(vel)
        if keys[pg.K_a]:
            self.move_left(vel)
        if keys[pg.K_d]:
            self.move_right(vel)
        if keys[pg.K_q]:
            self.move_up(vel)
        if keys[pg.K_e]:
            self.move_down(vel)
