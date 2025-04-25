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
class Input_text(ElementBehavior):
    def __init__(self,config:dict):
        super().__init__(config)
        self.screen = config["screen"]
        self.font = config.get("font", pygame.font.Font(None, 25))
        self.text = config.get("text","")
        self.color=config.get("color",(0,0,0))
        self.color_back=config.get("color_back",(255,255,255))
        self.hover_color = config.get("hover_color", (255, 199, 51))
        self.position = config["position"]
        self.detect_mouse=config.get("detect_mouse",True)
        self.pressed_color=config.get("pressed_color",(135,206,235))
        self.border_color=config.get("border_color",(127,127,127))
        self.border=config.get("border",2)
        self.rect = pygame.Rect(*self.position)
    def change_text(self,event):
        if self.states["active"] and event.type==KEYDOWN:
            if event.key == K_BACKSPACE:self.text=self.text[:-1]
            else:self.text+=event.unicode
    def draw(self):
        pygame.draw.rect(self.screen,self.color_back,self.rect)
        if self.detect_mouse:self.mouse_collision(self.rect,pygame.mouse.get_pos())
        if self.pressed:self.pressed_button(pygame.mouse.get_pressed(),pygame.mouse.get_pos())
        input_player=pygame.draw.rect(self.screen,self.border_color,self.rect,self.border)
        self.screen.blit(self.font.render(self.text, True, self.color), (input_player.x+5, input_player.y-2))
    def draw_hover_effect(self):return pygame.draw.rect(self.screen,self.hover_color,self.rect)
    def pressed_button(self,pressed_mouse,mouse_pos):
        if pressed_mouse[0] and self.rect.collidepoint(mouse_pos) and self.states["presses_touch"]:
            self.states["active"]=True
            if self.sound_touch:self.sound_touch.play(loops=0)
            self.states["presses_touch"]=False
            self.execute_commands()
        if pressed_mouse[0] and not self.rect.collidepoint(mouse_pos):self.states["active"],self.states["presses_touch"]=False,True
        if self.states["active"]:pygame.draw.rect(self.screen,self.pressed_color,self.rect)
    def show_player(self):return self.text
class ScrollBar:
    def __init__(self, config: dict):
        self.screen = config["screen"]
        position = config["position"]
        self.rect = pygame.Rect(*position)
        self.hover_color=config.get("hover_color",(255, 199, 51))
        self.sound_hover = config.get("sound_hover")
        self.sound_touch = config.get("sound_touch")
        self.thumb_height = config.get("thumb_height", max(20, int(position[3] * config.get("thumb_ratio", 0.2))))
        self.thumb_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.thumb_height)
        self.color = config.get("color", (200, 200, 200))
        self.color_thumb = config.get("color_bar", (255, 199, 51))
        self.commands = config.get("command1")
        self.elements = None
        self.dragging = False
        self.drag_offset = 0
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.thumb_rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_offset = event.pos[1] - self.thumb_rect.y
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_y = event.pos[1] - self.drag_offset
            new_y = max(self.rect.top, min(new_y, self.rect.bottom - self.thumb_height))
            self.thumb_rect.y = new_y
            self.scroll_elements()
    def scroll_elements(self):
        max_scroll = self.content_height
        if max_scroll == 0:proportion = 0.0
        else:proportion = (self.thumb_rect.y - self.rect.y) / (self.rect.height - self.thumb_height)
        offset = int(proportion * max_scroll)
        for el, (x0, y0) in zip(self.elements, self.initial_positions):
            new_y = y0 - offset
            el.position = (x0, new_y)
            el.rect.y = new_y
        if callable(self.commands):self.commands(proportion)
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, self.color_thumb, self.thumb_rect)
    def update_elements(self, elements: list):
        if self.elements is None:
            self.elements = elements
            self.initial_positions = [(el.position[0], el.position[1]) for el in self.elements]
            if self.elements:
                top = min(y for _, y in self.initial_positions)
                bottom = max(el.rect.bottom for el in self.elements)
                self.content_height = bottom - top
            else:self.content_height = self.rect.height