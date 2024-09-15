import pygame,random,os,sys
from pygame.locals import *
import numpy as np
from Genetic_Algorithm import *
class objects():
    def __init__(self):
        self.width=800
        self.height=600
        self.load_images()
        self.load_fonts()
        self.load_sounds()
        self.define_colors()
    def define_colors(self):
        self.GRAY=(127,127,127)
        self.WHITE=(255,255,255)
        self.BLACK=(0,0,0)
        self.GREEN=(0,255,0)
        self.BLUE=(0,0,255)
        self.SKYBLUE=(135,206,235)
        self.YELLOW=(255,255,0)
        self.RED=(255,0,0)
        self.GOLDEN=(255,199,51)
    def load_images(self):
        self.image_path = os.path.join(os.path.dirname(__file__), "images")
        self.image_background=pygame.image.load(os.path.join(self.image_path,"bg.png"))
    def load_fonts(self):
        self.font_path = os.path.join(os.path.dirname(__file__), "fonts")
    def load_sounds(self):
        self.sound_path = os.path.join(os.path.dirname(__file__), "sounds")
class Tube(objects):
    def __init__(self,x,y,angle,width_image,height_image):
        super().__init__()
        self.image=pygame.image.load(os.path.join(self.image_path,"tubo.png"))
        self.image=pygame.transform.rotate(self.image,angle)
        self.image=pygame.transform.scale(self.image,(width_image,height_image))
        self.rect=pygame.Rect(x,y,width_image,height_image)
        self.x=x
        self.y=y
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
class flapy_ghost(objects):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(os.path.join(self.image_path,"flappy_ghost.png"))
        self.image=pygame.transform.scale(self.image,(100,100))
class Game(objects):
    def __init__(self,model=None):
        super().__init__()
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.model=model
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        self.scores=0
        self.reward=0
        self.game_over=False
        self.reset=False
        self.gravity=0.25
        self.down_gravity=0
        self.jumper=-5
        self.isjumper=False
        self.flap_ghost=flapy_ghost()
        self.space_tubes = 200
        self.speed_tubes = 5
        self.instances()
        self.objects()
    def instances(self):
        self.x_position = [self.width + i * self.space_tubes for i in range(6)]
        self.tubes = [Tube(x, random.randint(self.height//2, self.height), 0, 100, self.height//2) for x in self.x_position]
        self.tubes_invert=[Tube(x,random.randint(-self.height//2,0-100),180,100,self.height//2) for x in self.x_position]
    def objects(self,object2=None,object3=None):
        self.object1=Rect(100,100,40,40)
        self.object2=object2
        self.object3=object3
    def update(self):
        if not self.isjumper:
            self.down_gravity+=self.gravity
            self.object1.y+=self.down_gravity
        if self.object1.y<=-20:
            self.object1.y=-15
            self.down_gravity=self.gravity
        if self.object1.y>=self.height+100:self.restart()
    def events(self):
        self.generator_tubes(self.screen,self.tubes,self.speed_tubes,self.space_tubes,self.height//2,self.height,"object2")
        self.generator_tubes(self.screen,self.tubes_invert,self.speed_tubes,self.space_tubes,-self.height//2,-100,"object3")
        self.reward+=0.1
    def generator_tubes(self,screen,tubes,speed_tubes,space_tubes,height_init,height_finish,objects=None):
        for tube in tubes:
            tube.x -= speed_tubes
            tube.rect.topleft = (tube.x, tube.y)
            if tube.x < -200:
                last_tube = max(tubes, key=lambda t: t.x)
                tube.x = last_tube.x + space_tubes
                tube.y = random.randint(height_init, height_finish)
            self.collision(tube)
            self.define_objects(objects,tube)
            tube.draw(screen)
    def collision(self,tube):
        if tube.rect.colliderect(self.object1):self.restart()
    def define_objects(self,objects,tube):
        if objects=="object2":self.object2=tube.rect
        if objects=="object3":self.object3=tube.rect
    def backgrounds(self):
        for background in [0,360,720,1080]:
            self.screen.blit(self.image_background, (background, 0))
    def draw(self):
        self.backgrounds()
        self.screen.blit(self.flap_ghost.image,(self.object1.x-30,self.object1.y-20))
        self.events()
        self.filt()
    def jump(self):
        self.isjumper=True
        if self.isjumper:
            self.down_gravity=self.jumper
            self.isjumper=False
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:self.game_over=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:self.running=False
                if event.key==pygame.K_SPACE:self.jump()
    def get_state(self):
        return np.array([self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y])
    def IA_actions(self,action):
        if action[0]>0 and self.object2.top > 0 or action[0]<0 and self.object2.bottom < self.height:self.jump()
    def restart(self):
        self.instances()
        self.objects()
        self.events()
        self.scores=0
        self.reward=0
        self.running=False
    def filt(self):
        background=pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        background.fill((0,0,0,50))
        self.screen.blit(background,(0,0))
    def run_with_model(self):
        self.running=True
        score=0
        while self.running and self.game_over==False:
            self.handle_keys()
            self.update()
            self.draw()
            state=self.get_state()
            action = self.model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
            self.IA_actions(action)
            score =int(self.reward)
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return score
if __name__=="__main__":
    input_size = 6 
    output_size = 2 
    game=Game()
    best_model = genetic_algorithm(game, input_size, output_size)
    game.model = best_model
pygame.quit()
sys.exit()