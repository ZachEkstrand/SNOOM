from settings import *
import random
import math
import pygame as pg

class Player:
    def __init__(self, game):
        self.game = game
        self.emit_signal = game.signal_manager.emit_signal
        self.sound_manager = game.sound_manager
        self.x, self.y = game.map.player_pos
        self.angle = game.map.player_angle
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.score = 0
        self.ammo = PLAYER_STARTING_AMMO
        self.damage = PLAYER_DAMAGE
        self.candy_canes = 0
        self.key = False
        self.shooting = False
        self.powerup = None
        self.hit_streak = 0
        self.kill_streak = 0
        self.room_num = 1
        self.stunned = False
        self.stun_time = 0

        self.exit_x, self.exit_y = self.game.map.exit_pos

    def new_round(self):
        self.x, self.y = self.game.map.player_pos
        self.angle = self.game.map.player_angle
        self.max_health = PLAYER_HEALTH
        if self.health > self.max_health:
            self.health = self.max_health
        self.key = False
        self.exit_x, self.exit_y = self.game.map.exit_pos
        self.powerup = None
        self.room_num += 1

    def update(self):
        if self.health > self.max_health:
            self.health = self.max_health
        self.check_stun()
        self.check_inputs()
        self.check_door()

    def check_stun(self):
        time_now = pg.time.get_ticks()
        if time_now -self.stun_time >= 1000:
            self.stunned = False

    def check_inputs(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        if self.game.controller_manager:
            self.game.controller_manager.read_controller_inputs()
            self.controller_inputs(dx, dy, speed_sin, speed_cos)

    def check_door(self):
        if self.x > float(self.exit_x):
            self.game.sound_manager.play(16)
            r1 = 0
            r2 = 120000
            w1 = 1000
            w2 = 0
            time_bonus = ((w2 -w1) / (r2 -r1)) * (self.game.scene_manager.round_stopwatch.elapsed_time -r1) +w1
            self.score += max(0, int(time_bonus)) * self.room_num
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.new_round()
        
    def controller_inputs(self, dx, dy, speed_sin, speed_cos):
        controller_manager = self.game.controller_manager
        dx, dy = self.controller_movement(dx, dy, speed_sin, speed_cos)
        self.angle %= math.tau

        self.check_hat('up_pad', -1, 1, 1)
        self.check_hat('down_pad', 1, 1, -1)
        self.check_hat('right_pad', 1, 0, 1)
        self.check_hat('left_pad', -1, 0, -1)

        self.check_button('A_button', 5)
        self.check_button('B_button', 6)
        self.check_button('X_button', 7)
        self.check_button('menu_button', 8)
        
        if round(controller_manager.inputs[3]) == 1 and self.stunned == False:
            self.emit_signal(self.attack)
        if (round(controller_manager.inputs[3]) == -1) and (self.shooting == False) and (self.game.scene_manager.current_scene == 'arena'):
            self.game.signal_manager.Permissions['Player.attack'] = True

        self.check_wall_collision(dx, dy)

    def controller_movement(self, dx, dy, speed_sin, speed_cos):
        controller_manager = self.game.controller_manager
        if self.game.signal_manager.Permissions['joysticks'] and self.stunned == False:
            left = self.get_joy_str(1, controller_manager.inputs[0])
            right = self.get_joy_str(2, controller_manager.inputs[0])
            forward = self.get_joy_str(1, controller_manager.inputs[1])
            backward = self.get_joy_str(2, controller_manager.inputs[1])
            if left:
                dx += speed_sin * -left
                dy += -speed_cos * -left
            if right:
                dx += -speed_sin * right
                dy += speed_cos * right
            if forward:
                dx += speed_cos * -forward
                dy += speed_sin * -forward
            if backward:
                dx += -speed_cos * backward
                dy += -speed_sin * backward

            look_left = self.get_joy_str(1, controller_manager.inputs[2], w1=0.0000000025, w2=0.03)
            look_right = self.get_joy_str(2, controller_manager.inputs[2], w1=0.0000000025, w2=0.03)
            if look_left:
                self.angle += look_left * LOOK_SENSITIVITY * self.game.delta_time

            if look_right:
                self.angle += look_right * LOOK_SENSITIVITY * self.game.delta_time
        return dx, dy

    def get_joy_str(self, mode, vi, r1=0.11, r2=0.99, w1=0.00000025, w2=0.05):
        if mode == 1:
            if vi > -r1:
                return False
            return (-(w2 -w1) / -(r2 -r1)) * (vi +r1) -w1
        if mode == 2:
            if vi < r1:
                return False
            return ((w2 -w1) / (r2 -r1)) * (vi -r1) +w1

    def check_hat(self, name, val, id, active):
        if self.game.signal_manager.Permissions[name] and self.game.controller_manager.inputs[4][id] == active:
            self.game.signal_manager.Permissions[name] = False
            self.sound_manager.play(2)
            if id == 1: self.game.scene_manager.selected_button += val
            else: self.game.scene_manager.column += val
        if self.game.controller_manager.inputs[4][id] != active and self.game.scene_manager.current_scene != 'arena':
            self.game.signal_manager.Permissions[name] = True

    def check_button(self, name, id):
        if self.game.signal_manager.Permissions[name] and self.game.controller_manager.inputs[id] == 1:
            self.game.signal_manager.Permissions[name] = False
            if name == 'A_button':
                self.game.scene_manager.A_down = True
            if name == 'B_button':
                self.game.scene_manager.B_down = True
            if name == 'X_button' and self.stunned == False:
                self.game.scene_manager.X_down = True
            if name == 'menu_button':
                self.game.scene_manager.menu_button_down = True
        if self.game.controller_manager.inputs[id] != 1:
            self.game.signal_manager.Permissions[name] = True

    def attack(self):
        if self.ammo > 0:
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.ammo -= 1
            self.shooting = True

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x +dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y +dy * scale)):
            self.y += dy
    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.map_diction or ((x, y) == self.game.map.exit_pos and self.key)
    
    def take_damage(self, damage):
        self.game.sound_manager.play(random.randint(5, 7)) 
        self.health -= damage
        self.game.controller_manager.rumble(0, 1, 100)
        if self.powerup == 'CATCHER':
            self.ammo += 1
        self.check_game_over()

    def check_game_over(self):
        if self.health < 1:
            self.new_highscore, self.leaderboard_index = self.check_new_highscore()
            self.game.scene_manager.change_scene('game_over')

    def check_new_highscore(self):
        for i, score in enumerate(self.game.leaderboard.scores):
            if int(score) < self.score:
                return True, i
        return False, None
    
    def eat(self):
        if self.candy_canes > 0 and self.health != self.max_health:
            self.sound_manager.play(17)
            self.candy_canes -= 1
            self.health += 25
            if self.health > self.max_health:
                self.health = self.max_health

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)