import pygame
class Button:
    def __init__(self,config):
        self.screen=config["screen"]
        self.main=config.get("main", None)
        self.font=config.get("font",pygame.font.Font(None,25))
        self.text=config.get("text","")
        self.color=config.get("color",(255,255,255))
        self.color2=config.get("color2",(0,0,0))
        self.position=config.get("position",(0,0))
        self.position2=config.get("position2",self.position)
        self.pressed=config.get("pressed",True)
        self.detect_mouse=config.get("detect_mouse",True)
        self.type_button=config.get("type_button",0)
        self.sound_hover=config.get("sound_hover",None)
        self.sound_touch=config.get("sound_touch",None)
        self.commands = [config.get(f"command{i}") for i in range(1,4)]
        self.button_states=config.get("button_states",{"sound_hover":True,"sound_touch":True})
    def draw(self):
        self.button=self.screen.blit(self.font.render(self.text,True,self.color),self.position) if self.type_button==0 else pygame.draw.polygon(self.screen, self.color, self.position)
        
    def update(self):
        if self.detect_mouse:self.mouse_collision(mouse_pos=pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(pressed_mouse=pygame.mouse.get_pressed())
        else:return self.button
    def mouse_collision(self,mouse_pos):
        self.screen.blit(self.font.render(self.text,True,self.color2),self.position) if self.type_button==0 else pygame.draw.polygon(self.screen, self.color2, self.position2)
        if self.button.collidepoint(mouse_pos) and self.button_states["sound_hover"]:
            self.sound_hover.play(loops=0)
            self.button_states["sound_hover"]=False
        else:self.button_states["sound_hover"]=True
    def pressed_button(self,pressed_mouse):
        if pressed_mouse[0] and self.button_states["sound_touch"]:
            self.sound_touch.play(loops=0)
            self.button_states["sound_touch"]=False
            if self.main!=None:self.main=self.main
            self.execute_commands()
        else:self.button_states["sound_touch"]=True
    def execute_commands(self):
            for command in self.commands:
                if callable(command):command()