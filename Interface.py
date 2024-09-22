from Elements import *
class interface(objects):
    def __init__(self):
        super().__init__()
        self.button_states={}
    def filt(self,width,height,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((width,height),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font4.render("FLAPPY GHOST", True, "orange"),(35,self.height/2-250))
            self.button(self.screen,-1,self.font2_5,"PLAY",self.WHITE,(self.width/2-60,self.height/2-150),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"QUIT",self.WHITE,(self.width/2-60,self.height/2-115),self.GOLDEN,command=self.close_game,sound_hover=self.sound_buttonletters,sound_touch=self.sound_exit)
            self.button(self.screen,4,self.font2_5,"OPTIONS",self.WHITE,(self.width-180,self.height-50),self.GOLDEN,command=self.menu_options,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
    def game_over_menu(self):
        if self.main==1:
            pass
    def mode_game_menu(self):
        if self.main==2:
            pass
    def pausa_menu(self):
        if self.main==3:
            pass
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
    def button(self,screen,main:int=None,font=None,text:str=None,color=None,position=None,color2=None,pressed=True,command=None,detect_mouse=True,command2=None,sound_hover=None,sound_touch=None,position2=None,type_button:int=0):
        button_id = (text, position)
        if button_id not in self.button_states:self.button_states[button_id] = {'hover_played': False, 'click_played': False, 'is_hovering': False}
        state = self.button_states[button_id]
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
                if type_button==1:pygame.draw.polygon(self.screen, self.WHITE, position2)
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