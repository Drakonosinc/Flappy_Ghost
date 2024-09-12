import pygame,random,os

# colors
white=(255,255,255)
black=(0,0,0)
gray=(128,128,128)
yellow=(255,255,102)
green=(0,255,0)
blue=(0,0,255)
red=(255,0,0)
class objects():
    def __init__(self):
        self.image_path = os.path.join(os.path.dirname(__file__), "images")
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
        self.rect=pygame.Rect(100,100,40,40)
class Game(objects):
    def __init__(self):
        # super().__init__()
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.width=800
        self.height=600
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        self.background=gray
        self.score=0
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
    def instances(self):
        self.x_position = [self.width + i * self.space_tubes for i in range(6)]
        self.tubes = [Tube(x, random.randint(self.height//2, self.height), 0, 100, self.height//2) for x in self.x_position]
        self.tubes_invert=[Tube(x,random.randint(-self.height//2,0-100),180,100,self.height//2) for x in self.x_position]
    def update(self):
        if not self.isjumper:
            self.down_gravity+=self.gravity
            self.flap_ghost.rect.y+=self.down_gravity
        if self.flap_ghost.rect.y<=-20:
            self.flap_ghost.rect.y=-15
            self.down_gravity=self.gravity
        if self.flap_ghost.rect.y>=self.height+100:self.game_over=True
    def events(self):
        self.generator_tubes(self.screen,self.tubes,self.speed_tubes,self.space_tubes,self.height//2,self.height)
        self.generator_tubes(self.screen,self.tubes_invert,self.speed_tubes,self.space_tubes,-self.height//2,-100)
    def generator_tubes(self,screen,tubes,speed_tubes,space_tubes,height_init,height_finish):
        for tube in tubes:
            tube.x -= speed_tubes
            tube.rect.topleft = (tube.x, tube.y)
            if tube.x < -200:
                last_tube = max(tubes, key=lambda t: t.x)
                tube.x = last_tube.x + space_tubes
                tube.y = random.randint(height_init, height_finish)
            self.collision(tube)
            tube.draw(screen)
    def collision(self,tube):
        if tube.rect.colliderect(self.flap_ghost.rect):
            self.game_over=True
    def draw(self):
        self.screen.fill(self.background)
        self.screen.blit(self.flap_ghost.image,(self.flap_ghost.rect.x-30,self.flap_ghost.rect.y-20))
    def jump(self):
        self.isjumper=True
        if self.isjumper:
            self.down_gravity=self.jumper
            self.isjumper=False
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:self.running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:self.running=False
                if event.key==pygame.K_SPACE:self.jump()
    def run(self):
        while self.running and self.game_over==False:
            self.handle_keys()
            self.update()
            self.draw()
            self.events()
            background=pygame.Surface((self.width,self.height),pygame.SRCALPHA)
            background.fill((0,0,0,50))
            self.screen.blit(background,(0,0))
            pygame.display.flip()
            self.clock.tick(self.FPS)
            
if __name__=="__main__":
    game=Game()
    game.run()

pygame.quit()