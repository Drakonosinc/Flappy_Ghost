from .Base_Menu import BaseMenu
class MainMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['play'] = factory.create_TextButton({"text": "PLAY","position": (self.width/2-60, self.height/2-150),"command1":lambda:self.change_mains({"main":2})})
        self.buttons['quit'] = factory.create_TextButton({"text": "QUIT","position": (self.width/2-60,self.height/2-115),"sound_touch": self.interface.sound_exit,"command1": self.interface.close_game})
        self.buttons['options'] = factory.create_TextButton({"text": "OPTIONS","position": (self.width-180,self.height-50),"command1":lambda:self.change_mains({"main":4})})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font4.render("FLAPPY GHOST", True, "orange"),(35,self.height/2-250))
        self.execute_buttons(*self.buttons.values())