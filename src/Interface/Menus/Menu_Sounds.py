from .Base_Menu import BaseMenu
class SoundsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.sound_type={"sound_menu":f"Sound Menu {"ON" if (x:=self.config.config_sounds["sound_menu"]) else "OFF"}","color_menu":self.interface.SKYBLUE if x else self.interface.RED,"value_menu":x,
                        "sound_Game":f"Sound Game {"ON" if (j:=self.config.config_sounds["sound_game"]) else "OFF"}","color_game":self.interface.SKYBLUE if j else self.interface.RED,"value_game":j}
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons['sound_menu_button'] = factory.create_TextButton({"text": self.sound_type["sound_menu"],"position": (35,self.HEIGHT/2-150),"command1":lambda:self.sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.interface.sound_back,True),"command2":self.config.save_config})
        self.buttons['sound_game_button'] = factory.create_TextButton({"text": self.sound_type["sound_Game"],"position": (35,self.HEIGHT/2-100),"command1":lambda:self.sound_on_off("sound_Game","color_game","value_game","Sound Game",self.interface.sound_back_game),"command2":self.config.save_config})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Sounds", True, "orange"),(35,self.HEIGHT/2-250))
        self.buttons['sound_menu_button'].change_item({"color":self.sound_type["color_menu"],"text":self.sound_type["sound_menu"]})
        self.buttons['sound_game_button'].change_item({"color":self.sound_type["color_game"],"text":self.sound_type["sound_Game"]})
        self.execute_buttons(*self.buttons.values())