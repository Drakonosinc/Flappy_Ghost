from Loaders.Load_elements import *
from .Elements_interface import *
from .Menus import *
class interface(load_elements,BaseMenu):
    def __init__(self):
        load_elements.__init__(self)
        BaseMenu.__init__(self,self)
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.sound_type={"sound_menu":f"Sound Menu {"ON" if (x:=self.config.config_sounds["sound_menu"]) else "OFF"}","color_menu":self.SKYBLUE if x else self.RED,"value_menu":x,
                        "sound_Game":f"Sound Game {"ON" if (j:=self.config.config_sounds["sound_game"]) else "OFF"}","color_game":self.SKYBLUE if j else self.RED,"value_game":j}
        self.utils_keys={"key_jump":False}
        self.key=None
        self.initialize_menus()
    def initialize_menus(self):
        self.main_menu = MainMenu(self)
        self.game_over_menu = GameOver(self)
        self.game_mode_menu = GameMode(self)
    def play_music(self):
        self.check_sounds()
        self.sound_back.set_volume(0.5)
    def draw_interfaces(self):
        menu_routes = {
            0: self.main_menu.render,
            1: self.game_over_menu.render,
            2: self.game_mode_menu.render,}
        if self.main==3:self.pausa_menu()
        elif self.main==4:self.menu_options()
        elif self.main==5:self.visuals_menu()
        elif self.main==6:self.keys_menu()
        elif self.main==7:self.sounds_menu()
        if self.main in menu_routes:menu_routes[self.main]()
        self.draw_generation()
    def draw_buttons(self):
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.buttons_pausa()
        self.buttons_menu_options()
        self.buttons_visual()
        self.buttons_keys()
        self.buttons_sounds()
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font3_5.render(f"Generation: {int(self.generation)}", True, "orange"),(35,0))
    def menu_AI(self):
        self.execute_buttons(*self.buttons_in_config_ai,*self.text_in_training_ai,self.scroll)
        self.save_model.change_item({"color":self.SKYBLUE if self.config.config_AI["model_save"] else self.RED,"text":"ON" if self.config.config_AI["model_save"] else "OFF"})
        self.scroll.update_elements([*self.buttons_in_config_ai,*self.text_in_training_ai])
    def text_training_ai(self):
        if not hasattr(self, "text_in_training_ai"):
            self.text_C=self.button_factory_f2_5.create_Text({"text":(f"Config Training AI"),"position":(self.width/2-60,self.height/2-150),"detect_mouse":False})
            self.text_G=self.button_factory_f2_5.create_Text({"text":(f"Generation Size\n{self.config.config_AI['generation_value']:^36}"),"position":(self.width/2-40,self.height/2-100),"detect_mouse":False})
            self.text_P=self.button_factory_f2_5.create_Text({"text":(f"Population Size\n{self.config.config_AI['population_value']:^37}"),"position":(self.width/2-40,self.height/2-25),"detect_mouse":False})
            self.text_A=self.button_factory_f2_5.create_Text({"text":(f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{39 if self.config.config_AI['try_for_ai']<10 else 37}}"),"position":(self.width/2-40,self.height/2+50),"detect_mouse":False})
            self.text_S=self.button_factory_f2_5.create_Text({"text":(f"Save model"),"position":(self.width/2-40,self.height/2+125),"detect_mouse":False})
            self.text_in_training_ai=[self.text_C,self.text_G,self.text_P,self.text_A,self.text_S]
        else:
            self.text_G.change_item({"text": f"Generation Size\n{self.config.config_AI['generation_value']:^36}"})
            self.text_P.change_item({"text": f"Population Size\n{self.config.config_AI['population_value']:^37}"})
            self.text_A.change_item({"text": f"Attempts By AI\n{self.config.config_AI['try_for_ai']:^{39 if self.config.config_AI['try_for_ai']<10 else 36}}"})
    def buttons_config_AI(self):
        self.increase_generation = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (self.width-220,self.height/2-70),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value'),"command2":self.text_training_ai})
        self.decrease_generation = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (self.width-345,self.height/2-70),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'generation_value',True,-1),"command2":self.text_training_ai})
        self.increase_population = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (self.width-220,self.height/2+5),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value'),"command2":self.text_training_ai})
        self.decrease_population = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (self.width-345,self.height/2+5),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'population_value',True,-1),"command2":self.text_training_ai})
        self.increase_try_for_ai = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (self.width-220,self.height/2+80),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai'),"command2":self.text_training_ai})
        self.decrease_try_for_ai = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (self.width-345,self.height/2+80),"command1":lambda:self.increase_decrease_variable(self.config.config_AI,'try_for_ai',True,-1),"command2":self.text_training_ai})
        self.save_model = self.button_factory_f2_5.create_TextButton({"text": "OFF","color": self.SKYBLUE,"position": (self.width-185,self.height/2+125),"command1":lambda:self.on_off(self.config.config_AI,"model_save"),"command2":self.config.save_config})
        self.buttons_in_config_ai=[self.increase_generation,self.decrease_generation,self.increase_population,self.decrease_population,self.increase_try_for_ai,self.decrease_try_for_ai,self.save_model]
        self.scroll=self.button_factory_f2_5.create_ScrollBar({"position": (self.width-30, 100, 20, self.height-200),"thumb_height": 20})
    def type_game(self,mode_one=False,mode_two=False,mode_three=False):
        self.mode_game["Training AI"]=mode_one
        self.mode_game["Player"]=mode_two
        if self.model_training!=None:self.mode_game["AI"]=mode_three
        else:self.load_AI()
    def pausa_menu(self):
        self.filt(self.width,self.height,150,self.GRAY)
        self.screen.blit(self.font3.render("Pause", True, "orange"),(35,self.height/2-250))
        self.execute_buttons(self.reset_button,self.option_button,self.menu_button,self.exit_button)
    def buttons_pausa(self):
        self.reset_button = self.button_factory_f2_5.create_TextButton({"text": "Reset","position": (35,self.height/2-150),"command1":self.reset,"command2":lambda:self.change_mains({"main":-1})})
        self.option_button = self.button_factory_f2_5.create_TextButton({"text": "Option","position": (35,self.height/2-100),"command1":self.reset,"command2":lambda:self.change_mains({"main":4,"run":True}),"command3":self.check_sounds})
        self.menu_button = self.button_factory_f2_5.create_TextButton({"text": "Menu","position": (35,self.height/2-50),"command1":self.reset,"command2":lambda:self.change_mains({"main":0,"run":True}),"command3":self.check_sounds})
        self.exit_button = self.button_factory_f2_5.create_TextButton({"text": "Exit","position": (35,self.height/2),"sound_touch": self.sound_exit,"command1":self.close_game})
    def menu_options(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.font3.render("Options", True, "orange"),(35,self.height/2-250))
        self.execute_buttons(self.visual_button,self.sounds_button,self.keys_button,self.back_button)
    def buttons_menu_options(self):
        self.visual_button = self.button_factory_f2_5.create_TextButton({"text": "Visuals","position": (35,self.height/2-150),"command1":lambda:self.change_mains({"main":5})})
        self.sounds_button = self.button_factory_f2_5.create_TextButton({"text": "Sounds","position": (35,self.height/2-100),"command1":lambda:self.change_mains({"main":7})})
        self.keys_button = self.button_factory_f2_5.create_TextButton({"text": "Keys","position": (35,self.height/2-50),"command1":lambda:self.change_mains({"main":6})})
        self.back_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.height-100),"command1":lambda:self.change_mains({"main":0})})
    def check_sounds(self):
        self.sound_back_game.stop()
        self.sound_back.play(loops=-1) if self.sound_type["value_menu"] else None
    def visuals_menu(self):
        self.screen.fill(self.BLACK)
        self.items_visuals()
        self.screen.blit(self.font3.render("Visuals", True, "orange"),(35,self.height/2-250))
        self.execute_buttons(self.back_visual_button,self.decrease_player_button,self.increase_player_button,self.decrease_tube_button,self.increase_tube_button,self.save_visuals_button,self.default_visuals_button)
    def buttons_visual(self):
        self.back_visual_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.height-100),"command1":lambda:self.change_mains({"main":4})})
        self.decrease_player_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": "<","position": (self.players[0].rect.x-40,self.players[0].rect.y+70),"command1":lambda:self.change_items("value_flyers","flyers",-1)})
        self.increase_player_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": ">","position": (self.players[0].rect.x+60,self.players[0].rect.y+70),"command1":lambda:self.change_items("value_flyers","flyers",1)})
        self.decrease_tube_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": "<","position": (self.width/2-95,self.height/2),"command1":lambda:self.change_items("value_tubes","tubes",-1)})
        self.increase_tube_button = self.button_factory_f2_5.create_TextButton({"font": self.font3_5,"text": ">","position": (self.width/2+75,self.height/2),"command1":lambda:self.change_items("value_tubes","tubes",1)})
        self.save_visuals_button = self.button_factory_f2_5.create_TextButton({"text": "Save config","position": (self.width/2+80,self.height-85),"command1":self.config.save_config})
        self.default_visuals_button = self.button_factory_f2_5.create_TextButton({"text": "Default config","position": (self.width/2+50,self.height-50),"command1":lambda:self.config.config(visuals=True),"command2":self.load_visuals})
    def items_visuals(self):
        self.screen.blit(self.flappy_ghost,(self.players[0].rect.x-30,self.players[0].rect.y+50))
        self.screen.blit(self.tubes[0].tube_image,(self.width/2-50,self.height/2))
        self.screen.blit(self.tubes_invert[0].tube_image,(self.width/2+180,0))
    def change_items(self,item,background,number):
        self.config.config_visuals[item]=((self.config.config_visuals[item] + number) % len(self.config.config_visuals[background]))
        self.load_visuals()
    def load_visuals(self):
        self.load_images()
        self.instances()
    def keys_menu(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.font3.render("Keys", True, "orange"),(35,self.height/2-250))
        self.execute_buttons(self.back_keys_button,self.space_button,self.save_keys_button,self.default_keys_button)
    def buttons_keys(self):
        self.back_keys_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.height-100),"command1":lambda:self.change_mains({"main":4})})
        self.space_button = self.button_factory_f2_5.create_TextButton({"text": self.config.config_keys["Name_key1"],"position": (35,self.height/2-150),"command1":lambda:self.change_keys("key_jump","Name_key1",self.space_button)})
        self.save_keys_button = self.button_factory_f2_5.create_TextButton({"text": "Save config","position": (self.width/2+80,self.height-85),"command1":self.config.save_config})
        self.default_keys_button = self.button_factory_f2_5.create_TextButton({"text": "Default config","position": (self.width/2+50,self.height-50),"command1":lambda:(self.config.config(keys=True),self.change_mains({"main":6,"command":self.buttons_keys}))})
    def change_keys(self,key,key_name,button=None):
        self.key=key
        self.key_name=key_name
        self.button_key=button
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
        self.check_item(self.utils_keys,self.SKYBLUE,self.WHITE,"color",**{"key_jump":self.space_button})
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config.config_keys[self.key]=event.key
            self.config.config_keys[self.key_name]=event.unicode.upper()
            self.check_item(self.config.config_keys,self.config.config_keys[self.key_name],self.WHITE,"text",**{self.key:self.button_key})
            self.change_keys(self.key,self.key_name)
    def sounds_menu(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.font3.render("Sounds", True, "orange"),(35,self.height/2-250))
        self.execute_buttons(self.back_sounds_button,self.sound_menu_button,self.sound_game_button)
        self.sound_menu_button.change_item({"color":self.sound_type["color_menu"],"text":self.sound_type["sound_menu"]})
        self.sound_game_button.change_item({"color":self.sound_type["color_game"],"text":self.sound_type["sound_Game"]})
    def buttons_sounds(self):
        self.back_sounds_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.height-100),"command1":lambda:self.change_mains({"main":4})})
        self.sound_menu_button = self.button_factory_f2_5.create_TextButton({"text": self.sound_type["sound_menu"],"position": (35,self.height/2-150),"command1":lambda:self.sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.sound_back,True),"command2":self.config.save_config})
        self.sound_game_button = self.button_factory_f2_5.create_TextButton({"text": self.sound_type["sound_Game"],"position": (35,self.height/2-100),"command1":lambda:self.sound_on_off("sound_Game","color_game","value_game","Sound Game",self.sound_back_game),"command2":self.config.save_config})
    def sound_on_off(self,sound:str,color,value=True,type_sound="",sound_back=None,play=False):
        self.sound_type[value]=not self.sound_type[value]
        self.sound_type[color]=self.SKYBLUE if self.sound_type[value] else self.RED
        self.sound_type[sound]=type_sound+" ON" if self.sound_type[value] else type_sound+" OFF"
        sound_back.play(loops=-1) if self.sound_type[value] and play else sound_back.stop()
        self.on_off(self.config.config_sounds,sound.lower())
    def show_score(self,player):
        if self.main==-1 or self.main==1:self.screen.blit(self.font.render(f"Score: {int(player.scores)}", True, "orange"),(35,self.height-50))