import pygame
from pygame.locals import *
class ElementsFactory:
    def __init__(self,config:dict):
        self.screen=config["screen"]
        self.font=config.get("font",pygame.font.Font(None,25))
        self.color=config.get("color",(255,255,255))
        self.hover_color=config.get("hover_color",(255, 199, 51))
        self.color_back=config.get("color_back",(255,255,255))
        self.sound_hover=config.get("sound_hover",None)
        self.sound_touch=config.get("sound_touch",None)
    def create_Text(self,config:dict):
        return Text({"screen": self.screen,"font": self.font,"color": self.color,"hover_color": self.hover_color,**config})
    def create_TextButton(self,config:dict):
        return TextButton({"screen": self.screen,"font": self.font,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_PolygonButton(self,config:dict):
        return PolygonButton({"screen": self.screen,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_InputText(self,config:dict):
        return Input_text({"screen": self.screen,"font": self.font,"color": self.color,"color_back":self.color_back,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
    def create_ScrollBar(self,config:dict):
        return ScrollBar({"screen": self.screen,"color": self.color,"hover_color": self.hover_color,"sound_hover": self.sound_hover,"sound_touch": self.sound_touch,**config})
class ElementBehavior:
    def __init__(self, config: dict):
        self.sound_hover = config.get("sound_hover")
        self.sound_touch = config.get("sound_touch")
        self.detect_mouse=config.get("detect_mouse",True)
        self.pressed = config.get("pressed",True)
        self.states=config.get("states",{"detect_hover":True,"presses_touch":True,"click_time": None,"active":False})
        self.commands = [config.get(f"command{i}") for i in range(1,4)]
        self.new_events(time=config.get("time",500))
    def events(self, event):pass
    def new_events(self,time):
        self.EVENT_NEW = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENT_NEW,time)
    def reactivate_pressed(self,event):
        if event.type==self.EVENT_NEW:self.states["presses_touch"]=True
    def draw_hover_effect(self):raise NotImplementedError
    def mouse_collision(self,rect,mouse_pos,draw=None):
        if rect.collidepoint(mouse_pos):
            self.draw_hover_effect() if draw is None else draw()
            if self.states["detect_hover"]:
                if self.sound_hover:self.sound_hover.play(loops=0)
                self.states["detect_hover"]=False
        else:self.states["detect_hover"]=True
    def pressed_button(self,pressed_mouse,mouse_pos):
        current_time = pygame.time.get_ticks()
        if pressed_mouse[0] and self.rect.collidepoint(mouse_pos) and self.states["presses_touch"]:
            self.states["presses_touch"]=False
            self.states["click_time"] = current_time
        if self.states["click_time"] is not None:
            if current_time - self.states["click_time"] >= 200:
                if self.sound_touch:self.sound_touch.play(loops=0)
                self.states["click_time"] = None
                self.states["presses_touch"] = True
                self.execute_commands()
    def execute_commands(self):
        for command in self.commands:
            if callable(command):command()
class Text:
    def __init__(self,config:dict):
        self.screen = config["screen"]
        self.font = config.get("font", pygame.font.Font(None, 25))
        self.Behavior = ElementBehavior(config)
        self.text = config["text"]
        self.color = config.get("color", (255, 255, 255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.position = config["position"]
        self.states=config.get("states",{"detect_hover":True})
        self.rect = pygame.Rect(*self.position, *self.font.size(self.text))
    def draw(self):
        self.screen.blit(self.font.render(self.text, True,self.color), self.position)
        if self.Behavior.detect_mouse:self.Behavior.mouse_collision(self.rect,pygame.mouse.get_pos(),self.draw_hover_effect)
    def draw_hover_effect(self):return self.screen.blit(self.font.render(self.text,True,self.hover_color),self.position)
class TextButton(Text,ElementBehavior):
    def __init__(self,config:dict):
        Text.__init__(self, config)
        ElementBehavior.__init__(self, config)
    def draw(self):
        super().draw()
        if self.pressed:self.pressed_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def change_item(self,config:dict):
        self.color=config.get("color",self.color)
        self.text=config.get("text",self.text)
        self.detect_mouse=config.get("detect_mouse",self.detect_mouse)
        self.pressed=config.get("pressed",self.pressed)
class PolygonButton(ElementBehavior):
    def __init__(self,config:dict):
        super().__init__(config)
        self.screen = config["screen"]
        self.position = config["position"]
        self.hover_position = config.get("hover_position",self.position)
        self.color = config.get("color", (255, 255, 255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.detect_mouse=config.get("detect_mouse",True)
        self.rect = pygame.draw.polygon(self.screen, self.color, self.position).copy()
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, self.position)
        if self.detect_mouse:self.mouse_collision(self.rect,pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def draw_hover_effect(self):return pygame.draw.polygon(self.screen, self.hover_color, self.hover_position)
    def change_item(self,config:dict):
        self.color=config.get("color",self.color)
        self.detect_mouse=config.get("detect_mouse",self.detect_mouse)
        self.pressed=config.get("pressed",self.pressed)

class ScrollBar:
    def __init__(self,config:dict):
        self.screen=config["screen"]
        self.color = config.get("color", (255, 255, 255))
        self.color_bar = config.get("color_bar", (255, 199, 51))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.position = config["position"]
        self.position_bar = config["position_bar",self.position]
        self.commands = [config.get(f"command{i}") for i in range(1,4)]
        self.sound_hover = config.get("sound_hover")
        self.sound_touch = config.get("sound_touch")
        self.pressed = config.get("pressed",True)
        self.detect_mouse=config.get("detect_mouse",True)
        self.pressed_keep = config.get("pressed_keep",True)
        self.button_states=config.get("button_states",{"detect_hover":True,"presses_touch":True,"pressed_keep":True})
        self.holding = False
        self.rect = pygame.Rect(*self.position)
        self.rect_bar = pygame.Rect(*self.position_bar,self.position.width,self.position.height*4)
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):self.holding = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:self.holding = False
    def draw(self):
        if self.detect_mouse:self.mouse_collision(pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
        if self.pressed_keep:self.pressed_keep_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
    def mouse_collision(self,mouse_pos):pass
    def pressed_button(self,pressed_mouse,mouse_pos):pass
    def pressed_keep_button(self,pressed_mouse,mouse_pos):pass
    def execute_commands(self):
        for command in self.commands:
            if callable(command):command()