from sprite_object import *
import math

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/player/00.png', scale=HEIGHT, animation_time=50):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.x, self.y = (0, (HEIGHT -self.image.get_height()))
        self.frame_time = animation_time
        self.last_frame = pg.time.get_ticks()

    def update(self):
        if self.player.powerup == 'PITCHER':
            self.frame_time * 0.7
        if self.game.scene_manager.current_scene == 'pause_menu': pass
        else: self.animate()

    def animate(self):
        time_now = pg.time.get_ticks()
        if self.game.player.shooting:
            if self.frame_counter == 0:
                self.frame_counter += 1
                self.last_frame = time_now
                self.images.rotate(-1)
                self.x, self.y = (0, HEIGHT -self.images[0].get_height() -16)
                self.game.sound_manager.play(4, player=True)
            if time_now -self.last_frame > self.frame_time:
                self.images.rotate(-1)
                self.x, self.y = (0, HEIGHT -self.images[0].get_height())
                self.frame_counter += 1
                self.last_frame = time_now
                if self.frame_counter == 2:
                    self.x, self.y = (0, 0)
                if self.frame_counter == 4:
                    self.game.object_handler.spawn_projectile(self.player.pos, 'player', (self.game.player.angle -0.00102), self.player.damage)
                    if self.player.powerup == 'TRIPLE':
                        self.game.object_handler.spawn_projectile(self.game.player.pos, 'player', (self.game.player.angle -0.00102) -math.pi / 16, self.player.damage)
                        self.game.object_handler.spawn_projectile(self.game.player.pos, 'player', (self.game.player.angle -0.00102) +math.pi / 16, self.player.damage)
                if self.frame_counter == len(self.images):
                    self.game.player.shooting = False
                    self.frame_counter = 0

        self.image = self.images[0]