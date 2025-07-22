from .Base_Menu import BaseMenu
class SoundsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons['sound_menu_button'] = factory.create_TextButton({"text": self.sound_type["sound_menu"],"position": (35,self.HEIGHT/2-150),"command1":lambda:self.sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.interface.sound_back,True),"command2":self.config.save_config})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Sounds", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())