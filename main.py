import sys
import pygame as pg
from pygame.locals import *
from settings import *
from map import *
from controller_setup import *
from signal_manager import *
from scene_manager import *
from player import *
from object_renderer import *
from ray_casting import *
from object_handler import *
from pathfinding import *
from leaderboard import *
from sound_manager import *

class Game:
    def __init__(self):
        pg.init()
        flags = DOUBLEBUF #| FULLSCREEN | SCALED
        self.screen = pg.display.set_mode(RES, flags, 8
        )
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.XBC = XBController(self)
        self.sound_manager = SoundManager(self)
        self.signal_manager = SignalManager(self)
        self.scene_manager = SceneManager(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = Pathfinding(self)
        self.leaderboard = Leaderboard(self)

    def reset_game(self):
        del self.map
        del self.signal_manager
        del self.scene_manager
        del self.player
        del self.object_renderer
        del self.object_handler
        del self.pathfinding
        self.map = Map(self)
        self.signal_manager = SignalManager(self)
        self.scene_manager = SceneManager(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = Pathfinding(self)

    def new_round(self):
        del self.map
        del self.signal_manager
        del self.ray_casting
        del self.object_handler
        del self.pathfinding
        self.map = Map(self)
        self.signal_manager = SignalManager(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = Pathfinding(self)
        self.scene_manager.change_scene('arena')
        self.player.new_round()

    def run(self):
        pg.display.flip()
        self.check_events()
        self.draw_flat()
        self.update()
        s#elf.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.scene_manager.quit or(event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def update(self):
        self.player.update()
        self.scene_manager.update_scene()
        self.delta_time = self.clock.tick(FPS)

    def draw(self):
        self.scene_manager.draw_scene()
        
    def draw_flat(self):
        scale = 30
        self.screen.fill('black')
        [pg.draw.rect(self.screen, 'darkgray', (pos[0] * scale, pos[1] * scale, scale, scale), 1) for pos in self.map.map_diction]
        pg.draw.circle(self.screen, 'green', (self.player.x * scale, self.player.y * scale), 7)

if __name__ == '__main__':
    game = Game()
    while True:
        game.run()