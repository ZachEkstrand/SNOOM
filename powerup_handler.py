import random
from settings import *

class Powerup_handler:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.powerups = [
            'triple',
            'BEEG',
            'sight',
            'armor',
            'ice',
            'bounce'
        ]
        self.player_powerup = None

    def update(self):
        self.check_powerup(self.player_powerup)

    def check_powerup(self, powerup, just_aquired=False):
        if powerup == 'armor':
            self.player.max_health == PLAYER_HEALTH * 2
            if just_aquired:
                self.player.health == PLAYER_HEALTH * 2
        else:
            self.max_health = PLAYER_HEALTH
        if powerup == 'ice':
            self.player.damage = PLAYER_DAMAGE * 2
        else:
            self.player.damage = PLAYER_DAMAGE

    def pick_powerup(self):
        self.player_powerup = random.choice(self.powerups)
        self.game.player.powerup = self.player_powerup
        self.check_powerup(self.player_powerup, just_aquired=True)
        