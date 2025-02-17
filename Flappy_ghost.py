import random
import numpy as np
from Genetic_Algorithm import *
from Interface import *
from Player import *
class Game(interface):
    def __init__(self,model=None):
        super().__init__()
        self.model=model
        self.load_AI()
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        self.game_over=False
        self.gravity=0.25
        self.jumper=-5
        self.space_tubes = 200
        self.speed_tubes = 5
        self.generation=0
        self.instances()
        self.objects()
        self.play_music()
    def instances(self):
        self.x_position = [self.width + i * self.space_tubes for i in range(6)]
        self.tubes = [Tube(x, random.randint(self.height//2, self.height), 0, 100, self.height//2) for x in self.x_position]
        self.tubes_invert=[Tube(x,random.randint(-self.height//2,0-100),180,100,self.height//2) for x in self.x_position]
        self.population()
    def population(self):
        self.players = [Player(100,100,40,40) for _ in range(self.config_AI["population_value"] if self.mode_game["Training AI"] else 1)]
        self.models = []
    def objects(self):
        self.object2=Rect(0,0,0,0)
        self.object3=Rect(0,0,0,0)
        self.object4=Rect(0,0,0,0)
        self.object5=Rect(0,0,0,0)
    def update(self):
        for player in self.players:
            if player.active:
                player.fall(self.gravity)
                if player.rect.y<=-20:
                    player.rect.y=-15
                    player.down_gravity=self.gravity
                if player.rect.y>=self.height+100:self.sounddeath(player=player,reward=-20)
                player.reward += 0.1
    def creates_tubes(self):
        self.generator_tubes(self.screen,self.tubes,self.speed_tubes,self.space_tubes,self.height//2,self.height,"object2")
        self.generator_tubes(self.screen,self.tubes_invert,self.speed_tubes,self.space_tubes,-self.height//2,-100,"object3")
    def generator_tubes(self,screen,tubes,speed_tubes,space_tubes,height_init,height_finish,objects=None,current_tube=None,next_tube1=None,next_tube2=None):
        for tube in tubes:
            tube.x -= speed_tubes
            tube.rect.topleft = (tube.x, tube.y)
            if tube.x < -100:
                last_tube = max(tubes, key=lambda t: t.x)
                tube.x = last_tube.x + space_tubes
                tube.y = random.randint(height_init, height_finish)
                self.reward+=5
                self.scores+=0.5
            self.collision(tube)
            tube.draw(screen)
        sorted_tubes = sorted(tubes, key=lambda t: t.x)
        for player in self.players:
            if player.active:
                for i, tube in enumerate(sorted_tubes):
                    if tube.x > player.rect.x:
                        current_tube = tube
                        next_tube1 = sorted_tubes[i + 1] if i + 1 < len(sorted_tubes) else None
                        next_tube2 = sorted_tubes[i + 2] if i + 2 < len(sorted_tubes) else None
                        break
        if current_tube:setattr(self, objects, current_tube.rect)
        if next_tube1:setattr(self, "object4", next_tube1.rect)
        if next_tube2:setattr(self, "object5", next_tube2.rect)
    def collision(self,tube):
        for player in self.players:
            if player.active and tube.rect.colliderect(player):self.sounddeath(reward=-25)
    def sounddeath(self,player,sound=True,reward=0):
        if sound:
            self.sound_death.play(loops=0)
            player.reward+=reward
            self.restart()
            sound=False
    def backgrounds(self):
        for background in [0,360,720,1080]:self.screen.blit(self.image_background, (background, 0))
    def draw(self):
        self.backgrounds()
        for player in self.players:
            if player.active:self.screen.blit(self.flappy_ghost,(player.rect.x-30,player.rect.y-20))
        self.draw_interfaces()
    def handle_keys(self):
        for event in pygame.event.get():
            self.event_quit(event)
            self.events(event)
            self.event_keydown(event)
            if self.main==6:self.event_keys(event)
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
            if self.mode_game["Player"] and event.key==self.config_keys["key_jump"]:self.jump()
            if self.main==-1 and self.mode_game["Training AI"]:
                if event.key==pygame.K_ESCAPE:self.restart()
                if event.key==K_1:save_model(self.model, torch.optim.Adam(self.model.parameters(), lr=0.001),self.model_path)
            if self.main==1 and event.key==K_r:
                self.reset()
                self.main=-1
    def events(self,event):
        if event.type == self.EVENT_BACKGROUND and self.main==-1:
            self.speed_tubes+=0.5
            self.config_visuals["value_background"]=random.randint(0,1)
            self.load_images()
    def get_state(self,player=Player(350, 600 - 35, 25, 25)):
        dist_to_tube_x = self.object2.x - player.rect.x
        dist_to_tube_y = player.rect.y - self.object2.y
        dist_to_tube_invert_y = player.rect.y - self.object3.y
        dist_to_tube_to_tube_invert_y = self.object3.y - self.object2.y
        return np.array([player.rect.x,player.rect.y,self.object2.x,self.object2.y,self.object3.x,self.object3.y,self.object4.x,self.object4.y,self.object5.x,self.object5.y,dist_to_tube_x,dist_to_tube_y,dist_to_tube_invert_y,dist_to_tube_to_tube_invert_y,self.down_gravity,self.speed_tubes])
    def AI_actions(self,action):self.down_gravity = action[0] * 10
    def restart(self):
        if self.mode_game["Training AI"]:self.reset(False)
        if self.mode_game["Player"] or self.mode_game["AI"]:self.main=1
    def reset(self,running=True):
        self.running=running
        self.instances()
        self.objects()
        self.creates_tubes()
        self.gravity=0.25
        self.scores=0
        self.speed_tubes=5
    def type_mode(self):self.actions_AI(self.model if self.mode_game["Training AI"] else self.model_training)
    def actions_AI(self,models):
        def actions(player,model):
            state=self.get_state(player)
            action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
            self.AI_actions(player,action)
        try:
            for player, model in zip(self.players, models):
                if player.active:actions(player,model)
        except:actions(self.players[0],models)
    def run_with_model(self):
        self.running=True
        for player in self.players:player.reward = 0
        while self.running and self.game_over==False:
            self.handle_keys(),self.draw()
            if self.main==-1:
                if self.mode_game["AI"] or self.mode_game["Training AI"]:self.type_mode()
                self.update(),self.creates_tubes()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        return [player.reward for player in self.players]