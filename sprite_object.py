import pygame as pg
import os
from collections import deque
from settings import *

class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candy_cane.png',
                 pos=(10.5, 3.5), scale=0.6, shift=0.5):
        self.game = game
        self.alive = True
        self.x, self.y = pos
        self.player = game.player
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        self.proj_width = proj_width
        self.screen_image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        self.screen_pos = self.screen_x -self.sprite_half_width, HALF_HEIGHT -proj_height // 2 +height_shift

        self.game.ray_casting.objects_to_render.append((self.norm_dist, self.screen_image, self.screen_pos))

    def get_sprite(self):
        self.proj_width = 0
        dx = self.x -self.player.x
        dy = self.y -self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta -self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS +delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH +self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def rumble(self, low=1, high=1, duration=1):
        if self.game.controller_manager:
            self.game.controller_manager.rumble(low, high, duration)

    def update(self):
        self.get_sprite()

    @property
    def pos(self):
        return (self.x, self.y)
    
    @property
    def map_pos(self):
        return (int(self.x), int(self.y))

class Tree(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/tree.png',
                 pos=(1, 1), scale=2, shift=-0.2):
        super().__init__(game, path, pos, scale, shift)

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        
        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x -self.sprite_half_width, HALF_HEIGHT -proj_height // 2 +height_shift

        if self.dist > 3 and self.dist < 15:
            self.game.ray_casting.objects_to_render.append((self.norm_dist, image, pos))

class Snowpile(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/snowpile.png',
                 pos=(1, 1), scale=1, shift=0.12):
        super().__init__(game, path, pos, scale, shift)

    def update(self):
        super().update()
        self.check_collision_on_player()

    def check_collision_on_player(self):
        if self.dist < 0.5:
            self.alive = False
            self.game.sound_manager.play(12)
            self.game.player.ammo += 3
            self.rumble(1, 1, 1)

class CandyCane(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/candy_cane.png',
                 pos=(1, 1), scale=0.6, shift=0.5):
        super().__init__(game, path, pos, scale, shift)

    def update(self):
        super().update()
        self.check_collision_on_player()

    def check_collision_on_player(self):
        if self.dist < 0.5:
            self.alive = False
            self.game.sound_manager.play(18)
            self.game.player.candy_canes += 1
            self.rumble(1, 1, 1)

class Key(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/key.png',
                 pos=(1, 1), scale=0.3, shift=0):
        super().__init__(game, path, pos, scale, shift)
        self.time_of_spawn = pg.time.get_ticks()
        self.game.sound_manager.play(14)
    
    def update(self):
        if self.game.scene_manager.current_scene == 'pause_menu':
            pass 
        else:
            self.check_collision_on_player()
            self.move()
        super().update()

    def check_collision_on_player(self):
        if self.dist < 0.5:
            self.alive = False
            self.game.sound_manager.play(15)
            self.game.player.key = True
            self.rumble(1, 1, 1)

    def move(self):
        freq = 2
        amp = 0.3
        time_since_spawn = pg.time.get_ticks() -self.time_of_spawn
        x = time_since_spawn / 1000
        self.SPRITE_HEIGHT_SHIFT = math.cos(x * freq) * amp

class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/power_cane/0.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False
    
    def get_images(self, path):
        images = deque()
        files = os.listdir(path)
        files.sort()
        for file_name in files:
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path +'/' +file_name).convert_alpha()
                images.append(img)
        return images
    
    def update(self):
        self.check_animation_time()
        self.animate(self.images)
        super().update()

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now -self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True
    
    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

class PowerCane(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/animated_sprites/power_cane/0.png',
                 pos=(0, 0), scale=0.6, shift=0.5, animation_time=120):
        super().__init__(game, path, pos, scale, shift, animation_time)
        
    def update(self):
        super().update()
        self.check_collision_on_player()

    def check_collision_on_player(self):
        if self.dist < 0.5:
            self.alive = False
            self.game.sound_manager.play(18)
            self.player.score += 50
            self.rumble(1, 1, 1)
            self.game.powerup_handler.pick_powerup()