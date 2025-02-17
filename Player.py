from pygame import *
class Player:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.down_gravity:float = 0
        self.isjumper:bool = False
        self.reward:int = 0
        self.scores:int=0
        self.active:bool = True
    def jump(self, jumper_value,sound):
        if self.isjumper:
            self.down_gravity = jumper_value
            if sound!=None:sound.play()
            self.isjumper = False
    def fall(self, gravity):
        self.down_gravity += gravity
        self.rect.y += self.down_gravity
    def reset(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.down_gravity = 0
        self.isjumper = False
        self.scores = 0
        self.active = True
    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)