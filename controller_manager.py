import pygame as pg

class ControllerManager:
    def __init__(self, game):
        self.joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
        self.controller = self.joysticks[0]
        self.inputs = [0 for i in range(9)]

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

        # X-button
        self.inputs[7] = self.controller.get_button(2)
        
        # menu-button
        self.inputs[8] = self.controller.get_button(7)

    def footstep(self, time_of_last_step):
        time_now = pg.time.get_ticks()
        if time_now -time_of_last_step > 600:
            self.rumble(1, 0, 100)
            time_of_last_step = time_now
        return time_of_last_step

    def rumble(self, low, high, duration):
        self.controller.rumble(low, high, duration)

    def stop_rumble(self):
        self.controller.stop_rumble()