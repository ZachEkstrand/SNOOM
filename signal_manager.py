from player import *

class SignalManager:
    def __init__(self, game):
        self.game = game
        self.Permissions = {
            'XBController.read_controller_inputs':True,
            'Player.xbc_inputs':True,
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
            #print(self.Permissions[method.__qualname__])