class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = 'title_screen'
        self.selected_button = 0
        self.A_down = False
        self.menu_button_down = False
    
    def change_scene(self, scene_name):
        self.selected_button = 0
        self.current_scene = scene_name

        self.A_down = False
        self.menu_button_down = False

        if scene_name == 'title_screen':
            self.game.signal_manager.Permissions['Player.controller_fire'] = False
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.signal_manager.Permissions['D-pad'] = True
            self.game.signal_manager.Permissions['up_pad'] = True
            self.game.signal_manager.Permissions['down_pad'] = True
            self.game.signal_manager.Permissions['main_buttons'] = True
            self.game.reset_game()
        if scene_name == 'arena':
            self.game.signal_manager.Permissions['Player.controller_fire'] = True
            self.game.signal_manager.Permissions['joysticks'] = True
            self.game.signal_manager.Permissions['D-pad'] = False
            self.game.signal_manager.Permissions['up_pad'] = False
            self.game.signal_manager.Permissions['down_pad'] = False
            self.game.signal_manager.Permissions['main_buttons'] = True
        if scene_name == 'pause_menu':
            self.game.signal_manager.Permissions['Player.controller_fire'] = False
            self.game.signal_manager.Permissions['joysticks'] = False
            self.game.signal_manager.Permissions['D-pad'] = True
            self.game.signal_manager.Permissions['up_pad'] = True
            self.game.signal_manager.Permissions['down_pad'] = True
            self.game.signal_manager.Permissions['main_buttons'] = True

    def update_scene(self):
        if self.current_scene == 'title_screen':
            self.title_screen_update()
        elif self.current_scene == 'arena':
            self.arena_update()
        elif self.current_scene == 'pause_menu':
            self.pause_menu_update()

    def arena_update(self):
        game = self.game
        game.ray_casting.update()
        game.object_handler.update()
        if self.menu_button_down:
            self.change_scene('pause_menu')

    def title_screen_update(self):
        if self.selected_button > 1:
            self.selected_button = 0
        if self.selected_button < 0:
            self.selected_button = 1
        elif self.A_down:
            if self.selected_button == 0:
                self.change_scene('arena')

    def pause_menu_update(self):
        game = self.game
        if self.selected_button > 1:
            self.selected_button = 0
        if self.selected_button < 0:
            self.selected_button = 1
        elif self.A_down:
            if self.selected_button == 0:
                self.change_scene('arena')
            if self.selected_button == 1:
                self.change_scene('title_screen')
        game.ray_casting.update()
        game.object_handler.update()

    def draw_scene(self):
        game = self.game
        if self.current_scene == 'title_screen':
            game.object_renderer.draw_title_screen()
        elif self.current_scene == 'arena':
            game.object_renderer.draw_arena()
        elif self.current_scene == 'pause_menu':
            game.object_renderer.draw_pause_menu()