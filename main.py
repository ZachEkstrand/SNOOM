import sys
import pygame as pg
from pygame.locals import *
from settings import *
from map import *
from controller_manager import *
from signal_manager import *
from scene_manager import *
from player import *
from object_renderer import *
from ray_casting import *
from object_handler import *
from pathfinding import *
from leaderboard import *
from sound_manager import *
from projectile import *
from powerup_handler import *

class Game:
    def __init__(self):
        pg.init()
        flags = DOUBLEBUF #| FULLSCREEN | SCALED
        self.screen = pg.display.set_mode(RES, flags, 8)
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.e_lines = {
            'start_x':[],
            'start_y':[],
            'end_x':[],
            'end_y':[],
            'next_x':[],
            'next_y':[]
        }
        self.markers = []
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.controller_manager = ControllerManager(self)
        self.sound_manager = SoundManager(self)
        self.signal_manager = SignalManager(self)
        self.scene_manager = SceneManager(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.powerup_handler = Powerup_handler(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = Pathfinding(self)
        self.leaderboard = Leaderboard(self)

    def reset_game(self):
        del self.map
        del self.signal_manager
        del self.scene_manager
        del self.player
        del self.object_renderer
        del self.ray_casting
        del self.object_handler
        del self.pathfinding
        self.map = Map(self)
        self.signal_manager = SignalManager(self)
        self.scene_manager = SceneManager(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = Pathfinding(self)

    def new_round(self):
        del self.map
        del self.signal_manager
        del self.ray_casting
        del self.object_handler
        del self.pathfinding
        self.map = Map(self)
        self.player.new_round()
        self.signal_manager = SignalManager(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = Pathfinding(self)
        self.scene_manager.change_scene('arena')

    def run(self):
        pg.display.flip()
        self.check_events()
        self.update()
        self.draw()
        #self.draw_flat()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.scene_manager.quit or(event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def update(self):
        self.powerup_handler.update()
        self.player.update()
        self.scene_manager.update_scene()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.scene_manager.draw_scene()
        
    def draw_flat(self):
        rays = self.ray_casting.draw_lines
        e_lines = self.e_lines
        scale = 30
        self.screen.fill('black')
        [pg.draw.rect(self.screen, 'darkgray', (pos[0] * scale, pos[1] * scale, scale, scale), 1) for pos in self.map.map_diction]
        [pg.draw.rect(self.screen, 'red', (scale * e_lines['next_x'][i], scale * e_lines['next_y'][i], scale, scale), 1) for i in range(len(e_lines['next_x']))]
        [pg.draw.line(self.screen, 'yellow', (scale * rays['ox'][i], scale * rays['oy'][i]), (scale * rays['ox'][i] + scale * rays['depth'][i] * rays['cos_a'][i], scale * rays['oy'][i] + scale * rays['depth'][i] * rays['sin_a'][i]), 1) for i in range(len(rays['ox']))]
        [pg.draw.circle(self.screen, 'white', (scale * ob.x, scale * ob.y), 5) for ob in self.object_handler.sprite_list if isinstance(ob, Snowpile)]
        [pg.draw.circle(self.screen, 'red', (scale * ob.x, scale * ob.y), 7) for ob in self.object_handler.npc_list if ob.alive]
        pg.draw.circle(self.screen, 'green', (scale * self.player.x, scale * self.player.y), 7)
        [pg.draw.circle(self.screen, 'yellow', (scale * key.x, scale * key.y), 5) for key in self.object_handler.sprite_list if isinstance(key, Key)]
        [pg.draw.circle(self.screen, 'blue', (ob.x * scale, ob.y * scale), 3) for ob in self.object_handler.sprite_list if isinstance(ob, Projectile)]
        [pg.draw.line(self.screen, 'orange', (scale * e_lines['start_x'][i], scale * e_lines['start_y'][i]), (scale * e_lines['end_x'][i], scale * e_lines['end_y'][i]), 1) for i in range(len(e_lines['end_x']))]
        #[pg.draw.circle(self.screen, 'white', (scale * marker[0], scale * marker[1]), 1) for marker in self.markers]
        self.e_lines = {
            'start_x':[],
            'start_y':[],
            'end_x':[],
            'end_y':[],
            'next_x':[],
            'next_y':[]
        }

if __name__ == '__main__':
    game = Game()
    while True:
        game.run()