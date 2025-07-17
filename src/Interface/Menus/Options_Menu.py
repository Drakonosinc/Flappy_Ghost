from .Base_Menu import BaseMenu
class OptionsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":0})})
        self.buttons['visual'] = factory.create_TextButton({"text": "Visuals","position": (35,self.HEIGHT/2-150),"command1":lambda:self.change_mains({"main":5})})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Options", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())