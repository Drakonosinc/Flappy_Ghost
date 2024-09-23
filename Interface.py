from Elements import *
class interface(objects):
    def __init__(self):
        super().__init__()
        self.mode_game={"Training AI":True,"PLayer":False,"AI":False}
    def draw_interfaces(self):
        self.main_menu()
        self.menu_options()
        self.mode_game_menu()
        self.game_over_menu()
        self.pausa_menu()
    def filt(self,width,height,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((width,height),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("FLAPPY GHOST", True, "orange"),(35,self.height/2-250))
            self.button(self.screen,2,self.font2_5,"PLAY",self.WHITE,(self.width/2-60,self.height/2-150),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"QUIT",self.WHITE,(self.width/2-60,self.height/2-115),self.GOLDEN,command=self.close_game,sound_hover=self.sound_buttonletters,sound_touch=self.sound_exit)
            self.button(self.screen,4,self.font2_5,"OPTIONS",self.WHITE,(self.width-180,self.height-50),self.GOLDEN,command=self.menu_options,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
    def game_over_menu(self):
        if self.main==1:
            self.filt(self.width,self.height,180,self.RED)
    def mode_game_menu(self):
        if self.main==2:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Mode Game", True, "orange"),(35,self.height/2-250))
            self.button(self.screen,None,self.font2_5,"Training AI",(self.SKYBLUE if self.mode_game["Training AI"] else self.WHITE),(35,self.height/2-150),self.GOLDEN,command=lambda:self.type_game(True),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"Player",(self.SKYBLUE if self.mode_game["PLayer"] else self.WHITE),(35,self.height/2-100),self.GOLDEN,command=lambda:self.type_game(False,True),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            # if self.model_training!=None:
            self.button(self.screen,None,self.font2_5,"AI",(self.SKYBLUE if self.mode_game["AI"] else self.WHITE),(35,self.height/2-50),self.GOLDEN,command=lambda:self.type_game(False,False,True),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,0,color=self.WHITE,color2=self.SKYBLUE,position=((50, 350), (50, 380), (25, 365)),position2=((50, 340), (50, 390), (10, 365)),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters,type_button=1)
            self.button(self.screen,-1,color=self.WHITE,color2=self.SKYBLUE,position=((650, 350), (650, 380), (675, 365)),position2=((650, 340), (650, 390), (690, 365)),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters,type_button=1)
    def type_game(self,mode_one=False,mode_two=False,mode_three=False):
        self.mode_game["Training AI"]=mode_one
        self.mode_game["PLayer"]=mode_two
        if os.path.exists(self.model_path):self.mode_game["AI"]=mode_three
    def pausa_menu(self):
        if self.main==3:
            self.filt(self.width,self.height,180)
    def menu_options(self):
        if self.main==4:
            self.screen.fill(self.BLACK)
            self.button(self.screen,0,color=self.WHITE,position=((50, 350), (50, 380), (25, 365)),position2=((50, 340), (50, 390), (10, 365)),sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters,type_button=1)
    def visuals_menu(self):
        if self.main==5:
            pass
    def keys_menu(self):
        if self.main==6:
            pass
    def button(self,screen,main:int=None,font=None,text:str=None,color=None,position=None,color2=None,pressed=True,command=None,detect_mouse=True,command2=None,sound_hover=None,sound_touch=None,position2=None,type_button:int=0,button_states={}):
        button_id = (text, position)
        if button_id not in button_states:button_states[button_id] = {'hover_played': False, 'click_played': False, 'is_hovering': False}
        state = button_states[button_id]
        if type_button==0:button=screen.blit(font.render(text,True,color),position)
        if type_button==1:button=pygame.draw.polygon(self.screen, color, position)
        is_hovering_now = button.collidepoint(self.mouse_pos)
        self.mouse_collision(screen,type_button,detect_mouse,is_hovering_now,font,text,color2,position,state,sound_hover,position2)
        if pressed:self.pressed_button(is_hovering_now,state,sound_touch,main,command,command2)
        else:return button
    def mouse_collision(self,screen,type_button,detect_mouse,is_hovering_now,font,text,color2,position,state,sound_hover,position2):
        if detect_mouse:
            if is_hovering_now:
                if type_button==0:screen.blit(font.render(text,True,color2),position)
                if type_button==1:pygame.draw.polygon(self.screen, color2, position2)
                if not state['is_hovering']:
                    if not state['hover_played']:
                        sound_hover.play(loops=0)
                        state['hover_played'] = True
                    state['is_hovering'] = True
            else:state['is_hovering'],state['hover_played']=False,False
    def pressed_button(self,is_hovering_now,state,sound_touch,main,command=None,command2=None):
        if self.pressed_mouse[0]:
            if is_hovering_now:
                if not state['click_played']:
                    sound_touch.play(loops=0)
                    state['click_played'] = True
                    if main!=None:self.main=main
                    if command!=None:command()
                    if command2!=None:command2()
        else:state['click_played'] = False