import pygame as pg
from sprite_object import *

class Projectile(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/snowball.png',
                 pos=(1, 1), scale=0.15, shift= -0.04, entity='player', angle=1, damage=50):
        super().__init__(game, path, pos, scale, shift)
        self.alive = True
        self.speed = 0.01
        self.entity = entity
        self.angle = angle
        self.damage = damage
        self.target = 'enemy'
        if self.entity == 'enemy':
            self.target = 'player'

    def update(self):
        super().update()
        if self.game.scene_manager.current_scene == 'pause_menu': pass
        else: self.run_logic()

    def run_logic(self):
        if self.alive:
            self.check_wall_collision()
            self.check_target_collision()
            self.movement()

    def check_wall_collision(self):
        if (int(self.x), int(self.y)) in self.game.map.map_diction:
            self.die()

    def die(self):
        if self.dist < 10:
            self.game.sound_manager.play(13)
        self.alive = False
        self.game.object_handler.del_queue.append(self)

    def check_target_collision(self):
        if self.target == 'enemy':
            for enemy in self.game.object_handler.npc_positions:
                enemy_x, enemy_y = self.game.object_handler.npc_positions[enemy]
                dx = self.x -enemy_x
                dy = self.y -enemy_y
                dist_from_enemy = math.hypot(dx, dy)
                if dist_from_enemy <= enemy.hitbox:
                    enemy.take_damage(self.damage)
                    self.die()
        if self.target == 'player':
            if self.dist <= 0.7:
                self.game.signal_manager.emit_signal(self.game.player.take_damage, args=self.damage)
                self.die()

    def movement(self):
        dx = math.cos(self.angle) * self.speed * self.game.delta_time
        dy = math.sin(self.angle) * self.speed * self.game.delta_time
        self.x += dx
        self.y += dy

    @property
    def pos(self):
        return self.x, self.y