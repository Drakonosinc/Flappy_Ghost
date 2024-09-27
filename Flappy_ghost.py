import random
from pygame.locals import *
import numpy as np
from Genetic_Algorithm import *
from Interface import *
class Game(interface):
    def __init__(self,model=None):
        super().__init__()
        self.model=model
        self.load_AI()
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        self.scores=0
        self.reward=0
        self.game_over=False
        self.gravity=0.25
        self.down_gravity=0
        self.jumper=-5
        self.isjumper=False
        self.flap_ghost=ghost()
        self.space_tubes = 200
        self.speed_tubes = 5
        self.instances()
        self.objects()
        self.play_music()
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
    def creates_tubes(self):
        self.generator_tubes(self.screen,self.tubes,self.speed_tubes,self.space_tubes,self.height//2,self.height,"object2")
        self.generator_tubes(self.screen,self.tubes_invert,self.speed_tubes,self.space_tubes,-self.height//2,-100,"object3")
    def generator_tubes(self,screen,tubes,speed_tubes,space_tubes,height_init,height_finish,objects=None):
        for tube in tubes:
            tube.x -= speed_tubes
            tube.rect.topleft = (tube.x, tube.y)
            if tube.x < -200:
                last_tube = max(tubes, key=lambda t: t.x)
                tube.x = last_tube.x + space_tubes
                tube.y = random.randint(height_init, height_finish)
                self.reward+=0.5
                self.scores+=0.5
            self.collision(tube)
            self.define_objects(objects,tube)
            tube.draw(screen)
    def collision(self,tube):
        if tube.rect.colliderect(self.object1):self.restart()
    def define_objects(self,objects,tube):
        if objects=="object2":self.object2=tube.rect
        if objects=="object3":self.object3=tube.rect
    def backgrounds(self):
        for background in [0,360,720,1080]:self.screen.blit(self.image_background, (background, 0))
    def draw(self):
        self.backgrounds()
        self.screen.blit(self.flap_ghost.image,(self.object1.x-30,self.object1.y-20))
        self.draw_interfaces()
    def jump(self):
        self.isjumper=True
        if self.isjumper:
            self.down_gravity=self.jumper
            self.isjumper=False
    def handle_keys(self):
        for event in pygame.event.get():
            self.event_quit(event)
            self.events(event)
            self.event_keydown(event)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
    def event_quit(self,event):
        if event.type==pygame.QUIT:self.close_game()
    def close_game(self):
        self.sound_exit.play(loops=0)
        self.game_over=True
    def event_keydown(self,event):
        if event.type==pygame.KEYDOWN:
            if self.main==3 and event.key==K_p:self.main=-1
            elif self.main==-1 and event.key==K_p:self.main=3
            if event.key==pygame.K_ESCAPE:self.restart()
            if self.mode_game["Player"]:
                if event.key==pygame.K_SPACE:self.jump()
            if self.main==-1:
                if event.key==K_1:save_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001),self.model_path)
            if self.main==1:
                if event.key==K_r:
                    self.reset()
                    self.main=-1
    def events(self,event):
        if event.type == self.EVENT_BACKGROUND and self.main==-1:
            self.speed_tubes+=0.5
            self.config_visuals["value_background"]=random.randint(0,1)
            self.load_images()
    def get_state(self):
        return np.array([self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y])
    def AI_actions(self,action):
        if action[0]>0 and self.object2.top > 0 or action[0]<0 and self.object2.bottom < self.height:self.jump()
    def restart(self):
        if self.mode_game["Training AI"] or self.mode_game["AI"]:
            self.reset()
        if self.mode_game["Player"]:self.main=1
    def reset(self):
        self.instances()
        self.objects()
        self.creates_tubes()
        self.scores=0
        self.reward=0
        self.speed_tubes=5
        self.running=False
    def type_mode(self):
        if self.mode_game["Training AI"]:self.actions_AI(self.model)
        if self.mode_game["AI"]:self.actions_AI(self.model_training)
    def actions_AI(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.AI_actions(action)
    def run_with_model(self):
        self.running=True
        score=0
        while self.running and self.game_over==False:
            self.handle_keys()
            self.draw()
            if self.main==-1:
                self.update()
                self.creates_tubes()
                self.type_mode()
                score =int(self.reward)
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return score