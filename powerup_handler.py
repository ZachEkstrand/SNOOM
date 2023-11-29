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
            'STUN',#9
            'COMBO',#10
        ]
        self.player_powerup = None

    def pick_powerup(self):
        self.player_powerup = random.choice(self.powerups)
        if self.player_powerup == 'ARMOR':
            self.player.max_health = PLAYER_HEALTH * 2
            self.player.health = PLAYER_HEALTH * 2
        self.game.player.powerup = self.player_powerup
        self.game.object_renderer.create_header(self.player_powerup, 255, animation_type='slide')
        