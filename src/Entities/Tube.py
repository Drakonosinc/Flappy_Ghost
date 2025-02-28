import pygame,os
from Elements import *
class Tube():
    def __init__(self,x,y,angle,width_image,height_image,objects=objects()):
        self.objects=objects
        self.config_visuals=objects.config_visuals
        self.load_tube(x,y,angle,width_image,height_image)
    def load_tube(self,x,y,angle,width_image,height_image):
        self.load_tube_image(angle,width_image,height_image)
        self.rect=pygame.Rect(x,y,width_image,height_image)
    def load_tube_image(self,angle,width_image,height_image):
        self.tube_image=pygame.image.load(os.path.join(self.objects.image_path,self.config_visuals["tubes"][self.config_visuals["value_tubes"]]))
        self.tube_image=pygame.transform.rotate(self.tube_image,angle)
        self.tube_image=pygame.transform.scale(self.tube_image,(width_image,height_image))
    def draw(self,screen):screen.blit(self.tube_image,(self.rect.x,self.rect.y))
    def move_tube_x(self,speed):self.rect.x-=speed
    def move_tube_y(self,speed):self.rect.y-=speed