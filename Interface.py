from Elements import *
from Button import Button
class interface(objects):
    def __init__(self):
        super().__init__()
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.sound_type={"sound_menu":"Sound Menu ON","color_menu":self.SKYBLUE,"value_menu":True,
                        "sound_Game":"Sound Game ON","color_game":self.SKYBLUE,"value_game":True}
        self.utils_keys={"key_jump":False}
        self.key=None
        self.draw_buttons()
    def play_music(self):
        self.sound_back.play(loops=-1)
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
        self.show_score()
        self.draw_generation()
    def draw_buttons(self):
        self.buttons_main_menu()
        self.buttons_game_over()
        self.buttons_mode_game()
        self.buttons_pausa()
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font3_5.render(f"Generation: {int(self.generation)}", True, "orange"),(35,0))
    def filt(self,width,height,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((width,height),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def check_colors(self,dic,color1,color2,**kwargs):
        for key,button in kwargs.items():setattr(button,"color",(color1 if dic[key] else color2))
    def execute_buttons(self,*args):
        for button in args:button.draw()
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("FLAPPY GHOST", True, "orange"),(35,self.height/2-250))
            self.execute_buttons(self.play_button,self.quit_button,self.options_button)
    def buttons_main_menu(self):
        self.play_button = Button({"screen": self.screen,"font": self.font2_5,"text": "PLAY","color": self.WHITE,"position": (self.width/2-60, self.height/2-150),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',2)})
        self.quit_button = Button({"screen": self.screen,"font": self.font2_5,"text": "QUIT","color": self.WHITE,"position": (self.width/2-60,self.height/2-115),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_exit,"command1": self.close_game})
        self.options_button = Button({"screen": self.screen,"font": self.font2_5,"text": "OPTIONS","color": self.WHITE,"position": (self.width-180,self.height-50),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',4)})
    def game_over_menu(self):
        if self.main==1:
            self.filt(self.width,self.height,150,self.RED)
            self.screen.blit(self.font4.render("Game Over", True, self.BLACK),(120,self.height/2-250))
            self.execute_buttons(self.restar_button,self.exit_button,self.exit_menu_button)
    def buttons_game_over(self):
        self.restar_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Press R to Restart","color": self.BLACK,"position": (120,self.height/2-150),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.reset,"command2":lambda:setattr(self,'main',-1)})
        self.exit_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Exit The Game","color": self.BLACK,"position": (120,self.height/2-100),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_exit,"command1":self.close_game})
        self.exit_menu_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Exit The Menu","color": self.BLACK,"position": (120,self.height/2-50),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.reset,"command2":lambda:setattr(self,'main',0),"command3":self.check_sounds})
    def mode_game_menu(self):
        if self.main==2:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Mode Game", True, "orange"),(35,self.height/2-250))
            self.execute_buttons(self.Training_AI_button,self.player_button,self.ai_button,self.continue_button,self.back_menu_button)
    def buttons_mode_game(self):
        self.Training_AI_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Training AI","color":self.WHITE,"position": (35,self.height/2-150),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.type_game(True),"command2":lambda:self.check_colors(self.mode_game,self.SKYBLUE,self.WHITE,**{"Training AI":self.Training_AI_button,"Player":self.player_button,"AI":self.ai_button}),})
        self.player_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Player","color":self.WHITE,"position": (35,self.height/2-100),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.type_game(False,True),"command2":lambda:self.check_colors(self.mode_game,self.SKYBLUE,self.WHITE,**{"Player":self.player_button,"Training AI":self.Training_AI_button,"AI":self.ai_button})})
        self.ai_button = Button({"screen": self.screen,"font": self.font2_5,"text": "AI","color":self.WHITE,"position": (35,self.height/2-50),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.type_game(False,False,True),"command2":lambda:self.check_colors(self.mode_game,self.SKYBLUE,self.WHITE,**{"AI":self.ai_button,"Player":self.player_button,"Training AI":self.Training_AI_button})})
        self.continue_button = Button({"screen": self.screen,"font": self.font1,"text": "→","color":self.WHITE,"position": (self.width-110,self.height-100),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:self.type_game(False,True) if all(not mode for mode in self.mode_game.values()) else None,"command2":lambda:(setattr(self,'main',-1),self.sound_back.stop(),self.sound_back_game.play(loops=-1)if self.sound_type["value_game"] else None)})
        self.back_menu_button = Button({"screen": self.screen,"font": self.font1,"text": "←","color":self.WHITE,"position": (35,self.height-100),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":lambda:setattr(self,'main',0)})
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
        self.reset_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Reset","color":self.WHITE,"position": (35,self.height/2-150),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.reset,"command2":lambda:setattr(self,'main',-1)})
        self.option_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Option","color":self.WHITE,"position": (35,self.height/2-100),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.reset,"command2":lambda:setattr(self,'main',4),"command3":self.check_sounds})
        self.menu_button = Button({"screen": self.screen,"font": self.font2_5,"text": "Menu","color":self.WHITE,"position": (35,self.height/2-50),"color2": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters,"command1":self.reset,"command2":lambda:setattr(self,'main',0),"command3":self.check_sounds})
        self.exit_button = Button({"screen": self.screen,
                                    "font": self.font2_5,
                                    "text": "Exit",
                                    "color":self.WHITE,
                                    "position": (35,self.height/2),
                                    "color2": self.GOLDEN,
                                    "sound_hover": self.sound_buttonletters,
                                    "sound_touch": self.sound_exit,
                                    "command1":self.close_game})
    def menu_options(self):
        if self.main==4:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Options", True, "orange"),(35,self.height/2-250))
            self.button(self.screen,5,self.font2_5,"Visuals",self.WHITE,(35,self.height/2-150),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,7,self.font2_5,"Sounds",self.WHITE,(35,self.height/2-100),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,6,self.font2_5,"Keys",self.WHITE,(35,self.height/2-50),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,0,self.font1,"←",self.WHITE,(35,self.height-100),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
    def check_sounds(self):
        self.sound_back_game.stop()
        self.sound_back.play(loops=-1) if self.sound_type["value_menu"] else None
    def visuals_menu(self):
        if self.main==5:
            self.screen.fill(self.BLACK)
            self.items_visuals()
            self.screen.blit(self.font3.render("Visuals", True, "orange"),(35,self.height/2-250))
            self.button(self.screen,None,self.font3_5,"<",self.WHITE,(self.object1.x-40,self.object1.y+70),self.GOLDEN,command=lambda:self.change_items("value_flyers","flyers",-1),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font3_5,">",self.WHITE,(self.object1.x+60,self.object1.y+70),self.GOLDEN,command=lambda:self.change_items("value_flyers","flyers",1),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font3_5,"<",self.WHITE,(self.width/2-95,self.height/2),self.GOLDEN,command=lambda:self.change_items("value_tubes","tubes",-1),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font3_5,">",self.WHITE,(self.width/2+75,self.height/2),self.GOLDEN,command=lambda:self.change_items("value_tubes","tubes",1),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,4,self.font1,"←",self.WHITE,(35,self.height-100),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"Save config",self.WHITE,(self.width/2+80,self.height-85),self.GOLDEN,command=self.save_config,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"Default config",self.WHITE,(self.width/2+50,self.height-50),self.GOLDEN,command=lambda:self.config(visuals=True),command2=self.load_visuals,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
    def items_visuals(self):
        self.screen.blit(self.flappy_ghost,(self.object1.x-30,self.object1.y+50))
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
            self.button(self.screen,None,self.font2_5,self.config_keys["Name_key1"],self.SKYBLUE if self.utils_keys["key_jump"] else self.WHITE,(35,self.height/2-150),self.GOLDEN,command=lambda:self.change_keys("key_jump","Name_key1"),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,4,self.font1,"←",self.WHITE,(35,self.height-100),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"Save config",self.WHITE,(self.width/2+80,self.height-85),self.GOLDEN,command=self.save_config,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"Default config",self.WHITE,(self.width/2+50,self.height-50),self.GOLDEN,command=lambda:self.config(keys=True),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
    def change_keys(self,key,key_name):
        self.key=key
        self.key_name=key_name
        self.utils_keys[self.key]= not self.utils_keys[self.key]
    def event_keys(self,event):
        if self.key!=None:
            if self.utils_keys[self.key] and event.type==KEYDOWN:
                self.config_keys[self.key]=event.key
                self.config_keys[self.key_name]=event.unicode.upper()
                self.utils_keys[self.key]= not self.utils_keys[self.key]
    def sounds_menu(self):
        if self.main==7:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Sounds", True, "orange"),(35,self.height/2-250))
            self.button(self.screen,None,self.font2_5,self.sound_type["sound_menu"],self.sound_type["color_menu"],(35,self.height/2-150),self.GOLDEN,command=lambda:self.sound_on_off("sound_menu","color_menu","value_menu","Sound Menu",self.sound_back,True),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,self.sound_type["sound_Game"],self.sound_type["color_game"],(35,self.height/2-100),self.GOLDEN,command=lambda:self.sound_on_off("sound_Game","color_game","value_game","Sound Game",self.sound_back_game),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,4,self.font1,"←",self.WHITE,(35,self.height-100),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
    def sound_on_off(self,sound:str,color=(0,0,0),value=True,type_sound="",sound_back=None,play=False):
        self.sound_type[value]=not self.sound_type[value]
        self.sound_type[color]=self.SKYBLUE if self.sound_type[value] else self.RED
        self.sound_type[sound]=type_sound+" ON" if self.sound_type[value] else type_sound+" OFF"
        sound_back.play(loops=-1) if self.sound_type[value] and play else sound_back.stop()
    def show_score(self):
        if self.main==-1 or self.main==1:self.screen.blit(self.font.render(f"Score: {int(self.scores)}", True, "orange"),(35,self.height-50))
    def button(self,screen,main:int=None,font=None,text:str=None,color=None,position=None,color2=None,pressed=True,command=None,detect_mouse=True,command2=None,sound_hover=None,sound_touch=None,position2=None,type_button:int=0,button_states={}):
        if (button_id:=(text, position)) not in button_states:button_states[button_id] = {'hover_played': False, 'click_played': False, 'is_hovering': False}
        state = button_states[button_id]
        button=screen.blit(font.render(text,True,color),position) if type_button==0 else pygame.draw.polygon(self.screen, color, position)
        is_hovering_now = button.collidepoint(self.mouse_pos)
        if detect_mouse:self.mouse_collision(screen,type_button,is_hovering_now,font,text,color2,position,state,sound_hover,position2)
        if pressed:self.pressed_button(is_hovering_now,state,sound_touch,main,command,command2)
        else:return button
    def mouse_collision(self,screen,type_button,is_hovering_now,font,text,color2,position,state,sound_hover,position2):
        if is_hovering_now:
            screen.blit(font.render(text,True,color2),position) if type_button==0 else pygame.draw.polygon(self.screen, color2, position2)
            if not state['is_hovering']:
                if not state['hover_played']:
                    sound_hover.play(loops=0)
                    state['hover_played'] = True
                state['is_hovering'] = True
        else:state['is_hovering'],state['hover_played']=False,False
    def pressed_button(self,is_hovering_now,state,sound_touch,main,command=None,command2=None):
        if self.pressed_mouse[0]:
            if is_hovering_now and not state['click_played']:
                sound_touch.play(loops=0)
                state['click_played'] = True
                if main!=None:self.main=main
                if command!=None:command()
                if command2!=None:command2()
        else:state['click_played'] = False