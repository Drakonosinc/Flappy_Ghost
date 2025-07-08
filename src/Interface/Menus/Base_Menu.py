import pygame
class BaseMenu:
    def __init__(self, interface=None):
        self.interface = interface
        if interface:
            self.screen = interface.screen
            self.WIDTH = interface.width
            self.HEIGHT = interface.height
            self.config = interface.config