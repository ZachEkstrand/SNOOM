from sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/player/00.png', scale=HEIGHT, animation_time=70):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.num_images = len(self.images)
        self.frame_counter = 0

    def update(self):
        if self.game.scene_manager.current_scene == 'pause_menu': pass
        else:
            self.check_animation_time()
            self.animate()

    def animate(self):
        if self.game.player.shooting:
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == 4:
                    self.game.object_handler.spawn_projectile(self.game.player.pos, 'player', (self.game.player.angle -0.00102) +(self.game.player.joy_str_0 * 3) +(self.game.player.joy_str_2 * 6)
                                                              )
                if self.frame_counter == self.num_images:
                    self.game.player.shooting = False
                    self.frame_counter = 0