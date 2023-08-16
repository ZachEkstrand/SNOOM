from player import *

class SignalManager:
    def __init__(self, game):
        self.game = game
        self.Permissions = {
            'XBController.read_controller_inputs':True,
            'Player.xbc_inputs':True,
            'Player.controller_fire':False,
            'joysticks':False,
            'D-pad':True,
            'up_pad':True,
            'down_pad':True,
            'main_buttons':True,
            'A_button':True,
            'menu_button':False
        }
        
    def emit_signal(self, method):
        if self.Permissions[method.__qualname__]:
            method()
        else:
            print(self.Permissions[method.__qualname__])