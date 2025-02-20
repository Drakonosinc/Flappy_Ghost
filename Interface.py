from Elements import *
from Button import *
class interface(objects):
    def __init__(self):
        super().__init__()
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.sound_type={"sound_menu":f"Sound Menu {"ON" if (x:=self.config_sounds["sound_menu"]) else "OFF"}","color_menu":self.SKYBLUE if x else self.RED,"value_menu":x,
                        "sound_Game":f"Sound Game {"ON" if (j:=self.config_sounds["sound_game"]) else "OFF"}","color_game":self.SKYBLUE if j else self.RED,"value_game":j}
        self.utils_keys={"key_jump":False}
        self.key=None
    def play_music(self):
        self.check_sounds()
        self.sound_back.set_volume(0.5)
    def draw_interfaces(self):
        self.main_menu()
        self.menu_options()
        self.mode_game_menu()
        self.game_over_menu()
        self.pausa_menu()
        self.sounds_menu()
        self.visuals_menu()
        self.keys_menu()
        self.draw_generation()
    def draw_buttons(self):
        self.button_factory_f2_5 = ButtonFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.buttons_main_menu()
        self.buttons_game_over()
        self.buttons_mode_game()
        self.buttons_pausa()
        self.buttons_menu_options()
        self.buttons_visual()
        self.buttons_keys()
        self.buttons_sounds()
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font3_5.render(f"Generation: {int(self.generation)}", True, "orange"),(35,0))
    def filt(self,width,height,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((width,height),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def check_item(self,dic,is_true,is_false,item,**kwargs):
        for key,button in kwargs.items():setattr(button,item,(is_true if dic[key] else is_false))
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("FLAPPY GHOST", True, "orange"),(35,self.height/2-250))
            self.execute_buttons(self.play_button,self.quit_button,self.options_button)
    def buttons_main_menu(self):
        self.play_button = self.button_factory_f2_5.create_TextButton({"text": "PLAY","position": (self.width/2-60, self.height/2-150),"command1":lambda:self.change_mains({"main":2})})
        self.quit_button = self.button_factory_f2_5.create_TextButton({"text": "QUIT","position": (self.width/2-60,self.height/2-115),"sound_touch": self.sound_exit,"command1": self.close_game})
        self.options_button = self.button_factory_f2_5.create_TextButton({"text": "OPTIONS","position": (self.width-180,self.height-50),"command1":lambda:self.change_mains({"main":4})})
    def game_over_menu(self):
        if self.main==1:
            self.filt(self.width,self.height,150,self.RED)
            self.screen.blit(self.font4.render("Game Over", True, self.BLACK),(120,self.height/2-250))
            self.execute_buttons(self.restar_button,self.exit_over_button,self.exit_menu_button)
    def buttons_game_over(self):
        self.restar_button = self.button_factory_f2_5.create_TextButton({"text": "Press R to Restart","position": (120,self.height/2-150),"command1":self.reset,"command2":lambda:self.change_mains({"main":-1})})
        self.exit_over_button = self.button_factory_f2_5.create_TextButton({"text": "Exit The Game","position": (120,self.height/2-100),"sound_touch": self.sound_exit,"command1":self.close_game})
        self.exit_menu_button = self.button_factory_f2_5.create_TextButton({"text": "Exit The Menu","position": (120,self.height/2-50),"command1":self.reset,"command2":lambda:self.change_mains({"main":0,"run":True,"command":self.check_sounds})})
    def mode_game_menu(self):
        if self.main==2:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Mode Game", True, "orange"),(35,self.height/2-250))
            if self.mode_game["Training AI"]:self.menu_AI()
            self.execute_buttons(self.Training_AI_button,self.player_button,self.ai_button,self.continue_button,self.back_menu_button)
    def buttons_mode_game(self):
        self.Training_AI_button = self.button_factory_f2_5.create_TextButton({"text": "Training AI","position": (35,self.height/2-150),"command1":lambda:self.type_game(True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"Training AI":self.Training_AI_button,"Player":self.player_button,"AI":self.ai_button})})
        self.player_button = self.button_factory_f2_5.create_TextButton({"text": "Player","position": (35,self.height/2-100),"command1":lambda:self.type_game(False,True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"Player":self.player_button,"Training AI":self.Training_AI_button,"AI":self.ai_button})})
        self.ai_button = self.button_factory_f2_5.create_TextButton({"text": "AI","position": (35,self.height/2-50),"command1":lambda:self.type_game(False,False,True),"command2":lambda:self.check_item(self.mode_game,self.SKYBLUE,self.WHITE,"color",**{"AI":self.ai_button,"Player":self.player_button,"Training AI":self.Training_AI_button})})
        self.continue_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "→","position": (self.width-110,self.height-100),"command1":lambda:self.type_game(False,True) if all(not mode for mode in self.mode_game.values()) else None,"command2":lambda:(self.change_mains({"main":-1,"run":True,"command":self.population}),self.sound_back.stop(),self.sound_back_game.play(loops=-1)if self.sound_type["value_game"] else None)})
        self.back_menu_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.height-100),"command1":lambda:self.change_mains({"main":0})})
        self.buttons_config_AI()
    def menu_AI(self):
        self.screen.blit(self.font2_5.render(f"Config Training AI", True, "White"),(self.width/2+20,self.height/2-150))
        self.screen.blit(self.font2_5.render(f"Generation Size\n{self.config_AI['generation_value']:^36}", True, "White"),(self.width/2+40,self.height/2-100))
        self.screen.blit(self.font2_5.render(f"Population Size\n{self.config_AI['population_value']:^36}", True, "White"),(self.width/2+40,self.height/2-25))
        self.screen.blit(self.font2_5.render(f"Attempts By AI\n{self.config_AI['try_for_ai']:^{38 if self.config_AI['try_for_ai']<10 else 36}}", True, "White"),(self.width/2+40,self.height/2+50))
        self.screen.blit(self.font2_5.render(f"Save model", True, "White"),(self.width/2+40,self.height/2+125))
        self.execute_buttons(self.increase_generation,self.decrease_generation,self.increase_population,self.decrease_population,self.increase_try_for_ai,self.decrease_try_for_ai,self.save_model)
        self.save_model.change_item({"color":self.SKYBLUE if self.config_AI["model_save"] else self.RED,"text":"ON" if self.config_AI["model_save"] else "OFF"})
    def buttons_config_AI(self):
        self.increase_generation = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (self.width-100,self.height/2-70),"command1":lambda:self.increase_decrease_variable(self.config_AI,'generation_value')})
        self.decrease_generation = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (self.width-178,self.height/2-70),"command1":lambda:self.increase_decrease_variable(self.config_AI,'generation_value',True,-1)})
        self.increase_population = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (self.width-100,self.height/2+5),"command1":lambda:self.increase_decrease_variable(self.config_AI,'population_value')})
        self.decrease_population = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (self.width-178,self.height/2+5),"command1":lambda:self.increase_decrease_variable(self.config_AI,'population_value',True,-1)})
        self.increase_try_for_ai = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": ">","position": (self.width-100,self.height/2+80),"command1":lambda:self.increase_decrease_variable(self.config_AI,'try_for_ai')})
        self.decrease_try_for_ai = self.button_factory_f2_5.create_TextButton({"font":self.font3_5,"text": "<","position": (self.width-178,self.height/2+80),"command1":lambda:self.increase_decrease_variable(self.config_AI,'try_for_ai',True,-1)})
        self.save_model = self.button_factory_f2_5.create_TextButton({"text": "OFF","color": self.SKYBLUE,"position": (self.width-105,self.height/2+125),"command1":lambda:self.on_off(self.config_AI,"model_save"),"command2":self.save_config})
    def type_game(self,mode_one=False,mode_two=False,mode_three=False):
        self.mode_game["Training AI"]=mode_one
        self.mode_game["Player"]=mode_two
        if self.model_training!=None:self.mode_game["AI"]=mode_three
        else:self.load_AI()
    def pausa_menu(self):
        if self.main==3:
            self.filt(self.width,self.height,150,self.GRAY)
            self.screen.blit(self.font3.render("Pause", True, "orange"),(35,self.height/2-250))
            self.execute_buttons(self.reset_button,self.option_button,self.menu_button,self.exit_button)
    def buttons_pausa(self):
        self.reset_button = self.button_factory_f2_5.create_TextButton({"text": "Reset","position": (35,self.height/2-150),"command1":self.reset,"command2":lambda:self.change_mains({"main":-1})})
        self.option_button = self.button_factory_f2_5.create_TextButton({"text": "Option","position": (35,self.height/2-100),"command1":self.reset,"command2":lambda:self.change_mains({"main":4,"run":True}),"command3":self.check_sounds})
        self.menu_button = self.button_factory_f2_5.create_TextButton({"text": "Menu","position": (35,self.height/2-50),"command1":self.reset,"command2":lambda:self.change_mains({"main":0,"run":True}),"command3":self.check_sounds})
        self.exit_button = self.button_factory_f2_5.create_TextButton({"text": "Exit","position": (35,self.height/2),"sound_touch": self.sound_exit,"command1":self.close_game})
    def menu_options(self):
        if self.main==4:
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
        if self.main==5:
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
        self.save_visuals_button = self.button_factory_f2_5.create_TextButton({"text": "Save config","position": (self.width/2+80,self.height-85),"command1":self.save_config})
        self.default_visuals_button = self.button_factory_f2_5.create_TextButton({"text": "Default config","position": (self.width/2+50,self.height-50),"command1":lambda:self.config(visuals=True),"command2":self.load_visuals})
    def items_visuals(self):
        self.screen.blit(self.flappy_ghost,(self.players[0].rect.x-30,self.players[0].rect.y+50))
        self.screen.blit(self.tubes[0].image,(self.width/2-50,self.height/2))
        self.screen.blit(self.tubes_invert[0].image,(self.width/2+180,0))
    def change_items(self,item,background,number):
        self.config_visuals[item]=((self.config_visuals[item] + number) % len(self.config_visuals[background]))
        self.load_visuals()
    def load_visuals(self):
        self.load_images()
        for i in range(len(self.tubes)):
            self.tubes[i].image=pygame.image.load(os.path.join(self.image_path,self.config_visuals["tubes"][self.config_visuals["value_tubes"]]))
            self.tubes[i].image=pygame.transform.rotate(self.tubes[0].image,0)
            self.tubes[i].image=pygame.transform.scale(self.tubes[0].image,(100, self.height//2))
            self.tubes_invert[i].image=pygame.image.load(os.path.join(self.image_path,self.config_visuals["tubes"][self.config_visuals["value_tubes"]]))
            self.tubes_invert[i].image=pygame.transform.rotate(self.tubes_invert[0].image,180)
            self.tubes_invert[i].image=pygame.transform.scale(self.tubes_invert[0].image,(100, self.height//2))
    def keys_menu(self):
        if self.main==6:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Keys", True, "orange"),(35,self.height/2-250))
            self.execute_buttons(self.back_keys_button,self.space_button,self.save_keys_button,self.default_keys_button)
    def buttons_keys(self):
        self.back_keys_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.height-100),"command1":lambda:self.change_mains({"main":4})})
        self.space_button = self.button_factory_f2_5.create_TextButton({"text": self.config_keys["Name_key1"],"position": (35,self.height/2-150),"command1":lambda:self.change_keys("key_jump","Name_key1",self.space_button)})
        self.save_keys_button = self.button_factory_f2_5.create_TextButton({"text": "Save config","position": (self.width/2+80,self.height-85),"command1":self.save_config})
        self.default_keys_button = self.button_factory_f2_5.create_TextButton({"text": "Default config","position": (self.width/2+50,self.height-50),"command1":lambda:(self.config(keys=True),self.change_mains({"main":6,"command":self.buttons_keys}))})
    def change_keys(self,key,key_name,button=None):
        self.key=key
        self.key_name=key_name
        self.button_key=button
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
        self.check_item(self.utils_keys,self.SKYBLUE,self.WHITE,"color",**{"key_jump":self.space_button})
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config_keys[self.key]=event.key
            self.config_keys[self.key_name]=event.unicode.upper()
            self.check_item(self.config_keys,self.config_keys[self.key_name],self.WHITE,"text",**{self.key:self.button_key})
            self.change_keys(self.key,self.key_name)
    def sounds_menu(self):
        if self.main==7:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Sounds", True, "orange"),(35,self.height/2-250))
            self.execute_buttons(self.back_sounds_button,self.sound_menu_button,self.sound_game_button)
            self.sound_menu_button.change_item({"color":self.sound_type["color_menu"],"text":self.sound_type["sound_menu"]})
            self.sound_game_button.change_item({"color":self.sound_type["color_game"],"text":self.sound_type["sound_Game"]})
    def buttons_sounds(self):
        self.back_sounds_button = self.button_factory_f2_5.create_TextButton({"font": self.font1,"text": "←","position": (35,self.height-100),"command1":lambda:self.change_mains({"main":4})})
        self.sound_menu_button = self.button_factory_f2_5.create_TextButton({"text": self.sound_type["sound_menu"],"position": (35,self.height/2-150),"command1":lambda:self.sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.sound_back,True),"command2":self.save_config})
        self.sound_game_button = self.button_factory_f2_5.create_TextButton({"text": self.sound_type["sound_Game"],"position": (35,self.height/2-100),"command1":lambda:self.sound_on_off("sound_Game","color_game","value_game","Sound Game",self.sound_back_game),"command2":self.save_config})
    def sound_on_off(self,sound:str,color,value=True,type_sound="",sound_back=None,play=False):
        self.sound_type[value]=not self.sound_type[value]
        self.sound_type[color]=self.SKYBLUE if self.sound_type[value] else self.RED
        self.sound_type[sound]=type_sound+" ON" if self.sound_type[value] else type_sound+" OFF"
        sound_back.play(loops=-1) if self.sound_type[value] and play else sound_back.stop()
        self.on_off(self.config_sounds,sound.lower())
    def show_score(self,player):
        if self.main==-1 or self.main==1:self.screen.blit(self.font.render(f"Score: {int(player.scores)}", True, "orange"),(35,self.height-50))
    def fade_transition(self,fade_in,color=(0,0,0),limit=255):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(color)
        alpha=0 if not fade_in else 255
        while (not fade_in and alpha <= limit) or (fade_in and alpha >= limit):
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            self.clock.tick(20)
            alpha += -15 if fade_in else 15
    def change_mains(self,config):
        if fade_in:=config.get("fade_in",True):self.fade_transition(False,config.get("color",(0,0,0)),255)
        if fade_out:=config.get("fade_out",False):self.fade_transition(True,config.get("color2",(0,0,0)),0)
        self.main=config.get("main",None)
        if config.get("command",None):config["command"]()
        if config.get("run",False):setattr(self,"running",False),setattr(self, "game_over", True)
        if config.get("recursive",False):self.change_mains({"main":self.main,"fade_in":fade_in,"fade_out":fade_out})
    def increase_decrease_variable(self,dic=None,variable="",length=None,number=1,save=True):
        if dic!=None and length!=None:dic[variable]=max(1, dic[variable] + number)
        elif dic!=None:dic[variable]+=number
        else:setattr(self,variable,getattr(self,variable)+number)
        if save:self.save_config()
    def on_off(self,dic=None,variable=""):
        if dic:dic[variable]=not dic[variable]
        else:setattr(self,variable,not getattr(self,variable))