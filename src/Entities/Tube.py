import pygame,os
class Tube():
    def __init__(self,x,y,angle,width,height,objects):
        self.rect=pygame.Rect(x,y,width,height)
        self.reset_position = (x, y, width, height)
        self.objects=objects
        self.config_visuals=objects.config.config_visuals
        self.load_tube_image(angle,width,height)
    def load_tube_image(self,angle,width_image,height_image):
        self.tube_image=pygame.image.load(os.path.join(self.objects.image_path,self.config_visuals["tubes"][self.config_visuals["value_tubes"]]))
        self.tube_image=pygame.transform.rotate(self.tube_image,angle)
        self.tube_image=pygame.transform.scale(self.tube_image,(width_image,height_image))
    def draw(self,screen):screen.blit(self.tube_image,(self.rect.x,self.rect.y))
    def move_tube_x(self,speed):self.rect.x-=speed
    def move_tube_y(self,speed):self.rect.y-=speed
    def reset(self):
        self.rect = pygame.Rect(*self.reset_position)