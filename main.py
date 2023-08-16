import sys
import pygame as pg
import asyncio
from settings import *
from map import *
from controller_setup import *
from signal_manager import *
from scene_manager import *
from player import *
from object_renderer import *
from ray_casting import *
from object_handler import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES, #pg.FULLSCREEN
        )
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.XBC = XBController(self)
        self.signal_manager = SignalManager(self)
        self.scene_manager = SceneManager(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)

    def reset_game(self):
        del self.map
        del self.signal_manager
        del self.scene_manager
        del self.player
        del self.object_renderer
        del self.ray_casting
        del self.object_handler
        self.map = Map(self)
        self.signal_manager = SignalManager(self)
        self.scene_manager = SceneManager(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)

    def run(self):
        pg.display.flip()
        self.check_events()
        self.update()
        self.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def update(self):
        self.player.update()
        self.scene_manager.update_scene()
        self.delta_time = self.clock.tick(FPS)

    def draw(self):
        self.scene_manager.draw_scene()

if __name__ == '__main__':
    game = Game()
    while True:
        game.run()