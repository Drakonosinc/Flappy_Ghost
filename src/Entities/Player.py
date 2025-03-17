from pygame import *
class Player:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.reset_position = (x, y, width, height)
        self.dy:float = 0
        self.isjumper:bool = False
        self.reward:int = 0
        self.scores:int=0
        self.active:bool = True
    def jump(self, jumper_value,sound):
        self.isjumper=True
        if self.isjumper:
            self.dy = jumper_value
            if sound!=None:sound.play()
            self.isjumper = False
    def reset(self):
        self.rect = Rect(*self.reset_position)
        self.dy = 0
        self.isjumper = False
        self.scores = 0
        self.active = True
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)