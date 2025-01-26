import pygame
class Button:
    def __init__(self,config):
        self.screen=config.get("screen", None)
        self.main=config.get("main", None)
        self.font=config.get("font",pygame.font.Font(None,25))
        self.text=config.get("text","")
        self.color=config.get("color",(255,255,255))
        self.color2=config.get("color2",(0,0,0))
        self.position=config.get("position",(0,0))
        self.position2=config.get("position2",None)
        self.pressed=config.get("pressed",True)
        self.detect_mouse=config.get("detect_mouse",True)
        self.type_button=config.get("type_button",0)
        self.sound_hover=config.get("sound_hover",None)
        self.sound_touch=config.get("sound_touch",None)
        self.command=config.get("command",None)
        self.command2=config.get("command2",None)
        self.command3=config.get("command3",None)
    def draw(self):
        button=self.screen.blit(self.font.render(self.text,True,self.color),self.position) if self.type_button==0 else pygame.draw.polygon(self.screen, self.color, self.position)
        if not self.detect_mouse and not self.pressed:return button
    def mouse_collision(self):
        self.screen.blit(self.font.render(self.text,True,self.color2),self.position) if self.type_button==0 else pygame.draw.polygon(self.screen, self.color2, self.position2)
        
def button(button_states={}):
    is_hovering_now = button.collidepoint(self.mouse_pos)
    if detect_mouse:self.mouse_collision(screen,type_button,is_hovering_now,font,text,color2,position,state,sound_hover,position2)
    if pressed:self.pressed_button(is_hovering_now,state,sound_touch,main,command,command2)
    else:return button
def mouse_collision(self,screen,type_button,is_hovering_now,font,text,color2,position,state,sound_hover,position2):
    if is_hovering_now:
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