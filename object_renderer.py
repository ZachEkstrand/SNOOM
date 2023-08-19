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
        self.wall_textures = self.load_wall_textures()
        self.digit_images = [self.get_texture(f'{path}digits/{i}.png', [self.digit_size] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.sky_image = self.get_texture(path +'sky.png', (WIDTH, HALF_HEIGHT))
        self.tree_horizon = self.get_texture(path +'unnamed.png', (WIDTH, HALF_HEIGHT))
        self.snowball_image = self.get_texture('resources/sprites/static_sprites/snowball.png', (64, 64))
        self.blood_screen = self.get_texture(path +'blood_screen.png', RES)
        self.game_over_image = self.get_texture(path +'game_over.png', RES)
        self.win_image = self.get_texture(path +'win.png', RES)
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
        self.char_sprites = [self.get_texture(f'{path}chars/doom-nightmare-{i}.png', (18 * self.general_font_size, 19 * self.general_font_size)) for i in range(41)]
        # username input
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.username = []
        self.column = 0
        self.row = 0
        self.done_button_image = self.get_texture(path +'done.png', (60 * 1.5, 19 * 1.5))
        self.selected_letter_highlight = self.get_texture(path +'select.png', (40 * self.general_font_size, 46 * self.general_font_size))
        

    def load_wall_textures(self):
        return {
            1:self.get_texture(path +'1.png'),
            2:self.get_texture(path +'2.png'),
            3:self.get_texture(path +'3.png'),
            4:self.get_texture(path +'4.png'),
            5:self.get_texture(path +'5.png')
        }
    
    
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
    
    def draw_arena(self):
        self.draw_background()
        self.render_game_objects()

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
        list_objects = sorted(self.game.ray_casting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
    
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