import pygame as pg
from sprite_object import *
from player import *
from npc import *

class Projectile(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/snowball.png',
                 pos=(1, 1), scale=0.15, shift= -0.04, entity='', angle=1, damage=1, powerup=''):
        super().__init__(game, path, pos, scale, shift)
        self.path = path
        self.alive = True
        self.speed = 0.005
        self.powerup = powerup
        self.entity = entity
        self.angle = angle
        self.damage = damage
        self.bounces = 0
        self.bonus = 0
        self.target = 'enemy'
        if isinstance(self.entity, NPC) or isinstance(self.entity, Boss):
            self.target = 'player'
        if self.powerup == 'PITCHER':
            self.speed *= 2
        if self.powerup == '2X DAMAGE':
            self.damage *= 2
        if self.powerup == 'GIANT':
            self.SPRITE_SCALE = 0.5
            self.bonus = 0.1
        self.ignore = []
        self.time_of_spawn = pg.time.get_ticks()

    def update(self):
        if self.game.scene_manager.current_scene == 'pause_menu': pass
        else:
            self.animate_color()
            self.run_logic()
        super().update()

    def animate_color(self):
        colored_surface = False
        root = 'resources/sprites/static_sprites/'
        if self.powerup == '2X DAMAGE':
            colored_surface = self.glow(root +'2x_damage.png')
        if self.powerup == 'BOUNCE':
            colored_surface = self.glow(root +'bounce.png')
        if self.powerup == 'LEECH':
            colored_surface = self.glow(root +'leech.png')
        if self.powerup == 'STUN':
            colored_surface = self.glow(root +'stun.png')
        if self.powerup == 'PITCHER':
            colored_surface = self.glow(root +'pitcher.png')
        if colored_surface:
            self.image = pg.image.load(self.path)
            self.image.blit(colored_surface, (0, 0))

    def glow(self, path):
        colored_surface = pg.image.load(path).convert_alpha()
        freq = 16
        amp = 255 / 2
        time_since_spawn = pg.time.get_ticks() -self.time_of_spawn
        x = time_since_spawn / 1000
        color_alpha = math.cos(x * freq) * amp +(255 / 2)
        colored_surface.set_alpha(color_alpha)
        return colored_surface

    def run_logic(self):
        for i in range(10):
            self.movement()
            if self.check_wall_collision() or self.check_target_collision():
                self.die()
                break

    def check_wall_collision(self):
        if (int(self.x), int(self.y)) in self.game.map.map_diction:
            if self.target == 'enemy':
                self.player.hit_streak = 0
            if self.powerup == 'BOUNCE' and self.bounces < 4:
                if self.check_wall_angle() == 'horizontal':
                    self.angle = 2 * math.pi -self.angle
                elif self.check_wall_angle() == 'vertical':
                    self.angle = math.pi -self.angle
                elif self.check_wall_angle() == 'corner':
                    self.angle = math.pi +self.angle
                self.bounces += 1
                return False
            return True
        return False
    
    def check_wall_angle(self):
        if self.dist_from_center(self.x) < self.dist_from_center(self.y):
            angle = 'horizontal'
        elif self.dist_from_center(self.x) > self.dist_from_center(self.y):
            angle = 'vertical'
        if self.dist_from_center(self.x) == self.dist_from_center(self.y):
            angle = 'corner'

        return angle

    def dist_from_center(self, n):
        nint = n -int(n)
        if nint <= 0.5:
            dist = 0.5 -nint
        if nint > 0.5:
            dist = nint -0.5
        return dist

    def die(self):
        if self.dist < 10:
            self.game.sound_manager.play(13)
        self.alive = False

    def check_target_collision(self):
        if self.target == 'enemy':
            for enemy in self.game.object_handler.npc_list.keys():
                enemy_x, enemy_y = self.game.object_handler.npc_list[enemy]
                dx = self.x -enemy_x
                dy = self.y -enemy_y
                dist_from_enemy = math.hypot(dx, dy)
                if dist_from_enemy <= enemy.hitbox +self.bonus:
                    if enemy not in self.ignore:
                        enemy.take_damage(self.damage, self.powerup)
                    if self.powerup == 'GIANT':
                        self.ignore.append(enemy)
                        return False
                    if self.powerup == 'LEECH':
                        self.player.health += 3
                        if self.player.health > self.player.max_health:
                            self.player.health = self.player.max_health
                    return True
        if self.target == 'player':
            if self.dist <= 0.7 +self.bonus:
                self.game.signal_manager.emit_signal(self.game.player.take_damage, args=self.damage)
                if self.powerup == 'STUN':
                    self.player.stunned = True
                    if self.game.controller_manager:
                        self.game.controller_manager.rumble(1, 0, 1000)
                    self.player.stun_time = pg.time.get_ticks()
                if self.powerup == 'LEECH':
                    self.entity.health += 1
                    if self.entity.health > self.entity.max_health:
                        self.entity.health = self.entity.max_health
                return True
        return False

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = self.speed * self.game.delta_time
        speed_cos = speed * cos_a
        speed_sin = speed * sin_a
        dx = speed_cos
        dy = speed_sin
        self.x += dx / 10
        self.y += dy / 10

    @property
    def pos(self):
        return self.x, self.y