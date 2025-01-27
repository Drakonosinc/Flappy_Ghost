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
        self.pressed_mouse=config.get("pressed_mouse",(False,False,False))
        self.pressed=config.get("pressed",True)
        self.mouse_pos=config.get("mouse_pos",(0,0))
        self.detect_mouse=config.get("detect_mouse",True)
        self.type_button=config.get("type_button",0)
        self.sound_hover=config.get("sound_hover",None)
        self.sound_touch=config.get("sound_touch",None)
        self.command=config.get("command",None)
        self.command2=config.get("command2",None)
        self.command3=config.get("command3",None)
        self.button_states=config.get("button_states",{"sound_hover":True,"sound_touch":True})
    def draw(self):
        self.button=self.screen.blit(self.font.render(self.text,True,self.color),self.position) if self.type_button==0 else pygame.draw.polygon(self.screen, self.color, self.position)
        if not self.detect_mouse and not self.pressed:return self.button
    def mouse_collision(self):
        self.screen.blit(self.font.render(self.text,True,self.color2),self.position) if self.type_button==0 else pygame.draw.polygon(self.screen, self.color2, self.position2)
        if self.button.collidepoint(self.mouse_pos) and self.button_states["sound_hover"]:
            self.sound_hover.play(loops=0)
            self.button_states["sound_hover"]=False
        else:self.button_states["sound_hover"]=True
    def pressed_button(self):pass


def pressed_button(self,is_hovering_now,state,sound_touch,main,command=None,command2=None):
    if self.pressed_mouse[0]:
        if is_hovering_now and not state['click_played']:
            sound_touch.play(loops=0)
            state['click_played'] = True
            if main!=None:self.main=main
            if command!=None:command()
            if command2!=None:command2()
    else:state['click_played'] = False