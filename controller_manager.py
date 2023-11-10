import pygame as pg

class ControllerManager:
    def __init__(self, game):
        self.joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
        self.controller = self.joysticks[0]
        self.inputs = [0, 0, 0, 0, 0, 0, 0, 0]

    def read_controller_inputs(self):
        self.inputs[0] = self.controller.get_axis(0)
        self.inputs[1] = self.controller.get_axis(1)
        self.inputs[2] = self.controller.get_axis(2)
        if self.controller.get_name() != 'Controller (Xbox One For Windows)':
            self.inputs[2] = self.controller.get_axis(3)
        self.inputs[3] = self.controller.get_axis(5)

        # D-pad
        self.inputs[4] = self.controller.get_hat(0)

        # A-button
        self.inputs[5] = self.controller.get_button(0)
        
        # B-button
        self.inputs[6] = self.controller.get_button(1)
        
        # menu-button
        self.inputs[7] = self.controller.get_button(7)