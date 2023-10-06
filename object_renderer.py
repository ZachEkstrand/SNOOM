import pygame as pg
from settings import *

path = 'resources/textures/'

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = game.player
        self.scene_manager = game.scene_manager
        # title_screen
        self.selected_button = 0
        self.title_image_scale = 3
        self.button_font_size = 3
        self.background_image = self.get_texture(path +'background.png', RES)
        self.title = self.get_texture(path +'title.png', (149 * self.title_image_scale, 72 * self.title_image_scale))
        self.start_button_image = self.get_texture(path +'start_game.png', (130 * self.button_font_size, 19 * self.button_font_size))
        self.start_button_shadow = self.get_texture(path +'start_game_shadow.png', (132 * self.button_font_size, 20 * self.button_font_size))
        self.leaderboard_button_image = self.get_texture(path +'leaderboard.png', (155 * self.button_font_size, 19 * self.button_font_size))
        self.leaderboard_button_shadow = self.get_texture(path +'leaderboard_shadow.png', (157 * self.button_font_size, 20 * self.button_font_size))
        # arena
        self.digit_size = 90
        self.sky_offset = 0
        self.tree_offset = 0
        self.wall_textures = {i:self.get_texture(path +f'{i}.png') for i in range(1, 10)}
        self.char_sprites_36x38 = [self.get_texture(f'{path}chars/doom-nightmare-{i}.png', (36 * 2.5, 38 * 2.5)) for i in range(41)]
        self.sky_image = self.get_texture(path +'sky.png', (WIDTH, HALF_HEIGHT))
        self.tree_horizon = self.get_texture(path +'tree_horizon.png', (WIDTH, HALF_HEIGHT))
        self.crosshair_image = self.get_texture(path +'crosshair.png', (31, 31))
        self.snowball_image = self.get_texture('resources/sprites/static_sprites/snowball.png', (64, 64))
        self.key_image = self.get_texture('resources/sprites/static_sprites/key.png', (59, 60))
        self.game_over_image = self.get_texture(path +'game_over.png', (260 * self.title_image_scale, 73 * self.title_image_scale))
        # pause_menu
        self.background_shade = self.get_texture(path +'background_shade.png', RES)
        self.quit_image = self.get_texture(path +'quit.png', (55 * self.button_font_size, 19 * self.button_font_size))
        self.quit_shadow = self.get_texture(path +'quit_shadow.png', (57 * self.button_font_size, 21 * self.button_font_size))
        self.resume_image = self.get_texture(path +'resume.png', (96 * self.button_font_size, 19 * self.button_font_size))
        self.resume_shadow = self.get_texture(path +'resume_shadow.png', (98 * self.button_font_size, 21 * self.button_font_size))
        # leaderboard
        self.general_font_size = 2.5
        self.header_font_size = 3.4
        self.highscores_image = self.get_texture(path +'highscores.png', (152 * self.header_font_size, 19 * self.header_font_size))
        self.char_sprites_18x19 = [self.get_texture(f'{path}chars/doom-nightmare-{i}.png', (18 * self.general_font_size, 19 * self.general_font_size)) for i in range(41)]
        # username input
        self.done_button_image = self.get_texture(path +'done.png', (60 * 1.5, 19 * 1.5))
        self.selected_letter_highlight = self.get_texture(path +'select.png', (40 * self.general_font_size, 46 * self.general_font_size))
    
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def draw_title_screen(self):
        blit = self.screen.blit
        blit(self.background_image, (0, 0))
        blit(self.title, (self.center_on_x(149 * self.title_image_scale), 40))
        if self.scene_manager.selected_button == 0:
            blit(self.start_button_shadow, (self.center_on_x(132 * self.button_font_size), 297))
        if self.scene_manager.selected_button == 1:
            blit(self.leaderboard_button_shadow, (self.center_on_x(157 * self.button_font_size), 387))
        if self.scene_manager.selected_button == 2:
            blit(self.quit_shadow, (self.center_on_x(57 * self.button_font_size), 477))
        blit(self.start_button_image, (self.center_on_x(130 * self.button_font_size), 300))
        blit(self.leaderboard_button_image, (self.center_on_x(155 * self.button_font_size), 390))
        blit(self.quit_image, (self.center_on_x(55 * self.button_font_size), 480))

    @staticmethod
    def center_on_x(x):
        return (WIDTH / 2) -(x / 2)
    
    @staticmethod
    def center_on_y(y):
        return (HEIGHT / 2) -(y / 2)
    
    def draw_leaderboard(self):
        blit = self.screen.blit
        blit(self.background_image, (0, 0))
        blit(self.background_shade, (0, 0))
        blit(self.highscores_image, (self.center_on_x(152 * self.header_font_size), 0))
        names = self.game.leaderboard.names #write to leaderboard.names NOT names
        scores = self.game.leaderboard.scores
        dashes = self.convert_string_to_font([' ', '-', ' ', '-', ' ', '-', ' ', '-', ' '])

        for j, name in enumerate(names):
            c_name = self.convert_string_to_font(name)
            for i, num in enumerate(c_name):
                blit(self.char_sprites_18x19[num], (40 +i * 18 * self.general_font_size, 80 +j * 27 *self.general_font_size))
            for i, num in enumerate(dashes):
                blit(self.char_sprites_18x19[num], (40 +(6 +i) * (18 * self.general_font_size), 80 +j * 27 * self.general_font_size))
            c_score = self.convert_string_to_font(scores[j])
            for i, num in enumerate(c_score):
                blit(self.char_sprites_18x19[num], (40 +(15 +i) * (18 * self.general_font_size), 80 +j * 27 * self.general_font_size))
        
    
    def draw_arena(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_HUD()

    def draw_background(self):
        blit = self.screen.blit
        self.sky_offset = (self.sky_offset +1.4 * self.game.player.rot_speed) % WIDTH
        self.tree_offset = (self.tree_offset +1.6 * self.game.player.rot_speed) % WIDTH
        blit(self.sky_image, (-self.sky_offset, 0))
        blit(self.sky_image, (-self.sky_offset +WIDTH, 0))
        blit(self.tree_horizon, (-self.tree_offset, 0))
        blit(self.tree_horizon, (-self.tree_offset +WIDTH, 0))

        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
    
    def render_game_objects(self):
        blit = self.screen.blit
        list_objects = sorted(self.game.ray_casting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            blit(image, pos)

        blit(self.crosshair_image, (self.center_on_x(31), self.center_on_y(31)))
        blit(self.game.object_handler.weapon.image, (0, 0))

    def draw_HUD(self):
        self.draw_health()
        self.draw_score()
        self.draw_ammo()
        self.draw_key()

    def draw_health(self):
        health = str(self.player.health)
        cmsg = self.convert_string_to_font(health +'%')
        for i, num in enumerate(cmsg):
            self.screen.blit(self.char_sprites_36x38[num], (36 * i * self.general_font_size, 10))

    def draw_score(self):
        score = str(self.player.score)
        cmsg = self.convert_string_to_font(score)
        i = len(cmsg)
        for num in cmsg:
            self.screen.blit(self.char_sprites_18x19[num], (WIDTH -(18 * i * self.general_font_size), 10))
            i -= 1

    def draw_ammo(self):
        blit = self.screen.blit
        ammo = str(self.player.ammo)
        cmsg = self.convert_string_to_font(ammo)
        i = len(cmsg)
        for num in cmsg:
            blit(self.char_sprites_36x38[num], (WIDTH -(30 * i * self.general_font_size) -10, 500))
            i -= 1
        i = len(cmsg)
        cmsg = self.convert_string_to_font('X')
        if i == 2:
            blit(self.char_sprites_18x19[cmsg[0]], (820, 525))
            blit(self.snowball_image, (745, 515))
        if i == 1:
            blit(self.char_sprites_18x19[cmsg[0]], (820 +(30 * self.general_font_size) -10, 525))
            blit(self.snowball_image,(745 +(30 * self.general_font_size) -10, 515))

    def draw_key(self):
        if self.game.player.key:
            self.screen.blit(self.key_image, (WIDTH -70, 70))
    
    def draw_pause_menu(self):
        blit = self.screen.blit

        self.draw_background()
        self.render_game_objects()
        blit(self.background_shade, (0, 0))
        if self.scene_manager.selected_button == 0:
            blit(self.resume_shadow, (self.center_on_x(98 * self.button_font_size), 237))
        if self.scene_manager.selected_button == 1:
            blit(self.quit_shadow, (self.center_on_x(57 * self.button_font_size), 337))
        blit(self.resume_image, (self.center_on_x(96 * self.button_font_size), 240))
        blit(self.quit_image, (self.center_on_x(55 * self.button_font_size), 340))

    def draw_game_over(self):
        blit = self.screen.blit
        self.draw_background()
        self.render_game_objects()
        blit(self.background_shade, (0, 0))
        blit(self.game_over_image, (self.center_on_x(260 * self.title_image_scale), self.center_on_y(73 * self.title_image_scale)))

    def draw_keyboard(self):
        blit = self.screen.blit
        blit(self.background_image, (0, 0))
        blit(self.background_shade, (0, 0))
        blit(self.selected_letter_highlight, (25 +self.game.scene_manager.column * 44 * self.general_font_size, 185 +self.game.scene_manager.selected_button * 52 * self.general_font_size))
        c_letters = self.convert_string_to_font(self.scene_manager.letters)
        for i, num in enumerate(c_letters):
            if i < 9:
                blit(self.char_sprites_36x38[num], (30 +i * 44 * self.general_font_size, 200))
            if i > 8 and i < 18:
                blit(self.char_sprites_36x38[num], (30 +(i -9) * (44 * self.general_font_size), 330))
            if i > 17:
                blit(self.char_sprites_36x38[num], (30 +(i -18) * (44 * self.general_font_size), 460))
        blit(self.done_button_image, (30 +(8 * 44 * self.general_font_size), 487))
        c_username = self.convert_string_to_font(self.scene_manager.username)
        for i, num in enumerate(c_username):
            blit(self.char_sprites_36x38[num], (30 +i * 44 * self.general_font_size, 30))
        c_score = self.convert_string_to_font(str(self.player.score))
        i = len(c_score)
        for num in c_score:
            blit(self.char_sprites_18x19[num], (WIDTH -(18 * i * self.general_font_size), 10))
            i -= 1

    @staticmethod
    def convert_string_to_font(msg):
        cmsg = []
        for char in msg:
            if char == '0':
                cmsg.append(0)
            if char == '1':
                cmsg.append(1)
            if char == '2':
                cmsg.append(2)
            if char == '3':
                cmsg.append(3)
            if char == '4':
                cmsg.append(4)
            if char == '5':
                cmsg.append(5)
            if char == '6':
                cmsg.append(6)
            if char == '7':
                cmsg.append(7)
            if char == '8':
                cmsg.append(8)
            if char == '9':
                cmsg.append(9)
            if char == 'A':
                cmsg.append(10)
            if char == 'B':
                cmsg.append(11)
            if char == 'C':
                cmsg.append(12)
            if char == 'D':
                cmsg.append(13)
            if char == 'E':
                cmsg.append(14)
            if char == 'F':
                cmsg.append(15)
            if char == 'G':
                cmsg.append(16)
            if char == 'H':
                cmsg.append(17)
            if char == 'I':
                cmsg.append(18)
            if char == 'J':
                cmsg.append(19)
            if char == 'K':
                cmsg.append(20)
            if char == 'L':
                cmsg.append(21)
            if char == 'M':
                cmsg.append(22)
            if char == 'N':
                cmsg.append(23)
            if char == 'O':
                cmsg.append(24)
            if char == 'P':
                cmsg.append(25)
            if char == 'Q':
                cmsg.append(26)
            if char == 'R':
                cmsg.append(27)
            if char == 'S':
                cmsg.append(28)
            if char == 'T':
                cmsg.append(29)
            if char == 'U':
                cmsg.append(30)
            if char == 'V':
                cmsg.append(31)
            if char == 'W':
                cmsg.append(32)
            if char == 'X':
                cmsg.append(33)
            if char == 'Y':
                cmsg.append(34)
            if char == 'Z':
                cmsg.append(35)
            if char == '%':
                cmsg.append(36)
            if char == '-':
                cmsg.append(37)
            if char == '(':
                cmsg.append(38)
            if char == ')':
                cmsg.append(39)
            if char == ' ':
                cmsg.append(40)
        return cmsg