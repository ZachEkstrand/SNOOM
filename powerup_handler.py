import random
from settings import *

class Powerup_handler:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.powerups = [
            'TRIPLE',#0
            'GIANT',#1
            'SIGHT',#2
            'ARMOR',#3
            '2X DAMAGE',#4
            'BOUNCE',#5
            'LEECH',#6
            'CATCHER',#7
            'PITCHER',#8
            'STUN'#9
        ]
        self.player_powerup = None

    def update(self):
        self.check_powerup(self.player_powerup)

    def check_powerup(self, powerup, just_aquired=False):
        if powerup == 'ARMOR':
            self.player.max_health = PLAYER_HEALTH * 2
            if just_aquired:
                self.player.health = PLAYER_HEALTH * 2
        else:
            self.max_health = PLAYER_HEALTH
        if powerup == '2X DAMAGE':
            self.player.damage = PLAYER_DAMAGE * 2
        else:
            self.player.damage = PLAYER_DAMAGE

    def pick_powerup(self):
        self.player_powerup = random.choice(self.powerups)
        self.game.player.powerup = self.player_powerup
        self.check_powerup(self.player_powerup, just_aquired=True)
        self.game.object_renderer.create_header(self.player_powerup, 255, animation_type='slide')
        