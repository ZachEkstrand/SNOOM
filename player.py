from settings import *

class Player:
    def __init__(self, game):
        self.game = game
        self.emit_signal = game.signal_manager.emit_signal
        self.sound_handler = game.sound_handler
        self.sfx = game.sound_handler.sfx
        self.XBC = game.XBC
        self.x, self.y = game.map.player_pos
        self.angle = game.map.player_angle
        self.health = PLAYER_MAX_HEALTH
        self.score = 0
        self.ammo = PLAYER_STARTING_AMMO
        self.key = False
        self.rot_speed = 0
        self.shooting = False

        self.exit_x, self.exit_y = self.game.map.exit_pos

    def new_round(self):
        self.x, self.y = self.game.map.player_pos
        self.angle = self.game.map.player_angle
        self.health = PLAYER_MAX_HEALTH
        self.key = False
        self.exit_x, self.exit_y = self.game.map.exit_pos

    def update(self):
        self.game.XBC.read_controller_inputs()
        self.xbc_inputs()
        if self.x > float(self.exit_x):
            self.game.new_round()
        
    def xbc_inputs(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        self.rot_speed = 0
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        rv1 = 0.11
        rv2 = 0.99
        wv1 = 0.0005
        wv2 = 0.05

        self.joy_str_0 = 0
        self.joy_str_1 = 0
        self.joy_str_2 = 0

        # joysticks
        if self.game.signal_manager.Permissions['joysticks']:
            if self.XBC.inputs[1] < -rv1:
                self.joy_str_1 = (-(wv2 -wv1) / -(rv2 -rv1)) * (self.XBC.inputs[1] +rv1) -wv1
                dx += speed_cos * -self.joy_str_1
                dy += speed_sin * -self.joy_str_1
            if self.XBC.inputs[1] > rv1:
                self.joy_str_1 = ((wv2 -wv1) / (rv2 -rv1)) * (self.XBC.inputs[1] -rv1) +wv1
                dx += -speed_cos * self.joy_str_1
                dy += -speed_sin * self.joy_str_1
            if self.XBC.inputs[0] < -rv1:
                self.joy_str_0 = (-(wv2 -wv1) / -(rv2 -rv1)) * (self.XBC.inputs[0] +rv1) -wv1
                dx += speed_sin * -self.joy_str_0
                dy += -speed_cos * -self.joy_str_0
            if self.XBC.inputs[0] > rv1:
                self.joy_str_0 = ((wv2 -wv1) / (rv2 -rv1)) * (self.XBC.inputs[0] -rv1) +wv1
                dx += -speed_sin * self.joy_str_0
                dy += speed_cos * self.joy_str_0

            if self.XBC.inputs[2] > rv1:
                self.joy_str_2 = ((wv2 -wv1) / (rv2 -rv1)) * (self.XBC.inputs[2] -rv1) +wv1
                self.angle += self.joy_str_2 * LOOK_SENSITIVITY
                self.rot_speed = self.joy_str_2 * PLAYER_ROT_SPEED

            if self.XBC.inputs[2] < -rv1:
                self.joy_str_2 = (-(wv2 -wv1) / -(rv2 -rv1)) * (self.XBC.inputs[2] +rv1) -wv1
                self.angle += self.joy_str_2 * LOOK_SENSITIVITY
                self.rot_speed = self.joy_str_2 * PLAYER_ROT_SPEED

        self.angle %= math.tau

        # D-pad
        if self.game.signal_manager.Permissions['D-pad']:
            if self.game.signal_manager.Permissions['up_pad'] and self.XBC.inputs[4][1] == 1:
                self.game.scene_manager.selected_button -= 1
                self.game.signal_manager.Permissions['up_pad'] = False
                self.sound_handler.play(2)
            if self.XBC.inputs[4][1] != 1:
                self.game.signal_manager.Permissions['up_pad'] = True

            if self.game.signal_manager.Permissions['down_pad'] and self.XBC.inputs[4][1] == -1:
                self.game.scene_manager.selected_button += 1
                self.game.signal_manager.Permissions['down_pad'] = False
                self.sound_handler.play(2)
            if self.XBC.inputs[4][1] != -1:
                self.game.signal_manager.Permissions['down_pad'] = True

            if self.game.signal_manager.Permissions['right_pad'] and self.XBC.inputs[4][0] == 1:
                self.game.scene_manager.column += 1
                self.game.signal_manager.Permissions['right_pad'] = False
                self.sound_handler.play(2)
            if self.XBC.inputs[4][0] != 1:
                self.game.signal_manager.Permissions['right_pad'] = True

            if self.game.signal_manager.Permissions['left_pad'] and self.XBC.inputs[4][0] == -1:
                self.game.scene_manager.column -= 1
                self.game.signal_manager.Permissions['left_pad'] = False
                self.sound_handler.play(2)
            if self.XBC.inputs[4][0] != -1:
                self.game.signal_manager.Permissions['left_pad'] = True

        # buttons
        if self.game.signal_manager.Permissions['main_buttons']:
            if self.game.signal_manager.Permissions['A_button'] and self.XBC.inputs[5] == 1:
                self.game.scene_manager.A_down = True
                self.game.signal_manager.Permissions['A_button'] = False
            if self.XBC.inputs[5] != 1:
                self.game.scene_manager.A_down = False
                self.game.signal_manager.Permissions['A_button'] = True

            if self.game.signal_manager.Permissions['B_button'] and self.XBC.inputs[6] == 1:
                self.game.scene_manager.B_down = True
                self.game.signal_manager.Permissions['B_button'] = False
            if self.XBC.inputs[6] != 1:
                self.game.scene_manager.B_button = False
                self.game.signal_manager.Permissions['B_button'] = True
        
            if self.game.signal_manager.Permissions['menu_button'] and self.XBC.inputs[7] == 1:
                self.game.scene_manager.menu_button_down = True
                self.game.signal_manager.Permissions['menu_button'] = False
            if self.XBC.inputs[7] != 1:
                self.game.scene_manager.menu_button_down = False
                self.game.signal_manager.Permissions['menu_button'] = True
        
        # trigger
        if round(self.XBC.inputs[3]) == 1:
            self.emit_signal(self.attack)
        if (round(self.XBC.inputs[3]) == -1) and (self.shooting == False) and (self.game.scene_manager.current_scene == 'arena'):
            self.game.signal_manager.Permissions['Player.attack'] = True

        self.check_wall_collision(dx, dy)

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
        self.health -= damage
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

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)