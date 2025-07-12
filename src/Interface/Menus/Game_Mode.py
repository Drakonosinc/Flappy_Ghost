from .Base_Menu import BaseMenu
class GameMode(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.config_ai_buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":0})})
        self.buttons['continue'] = factory.create_TextButton({"font": self.interface.font1,"text": "→","position": (self.WIDTH-110,self.HEIGHT-100),"command1":lambda:self.type_game(False,True) if all(not mode for mode in self.interface.mode_game.values()) else None,"command2":lambda:(self.change_mains({"main":-1,"run":True,"command":self.interface.population}),self.interface.sound_back.stop(),self.interface.sound_back_game.play(loops=-1)if self.interface.sound_type["value_game"] else None)})
        self.buttons['training_ai'] = factory.create_TextButton({"text": "Training AI","position": (35,self.HEIGHT/2-150),"command1":lambda:self.type_game(True),"command2":lambda:self.update_mode_buttons(self.buttons)})
        self.buttons['player'] = factory.create_TextButton({"text": "Player","position": (35,self.HEIGHT/2-100),"command1":lambda:self.type_game(False,True),"command2":lambda:self.update_mode_buttons(self.buttons)})
        self.buttons['ai'] = factory.create_TextButton({"text": "AI","position": (35,self.HEIGHT/2-50),"command1":lambda:self.type_game(False,False,True),"command2":lambda:self.update_mode_buttons(self.buttons)})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Mode Game", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())