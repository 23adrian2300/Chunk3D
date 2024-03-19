from utils.config import *
import pygame as pg
import sys
import moderngl as mgl
from engine.shader_program import *
from engine.scene import *
from engine.player import *


class Engine:
    def __init__(self):
        self.scene = None
        self.shader_program = None
        self.player = None
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        pg.display.set_mode(WINDOW_RESOLUTION, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.BLEND)
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        self.running = True
        self.on_init()
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

    def on_init(self):
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() / 1000
        pg.display.set_caption(f"Voxel Engine | FPS: {self.clock.get_fps() :.0f}")

    def render(self):
        self.ctx.clear(color=BACKGROUND_COLOR, depth=1.0)
        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()
