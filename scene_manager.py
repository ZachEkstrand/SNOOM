import pygame as pg
import random
from timer_handler import *

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.sound_manager = game.sound_manager
        self.current_scene = 'title_screen'
        self.quit = False
        self.selected_button = 0
        self.column = 0
        self.A_down = False
        self.menu_button_down = False
        self.round_stopwatch = None
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        self.sound_manager.set_volume(0, 0.3)
        self.sound_manager.play(0, loops=-1, fade_ms=1000)
    
    def change_scene(self, scene_name, reset_game=False, unpause=False):
        self.current_scene = scene_name
        self.selected_button = 0 # acting as self.row
        self.column = 0
        self.username = []

        self.A_down = False
        self.B_down = False
        self.X_down = False
        self.menu_button_down = False

        if scene_name == 'title_screen':
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.signal_manager.Permissions['up_pad'] = True
            self.game.signal_manager.Permissions['down_pad'] = True
            self.game.signal_manager.Permissions['right_pad'] = False
            self.game.signal_manager.Permissions['left_pad'] = False
            if reset_game:
                self.game.reset_game()
        if scene_name == 'leaderboard':
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.signal_manager.Permissions['up_pad'] = True
            self.game.signal_manager.Permissions['down_pad'] = True
            self.game.signal_manager.Permissions['right_pad'] = False
            self.game.signal_manager.Permissions['left_pad'] = False
            if reset_game:
                self.game.reset_game()
        if scene_name == 'arena':
            self.sound_manager.set_music_volume(0.8)
            self.sound_manager.set_sfx_volume(1)
            if unpause:
                self.sound_manager.unpause()
            if self.sound_manager.get_busy(1) == False or self.sound_manager.get_track() == self.sound_manager.tracks[11]:
                self.sound_manager.play(random.randint(0, 8), sfx=False, fade_ms=500)
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.game.signal_manager.Permissions['Player.take_damage'] = True
            self.game.signal_manager.Permissions['joysticks'] = True
            self.game.signal_manager.Permissions['up_pad'] = False
            self.game.signal_manager.Permissions['down_pad'] = False
            self.game.signal_manager.Permissions['right_pad'] = False
            self.game.signal_manager.Permissions['left_pad'] = False
        if scene_name == 'pause_menu':
            self.sound_manager.pause()
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.signal_manager.Permissions['up_pad'] = True
            self.game.signal_manager.Permissions['down_pad'] = True
            self.game.signal_manager.Permissions['right_pad'] = False
            self.game.signal_manager.Permissions['left_pad'] = False
        if scene_name == 'game_over':
            self.sound_manager.set_sfx_volume(0.25)
            self.sound_manager.queue(11)
            self.sound_manager.fade_music()
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.game.signal_manager.Permissions['Player.take_damage'] = False
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.signal_manager.Permissions['up_pad'] = False
            self.game.signal_manager.Permissions['down_pad'] = False
            self.game.signal_manager.Permissions['right_pad'] = False
            self.game.signal_manager.Permissions['left_pad'] = False
        if scene_name == 'keyboard':
            self.sound_manager.queue(10)
            self.sound_manager.fade_music()
            self.game.signal_manager.Permissions['Player.attack'] = False
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.signal_manager.Permissions['up_pad'] = True
            self.game.signal_manager.Permissions['down_pad'] = True
            self.game.signal_manager.Permissions['right_pad'] = True
            self.game.signal_manager.Permissions['left_pad'] = True

    def update_scene(self):
        if self.current_scene == 'title_screen':
            self.title_screen_update()
        elif self.current_scene == 'leaderboard':
            self.leaderboard_update()
        if self.current_scene == 'arena':
            self.arena_update()
        elif self.current_scene == 'pause_menu':
            self.pause_menu_update()
        elif self.current_scene == 'game_over':
            self.game_over_update()
        elif self.current_scene == 'keyboard':
            self.keyboard_update()

    def title_screen_update(self):
        if self.selected_button > 2:
            self.selected_button = 0
        if self.selected_button < 0:
            self.selected_button = 2
        elif self.A_down:
            if self.selected_button == 0:
                self.sound_manager.play(1)
                self.change_scene('arena')
            if self.selected_button == 1:
                self.sound_manager.play(3)
                self.change_scene('leaderboard')
            if self.selected_button == 2:
                self.quit = True

    def leaderboard_update(self):
        if self.A_down:
            self.sound_manager.play(3)
            self.change_scene('title_screen')

    def arena_update(self):
        game = self.game
        game.ray_casting.update()
        game.object_handler.update()
        if self.round_stopwatch:
            self.round_stopwatch.update(game.delta_time)
        if self.sound_manager.get_queue() == None:
            if self.sound_manager.get_track() == self.sound_manager.tracks[9]:
                self.sound_manager.queue(9)
            else:
                self.sound_manager.queue(random.randint(0, 8))
        if self.X_down:
            self.game.player.eat()
            self.X_down = False
        if self.menu_button_down:
            self.sound_manager.play(1)
            self.change_scene('pause_menu')

    def pause_menu_update(self):
        game = self.game
        game.ray_casting.update()
        game.object_handler.update()
        if self.selected_button > 1:
            self.selected_button = 0
        if self.selected_button < 0:
            self.selected_button = 1
        elif self.A_down:
            self.sound_manager.play(3)
            if self.selected_button == 0:
                self.change_scene('arena', unpause=True)
            if self.selected_button == 1:
                self.change_scene('title_screen', reset_game=True)
        elif self.menu_button_down:
            self.sound_manager.play(3)
            self.change_scene('arena', unpause=True)

    def game_over_update(self):
        game = self.game
        game.ray_casting.update()
        game.object_handler.update()
        if self.sound_manager.get_busy(1) == False:
            self.sound_manager.play(11, sfx=False, loops=-1)
        if self.A_down:
            if game.player.new_highscore:
                self.change_scene('keyboard')
            else:
                self.change_scene('title_screen', reset_game=True)
    
    def keyboard_update(self):
        if self.selected_button > 2:
            self.selected_button = 0
        if self.selected_button < 0 :
            self.selected_button = 2
        if self.column > 8:
            self.column = 0
        if self.column < 0:
            self.column = 8
        if self.sound_manager.get_busy(1) == False:
            self.sound_manager.play(10, sfx=False, loops=-1)
        if self.A_down:
            self.sound_manager.play(3)
            self.A_down = False
            if self.column != 8 or self.selected_button != 2:
                if len(self.username) < 6:
                    self.username.append(self.letters[self.column +self.selected_button * 9])
            if self.selected_button == 2 and self.column == 8 and len(self.username) > 0:
                self.game.leaderboard.add_entry(self.username)
                self.change_scene('leaderboard', reset_game=True)
        elif self.B_down:
            self.sound_manager.play(3)
            self.B_down = False
            if len(self.username) > 0:
                self.username.pop()

    def draw_scene(self):
        game = self.game
        if self.current_scene == 'title_screen':
            game.object_renderer.draw_title_screen()
        elif self.current_scene == 'leaderboard':
            game.object_renderer.draw_leaderboard()
        elif self.current_scene == 'arena':
            game.object_renderer.draw_arena()
        elif self.current_scene == 'pause_menu':
            game.object_renderer.draw_pause_menu()
        elif self.current_scene == 'game_over':
            game.object_renderer.draw_game_over()
        elif self.current_scene == 'keyboard':
            game.object_renderer.draw_keyboard()

    def start_round_stopwatch(self):
        if self.round_stopwatch == None:
            self.round_stopwatch = Stopwatch(pg.time.get_ticks())