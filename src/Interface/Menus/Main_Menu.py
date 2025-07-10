from .Base_Menu import BaseMenu
class MainMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['play'] = factory.create_TextButton({"text": "PLAY","position": (self.width/2-60, self.height/2-150),"command1":lambda:self.change_mains({"main":2})})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font4.render("FLAPPY GHOST", True, "orange"),(35,self.height/2-250))
        self.execute_buttons(*self.buttons.values())