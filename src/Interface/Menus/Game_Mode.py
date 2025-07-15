from .Base_Menu import BaseMenu
class GameMode(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
        self.config_ai_buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":0})})
        self.buttons['continue'] = factory.create_TextButton({"font": self.interface.font1,"text": "→","position": (self.WIDTH-110,self.HEIGHT-100),"command1":lambda:self._type_game(False,True) if all(not mode for mode in self.interface.mode_game.values()) else None,"command2":lambda:(self.change_mains({"main":-1,"run":True,"command":self.interface.population}),self.interface.sound_back.stop(),self.interface.sound_back_game.play(loops=-1)if self.interface.sound_type["value_game"] else None)})
        self.buttons['training_ai'] = factory.create_TextButton({"text": "Training AI","position": (35,self.HEIGHT/2-150),"command1":lambda:self._type_game(True),"command2":lambda:self.update_mode_buttons(self.buttons)})
        self.buttons['player'] = factory.create_TextButton({"text": "Player","position": (35,self.HEIGHT/2-100),"command1":lambda:self._type_game(False,True),"command2":lambda:self.update_mode_buttons(self.buttons)})
        self.buttons['ai'] = factory.create_TextButton({"text": "AI","position": (35,self.HEIGHT/2-50),"command1":lambda:self._type_game(False,False,True),"command2":lambda:self.update_mode_buttons(self.buttons)})
        self._setup_training_ai_buttons(),self._setup_training_ai_texts()
    def _type_game(self,mode_one=False,mode_two=False,mode_three=False):
        self.mode_game["Training AI"]=mode_one
        self.mode_game["Player"]=mode_two
        if self.model_training!=None:self.mode_game["AI"]=mode_three
        else:self.load_AI()
    def _setup_training_ai_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.config_ai_buttons['increase_generation'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (self.WIDTH-220,self.HEIGHT/2-70),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value'),"command2":self._update_training_ai_texts})
        self.config_ai_buttons['decrease_generation'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (self.WIDTH-345,self.HEIGHT/2-70),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value',True,-1),"command2":self._update_training_ai_texts})
        self.config_ai_buttons['increase_population'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (self.WIDTH-220,self.HEIGHT/2+5),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value'),"command2":self._update_training_ai_texts})
        self.config_ai_buttons['decrease_population'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (self.WIDTH-345,self.HEIGHT/2+5),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value',True,-1),"command2":self._update_training_ai_texts})
        self.config_ai_buttons['increase_try_for_ai'] = factory.create_TextButton({"font":self.interface.font3_5,"text": ">","position": (self.WIDTH-220,self.HEIGHT/2+80),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai'),"command2":self._update_training_ai_texts})
        self.config_ai_buttons['decrease_try_for_ai'] = factory.create_TextButton({"font":self.interface.font3_5,"text": "<","position": (self.WIDTH-345,self.HEIGHT/2+80),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai',True,-1),"command2":self._update_training_ai_texts})
        self.config_ai_buttons['save_model'] = factory.create_TextButton({"text": "OFF","color": self.interface.SKYBLUE,"position": (self.WIDTH-185,self.HEIGHT/2+125),"command1":lambda:self.on_off(self.config.config_AI,"model_save"),"command2":self.config.save_config})
        self.scroll = factory.create_ScrollBar({"position": (self.WIDTH-30, 100, 20, self.HEIGHT-200),"thumb_height": 20})
    def _setup_training_ai_texts(self):
        factory = self.interface.button_factory_f2_5
        self.config_ai_buttons['text_C'] = factory.create_Text({"text":(f"Config Training AI"),"position":(self.WIDTH/2-60,self.HEIGHT/2-150),"detect_mouse":False})
        self.config_ai_buttons['text_G'] = factory.create_Text({"text":(f"Generation Size\n{self.config.config_AI['generation_value']:^36}"),"position":(self.WIDTH/2-40,self.HEIGHT/2-100),"detect_mouse":False})
        self.config_ai_buttons['text_P'] = factory.create_Text({"text":(f"Population Size\n{self.config.config_AI['population_value']:^37}"),"position":(self.WIDTH/2-40,self.HEIGHT/2-25),"detect_mouse":False})
        self.config_ai_buttons['text_A'] = factory.create_Text({"text":(f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{39 if self.config.config_AI['try_for_ai']<10 else 37}}"),"position":(self.WIDTH/2-40,self.HEIGHT/2+50),"detect_mouse":False})
        self.config_ai_buttons['text_S'] = factory.create_Text({"text":(f"Save model"),"position":(self.WIDTH/2-40,self.HEIGHT/2+125),"detect_mouse":False})
    def _update_training_ai_texts(self):
        if 'text_G' in self.config_ai_buttons:self.config_ai_buttons['text_G'].change_item({"text": f"Generation Size\n{self.config.config_AI['generation_value']:^36}"})
        if 'text_P' in self.config_ai_buttons:self.config_ai_buttons['text_P'].change_item({"text": f"Population Size\n{self.config.config_AI['population_value']:^37}"})
        if 'text_A' in self.config_ai_buttons:self.config_ai_buttons['text_A'].change_item({"text": f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{39 if self.config.config_AI['try_for_ai']<10 else 36}}"})
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Mode Game", True, "orange"),(35,self.HEIGHT/2-250))
        if self.interface.mode_game["Training AI"]:self._render_menu_ai()
        self.execute_buttons(*self.buttons.values())
    def _render_menu_ai(self):
        self.execute_buttons(*self.config_ai_buttons.values())
        self.config_ai_buttons['save_model'].change_item({"color":self.interface.SKYBLUE if self.config.config_AI["model_save"] else self.interface.RED,"text":"ON" if self.config.config_AI["model_save"] else "OFF"})
        self.scroll.update_elements([*self.config_ai_buttons.values()])