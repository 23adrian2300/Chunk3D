from utils.config import *
import pygame as pg
import sys
import moderngl as mgl


class VoxelEngine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE,24)
        pg.display.set_mode(WINDOW_RESOLUTION, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags = mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        self.running = True

    def update(self):
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() / 1000
        pg.display.set_caption(f"Voxel Engine | FPS: {self.clock.get_fps() :.0f}")
    def render(self):
        self.ctx.clear(color=BACKGROUND_COLOR, depth=1.0)
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
                pg.quit()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()