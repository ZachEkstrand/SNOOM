import random
from sprite_object import *

path = 'resources/sprites/npc/'
class NPC(AnimatedSprite): #elf cadet
    def __init__(self, game, path=path +'soldier/0.png',pos=(1, 1),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.path = path
        self.attack_images = self.get_images(self.path +'/attack')
        self.death_images = self.get_images(self.path +'/death')
        self.pain_images = self.get_images(self.path +'pain')
        self.walk_immages = self.get_images(self.path +'walk')

        self.point_give = 7
        self.attack_dist = 3
        self.speed = 0.025
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.alive = True
        self.pain = False
