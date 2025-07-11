from .Base_Menu import BaseMenu
class GameOver(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['reset'] = factory.create_TextButton({"text": "Press R to Restart","position": (120,self.HEIGHT/2-150),"command1":self.interface.reset,"command2":lambda:self.change_mains({"main":-1})})
        self.buttons['quit'] = factory.create_TextButton({"text": "Exit The Game","position": (120,self.HEIGHT/2-100),"sound_touch": self.interface.sound_exit,"command1":self.interface.close_game})
    def render(self):
        self.filt(self.WIDTH,self.HEIGHT,150,self.interface.RED)
        self.screen.blit(self.interface.font4.render("Game Over", True, self.interface.BLACK),(120,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())