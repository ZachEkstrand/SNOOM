import pygame as pg
from settings import *
from sprite_object import *

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
        self.wall_textures = {i:self.get_texture(path +f'{i}.png') for i in range(1, 10)}
        self.char_sprites_36x38 = [self.get_texture(f'{path}chars/doom-nightmare-{i}.png', (36 * 2.5, 38 * 2.5)) for i in range(41)]
        self.crosshair_image = self.get_texture(path +'crosshair.png', (31, 31))
        self.snowball_image = self.get_texture('resources/sprites/static_sprites/snowball.png', (64, 64))
        self.candy_cane_image = self.get_texture('resources/sprites/static_sprites/candy_cane_item.png', (64 // 2, 143 // 2))
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

        self.del_queue = []
        self.new_round()
    
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def new_round(self):
        self.header_list = []
        self.create_header('ROOM ' +str(self.player.room_num), 0)

    def create_header(self, text, alpha, animation_type='fade'):
        self.header_list.append(Header(self, text, alpha, animation_type))

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

        del_indexes = []
        for i, header in enumerate(self.header_list):
            if header in self.del_queue:
                del_indexes.append(i)
        if del_indexes:
            del_indexes.sort(reverse=True)
        for i in del_indexes:
            del self.header_list[i]

    def draw_background(self):
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, 0, WIDTH, HEIGHT))
    
    def render_game_objects(self):
        blit = self.screen.blit
        list_objects = sorted(self.game.ray_casting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            blit(image, pos)
        blit(self.crosshair_image, (self.center_on_x(31), self.center_on_y(31)))
        blit(self.game.object_handler.weapon.image, self.game.object_handler.weapon.pos)

    def draw_HUD(self):
        self.draw_health()
        self.draw_score()
        self.draw_ammo()
        self.draw_candy_canes()
        self.draw_key()
        self.draw_mini_map()
        [header.update() for header in self.header_list]

    def draw_health(self):
        health = str(self.player.health)
        font_string = self.convert_string_to_font(health +'%')
        for i, num in enumerate(font_string):
            self.screen.blit(self.char_sprites_36x38[num], (36 * i * self.general_font_size, 10))

    def draw_score(self):
        score = str(self.player.score)
        font_string = self.convert_string_to_font(score)
        i = len(font_string)
        for num in font_string:
            self.screen.blit(self.char_sprites_18x19[num], (WIDTH -(18 * i * self.general_font_size), 10))
            i -= 1

    def draw_ammo(self):
        blit = self.screen.blit
        ammo = str(self.player.ammo)
        font_string = self.convert_string_to_font(ammo)
        i = len(font_string)
        for num in font_string:
            blit(self.char_sprites_36x38[num], (WIDTH -(30 * i * self.general_font_size) -10, 500))
            i -= 1
        i = len(font_string)
        font_string = self.convert_string_to_font('X')
        if i == 2:
            blit(self.char_sprites_18x19[font_string[0]], (820, 525))
            blit(self.snowball_image, (745, 515))
        if i == 1:
            blit(self.char_sprites_18x19[font_string[0]], (820 +(30 * self.general_font_size) -10, 525))
            blit(self.snowball_image,(745 +(30 * self.general_font_size) -10, 515))

    def draw_candy_canes(self):
        blit = self.screen.blit
        candy_canes = str(self.player.candy_canes)
        font_string = self.convert_string_to_font(candy_canes)
        i = len(font_string)
        for num in font_string:
            blit(self.char_sprites_36x38[num], (WIDTH -(30 * i * self.general_font_size) -10, 400))
            i -= 1
        i = len(font_string)
        font_string = self.convert_string_to_font('X')
        if i == 2:
            blit(self.char_sprites_18x19[font_string[0]], (820, 425))
            blit(self.candy_cane_image, (770, 400))
        if i == 1:
            blit(self.char_sprites_18x19[font_string[0]], (820 +(30 * self.general_font_size) -10, 425))
            blit(self.candy_cane_image, (770 +(30 * self.general_font_size) -10, 400))

    def draw_key(self):
        if self.game.player.key:
            self.screen.blit(self.key_image, (WIDTH -70, 70))

    def draw_mini_map(self):
        scale = 5
        door = self.game.map.exit_pos
        mini_map = pg.Surface((32 * scale, 32 * scale))
        mini_map.set_alpha(200)
        
        [pg.draw.rect(mini_map, (75, 75, 75), ((pos[0] * scale), (pos[1] * scale), scale, scale), 0) for pos in self.game.map.map_diction if pos != door]
        pg.draw.rect(mini_map, 'yellow', (door[0] * scale, door[1] * scale, scale, scale), 0)
        pg.draw.circle(mini_map, 'green', (self.player.x * scale, self.player.y * scale), 2)
        if self.player.powerup == 'sight':
            [pg.draw.circle(mini_map, 'red', (enemy.x * scale, enemy.y * scale), 2) for enemy in self.game.object_handler.npc_list if enemy.alive]
            [pg.draw.circle(mini_map, 'white', (sprite.x * scale, sprite.y * scale), 2) for sprite in self.game.object_handler.sprite_list if isinstance(sprite, Snowpile)]
        if self.game.object_handler.key_pos and self.player.key == False:
            pg.draw.circle(mini_map, 'yellow', (self.game.object_handler.key_pos[0] * scale, self.game.object_handler.key_pos[1] * scale), 1)
        self.screen.blit(mini_map, (10, 300))

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
    def convert_string_to_font(string):
        string = string.upper()
        font_string = []
        for char in string:
            if char == '0':
                font_string.append(0)
            if char == '1':
                font_string.append(1)
            if char == '2':
                font_string.append(2)
            if char == '3':
                font_string.append(3)
            if char == '4':
                font_string.append(4)
            if char == '5':
                font_string.append(5)
            if char == '6':
                font_string.append(6)
            if char == '7':
                font_string.append(7)
            if char == '8':
                font_string.append(8)
            if char == '9':
                font_string.append(9)
            if char == 'A':
                font_string.append(10)
            if char == 'B':
                font_string.append(11)
            if char == 'C':
                font_string.append(12)
            if char == 'D':
                font_string.append(13)
            if char == 'E':
                font_string.append(14)
            if char == 'F':
                font_string.append(15)
            if char == 'G':
                font_string.append(16)
            if char == 'H':
                font_string.append(17)
            if char == 'I':
                font_string.append(18)
            if char == 'J':
                font_string.append(19)
            if char == 'K':
                font_string.append(20)
            if char == 'L':
                font_string.append(21)
            if char == 'M':
                font_string.append(22)
            if char == 'N':
                font_string.append(23)
            if char == 'O':
                font_string.append(24)
            if char == 'P':
                font_string.append(25)
            if char == 'Q':
                font_string.append(26)
            if char == 'R':
                font_string.append(27)
            if char == 'S':
                font_string.append(28)
            if char == 'T':
                font_string.append(29)
            if char == 'U':
                font_string.append(30)
            if char == 'V':
                font_string.append(31)
            if char == 'W':
                font_string.append(32)
            if char == 'X':
                font_string.append(33)
            if char == 'Y':
                font_string.append(34)
            if char == 'Z':
                font_string.append(35)
            if char == '%':
                font_string.append(36)
            if char == '-':
                font_string.append(37)
            if char == '(':
                font_string.append(38)
            if char == ')':
                font_string.append(39)
            if char == ' ':
                font_string.append(40)
        return font_string
    
class Header:
    def __init__(self, object_renderer, text, alpha, animation_type):
        BLACK = (0, 0, 0)
        self.alpha = alpha
        self.text = text
        self.object_renderer = object_renderer
        self.animation_type = animation_type
        self.surface = pg.Surface((int(len(text) * 36 * 2.5), int(38 * 2.5)))
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.x = WIDTH

        self.surface.fill(BLACK)
        self.surface.set_colorkey(BLACK)
        self.font_string = object_renderer.convert_string_to_font(text)

        for i, num in enumerate(self.font_string):
            self.surface.blit(self.object_renderer.char_sprites_36x38[num], (36 * i * 2.5, 0))
        self.animation_phase = 1

    def update(self):
        self.animate()

    def animate(self):
        object_renderer = self.object_renderer
        blit = object_renderer.game.screen.blit
        time_now = pg.time.get_ticks()
        if self.animation_type == 'fade':
            x = object_renderer.center_on_x(self.width)
            y = 200
            stop_time = 1000
            if self.animation_phase == 1:
                self.surface.set_alpha(self.alpha)
                self.alpha += 10
                blit(self.surface, (x, y))
                if self.alpha >= 256:
                    self.alpha = 255
                    self.animation_phase = 2
                    self.timer_start = time_now
            elif self.animation_phase == 2:
                blit(self.surface, (x, y))
                if time_now -self.timer_start > stop_time:
                    self.animation_phase = 3
            elif self.animation_phase == 3:
                self.surface.set_alpha(self.alpha)
                self.alpha -= 11
                blit(self.surface, (x, y))
                if self.alpha <= 0:
                    object_renderer.del_queue.append(self)
        if self.animation_type == 'slide':
            y = 100
            center_x = object_renderer.center_on_x(self.width)
            stop_time = 1000
            if self.animation_phase == 1:
                self.x -= 30
                if self.x <= center_x:
                    self.x = center_x
                    self.animation_phase = 2
                    self.timer_start = time_now
                blit(self.surface, (self.x, y))
            elif self.animation_phase == 2:
                blit(self.surface, (self.x, y))
                if time_now -self.timer_start > stop_time:
                    self.animation_phase = 3
            elif self.animation_phase == 3:
                self.x -= 35
                blit(self.surface, (self.x, y))
                if self.x <= -self.width:
                    object_renderer.del_queue.append(self)
