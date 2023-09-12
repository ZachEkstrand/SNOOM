import pygame as pg
from sprite_object import *

class Projectile(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/snowball.png',
                 pos=(1, 1), scale=0.15, shift= -0.04, angle=1, entity='player'):
        super().__init__(game, path, pos, scale, shift)
        self.alive = True
        self.speed = 0.3
        self.angle = angle
        self.entity = entity

    def update(self):
        super().update()
        if self.game.scene_manager.current_scene == 'pause_menu': pass
        else: self.run_logic()

    def run_logic(self):
        if self.alive:
            self.check_wall_collision()
            self.movement()

    def check_wall_collision(self):
        if (int(self.x), int(self.y)) in self.game.map.map_diction:
            self.die()

    def die(self):
        self.alive = False
        self.game.object_handler.del_queue.append(self)

    def movement(self):
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        self.x += dx
        self.y += dy

    @property
    def pos(self):
        return self.x, self.y