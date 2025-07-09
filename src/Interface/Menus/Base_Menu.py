import pygame
class BaseMenu:
    def __init__(self, interface=None):
        self.interface = interface
        if interface:
            self.screen = interface.screen
            self.WIDTH = interface.width
            self.HEIGHT = interface.height
            self.config = interface.config
    def filt(self,width,height,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((width,height),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def check_item(self,dic,is_true,is_false,item,**kwargs):
        for key,button in kwargs.items():setattr(button,item,(is_true if dic[key] else is_false))
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def fade_transition(self,fade_in,color=(0,0,0),limit=255):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.fill(color)
        alpha=0 if not fade_in else 255
        while (not fade_in and alpha <= limit) or (fade_in and alpha >= limit):
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            self.interface.clock.tick(20)
            alpha += -15 if fade_in else 15
    def change_mains(self,config):
        if fade_in:=config.get("fade_in",True):self.fade_transition(False,config.get("color",(0,0,0)),config.get("limit",255))
        if fade_out:=config.get("fade_out",False):self.fade_transition(True,config.get("color2",(0,0,0)),0)
        self.main=config.get("main",None)
        if config.get("command",None):config["command"]()
        if config.get("run",False):setattr(self,"running",False),setattr(self, "game_over", True)
        if config.get("recursive",False):self.change_mains({"main":self.main,"fade_in":fade_in,"fade_out":fade_out})