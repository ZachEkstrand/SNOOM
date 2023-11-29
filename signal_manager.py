from player import *

class SignalManager:
    def __init__(self, game):
        self.game = game
        self.Permissions = {
            'Player.attack':False,
            'Player.take_damage':True,
            'joysticks':False,
            'D-pad':True,
            'up_pad':True,
            'down_pad':True,
            'right_pad':False,
            'left_pad':False,
            'main_buttons':True,
            'A_button':True,
            'B_button':False,
            'X_button':False,
            'menu_button':False
        }
        
    def emit_signal(self, method, args=None):
        if self.Permissions[method.__qualname__]:
            if args:
                method(args)
            else:
                method()
        else:
            pass