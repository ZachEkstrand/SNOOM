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
        self.rel_x = pg.mouse.get_rel()[0]
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
        else:
            self.keyboard_inputs(dx, dy, speed_sin, speed_cos)

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
            dx, dy = self.move(dx, dy, speed_sin, -speed_cos, strength=-left)
            dx, dy = self.move(dx, dy, -speed_sin, speed_cos, strength=right)
            dx, dy = self.move(dx, dy, speed_cos, speed_sin, strength=-forward)
            dx, dy = self.move(dx, dy, -speed_cos, -speed_sin, strength=backward)

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
        
    def keyboard_inputs(self, dx, dy, speed_sin, speed_cos):
        keys = pg.key.get_pressed()
        mouse_buttons = pg.mouse.get_pressed()
        if self.game.signal_manager.Permissions['joysticks'] and self.stunned == False:
            if keys[pg.K_a]:
                dx, dy = self.move(dx, dy, speed_sin, -speed_cos)
            if keys[pg.K_d]:
                dx, dy = self.move(dx, dy, -speed_sin, speed_cos)
            if keys[pg.K_w]:
                dx, dy = self.move(dx, dy, speed_cos, speed_sin)
            if keys[pg.K_s]:
                dx, dy = self.move(dx, dy, -speed_cos, -speed_sin)
            self.angle += (self.rel_x / 6000) * LOOK_SENSITIVITY * self.game.delta_time
        self.angle %= math.tau
        
        self.check_hat('up_pad', -1, pg.K_w, 0, keyboard=keys)
        self.check_hat('down_pad', 1, pg.K_s, 0, keyboard=keys)
        self.check_hat('right_pad', 1, pg.K_d, 0, keyboard=keys)
        self.check_hat('left_pad', -1, pg.K_a, 0, keyboard=keys)

        self.check_button('A_button', 0, mouse=mouse_buttons)
        self.check_button('B_button', pg.K_BACKSPACE, keyboard=keys)
        self.check_button('X_button', pg.K_TAB, keyboard=keys)
        self.check_button('menu_button', pg.K_ESCAPE, keyboard=keys)

        if mouse_buttons[0] and self.stunned == False:
            self.emit_signal(self.attack)
        if mouse_buttons[0] == False and self.shooting == False and self.game.scene_manager.current_scene == 'arena':
            self.game.signal_manager.Permissions['Player.attack'] = True

        self.check_wall_collision(dx, dy)
        
    def move(self, dx, dy, dx_adder, dy_adder, strength=0.050568178977272726):
        if strength:
            dx += dx_adder * strength
            dy += dy_adder * strength
        return dx, dy

    def check_hat(self, name, val, id, active, keyboard=False):
        if keyboard:
            if self.game.signal_manager.Permissions[name] and keyboard[id]:
                self.game.signal_manager.Permissions[name] = False
                self.sound_manager.play(2)
                if id in [pg.K_w, pg.K_s]: self.game.scene_manager.selected_button += val
                else: self.game.scene_manager.column += val
            if keyboard[id] == False and self.game.scene_manager.current_scene != 'arena':
                self.game.signal_manager.Permissions[name] = True
        else:
            if self.game.signal_manager.Permissions[name] and self.game.controller_manager.inputs[4][id] == active:
                self.game.signal_manager.Permissions[name] = False
                self.sound_manager.play(2)
                if id == 1: self.game.scene_manager.selected_button += val
                else: self.game.scene_manager.column += val
            if self.game.controller_manager.inputs[4][id] != active and self.game.scene_manager.current_scene != 'arena':
                self.game.signal_manager.Permissions[name] = True

    def check_button(self, name, id, keyboard=False, mouse=False):
        if keyboard or mouse:
            if self.game.signal_manager.Permissions[name] and (mouse or keyboard)[id]:
                self.game.signal_manager.Permissions[name] = False
                self.toggle_scene_button(name)
            if (mouse or keyboard)[id] == False:
                self.game.signal_manager.Permissions[name] = True
        else:
            if self.game.signal_manager.Permissions[name] and self.game.controller_manager.inputs[id] == 1:
                self.game.signal_manager.Permissions[name] = False
                self.toggle_scene_button(name)
            if self.game.controller_manager.inputs[id] != 1:
                self.game.signal_manager.Permissions[name] = True

    def toggle_scene_button(self, name):
        if name == 'A_button':
            self.game.scene_manager.A_down = True
        if name == 'B_button':
            self.game.scene_manager.B_down = True
        if name == 'X_button' and self.stunned == False:
            self.game.scene_manager.X_down = True
        if name == 'menu_button':
            self.game.scene_manager.menu_button_down = True

    def attack(self):
        if self.ammo > 0:
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.ammo -= 1
            self.shooting = True

    def check_wall_collision(self, dx, dy):
        dx, dy = self.normalize(dx, dy)
        print(math.hypot(dx, dy))
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x +dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y +dy * scale)):
            self.y += dy
    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.map_diction or ((x, y) == self.game.map.exit_pos and self.key)
    
    def normalize(self, dx, dy):
        vec = math.hypot(dx, dy)
        max_dist = PLAYER_SPEED * self.game.delta_time * 0.050568178977272726
        if vec > max_dist:
            mag = max_dist / vec
            dx *= mag
            dy *= mag
        return dx, dy
    
    def take_damage(self, damage):
        self.game.sound_manager.play(random.randint(5, 7)) 
        self.health -= damage
        if self.game.controller_manager:
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