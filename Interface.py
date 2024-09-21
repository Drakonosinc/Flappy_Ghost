from Elements import *
class interface(objects):
    def __init__(self):
        super().__init__()
        self.button_states={}
    def filt(self,number):
        background=pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        background.fill((0,0,0,number))
        self.screen.blit(background,(0,0))
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
    def visuals_menu(self):
        if self.main==5:
            pass
    def keys_menu(self):
        if self.main==6:
            pass
    def button(self,screen,main:int,font,text:str,color,position,color2=None,pressed=True,command=None,detect_mouse=True,command2=None,sound_hover=None,sound_touch=None):
        button_id = (text, position)
        if button_id not in self.button_states:self.button_states[button_id] = {'hover_played': False, 'click_played': False, 'is_hovering': False}
        state = self.button_states[button_id]
        button=screen.blit(font.render(text,True,color),position)
        is_hovering_now = button.collidepoint(self.mouse_pos)
        self.mouse_collision(screen,detect_mouse,is_hovering_now,font,text,color2,position,state,sound_hover)
        if pressed:self.pressed_button(is_hovering_now,state,sound_touch,main,command,command2)
        else:return button
    def mouse_collision(self,screen,detect_mouse,is_hovering_now,font,text,color2,position,state,sound_hover):
        if detect_mouse:
            if is_hovering_now:
                screen.blit(font.render(text,True,color2),position)
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
    # def button_arrow(self,main,position,position2,color,number:int,number2=None,pressed=True,detect_mouse=True,command=None):
    #     arrow_button=pygame.draw.polygon(self.screen, color, position)
    #     if detect_mouse:
    #         if arrow_button.collidepoint(self.mouse_pos):
    #             pygame.draw.polygon(self.screen, self.WHITE, position2)
    #             if self.notsound_playing[number]:
    #                 self.sound_buttonletters.play(loops=0)
    #                 self.notsound_playing[number]=False
    #         else:self.notsound_playing[number]=True
    #     if self.pressed_mouse[0] and pressed:
    #         if arrow_button.collidepoint(self.mouse_pos):
    #             if self.notsound_playing[number2]:
    #                 self.sound_touchletters.play(loops=0)
    #                 self.notsound_playing[number2]=False
    #                 if main!=None:self.main=main
    #                 if command!=None:command()
    #         else:self.notsound_playing[number2]=True
    #     if pressed==False:return arrow_button