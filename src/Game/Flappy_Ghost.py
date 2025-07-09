import random
from Interface.Interface import *
from Entities import *
from Physics import *
from AI import *
class Game(interface):
    def __init__(self):
        super().__init__()
        self.load_AI()
        self.physics = PhysicsHandler()
        self.ai_handler = AIHandler(self)
        self.collision_handler = CollisionHandler(self)
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        self.game_over=False
        self.exit=False
        self.space_tubes = 200
        self.speed_tubes = 5
        self.generation=0
        self.instances()
        self.population()
        self.objects()
        self.draw_buttons()
        self.play_music()
    def instances(self):
        self.x_position = [self.width + i * self.space_tubes for i in range(6)]
        self.tubes = [Tube(x, random.randint(self.height//2, self.height), 0, 100, self.height//2, load_elements()) for x in self.x_position]
        self.tubes_invert=[Tube(x,random.randint(-self.height//2,0-100),180,100,self.height//2, load_elements()) for x in self.x_position]
    def population(self):
        self.players = [Player(100,100,40,40) for _ in range(self.config.config_AI["population_value"] if self.mode_game["Training AI"] else 1)]
        self.models = []
    def objects(self):
        self.object2=Rect(0,0,0,0)
        self.object3=Rect(0,0,0,0)
        self.object4=Rect(0,0,0,0)
        self.object5=Rect(0,0,0,0)
    def update(self,player):
        if not player.isjumper:self.physics.apply_gravity(player)
        if player.rect.y<=-20:
            player.rect.y=-15
            player.dy=self.physics.gravity
        if player.rect.y>=self.height+100:self.collision_handler.handle_collision(player, reward=-20)
        player.reward += 0.1
    def creates_tubes(self):
        self.generator_tubes(self.screen,self.tubes,self.speed_tubes,self.space_tubes,self.height//2,self.height,"object2")
        self.generator_tubes(self.screen,self.tubes_invert,self.speed_tubes,self.space_tubes,-self.height//2,-100,"object3")
    def generator_tubes(self,screen,tubes,speed_tubes,space_tubes,height_init,height_finish,objects=None):
        for tube in tubes:
            tube.move_tube_x(speed_tubes)
            tube.rect.topleft = (tube.rect.x, tube.rect.y)
            tube.draw(screen)
            for player in self.players:
                if player.active:
                    if tube.rect.x < -100:
                        last_tube = max(tubes, key=lambda t: t.rect.x)
                        tube.rect.x = last_tube.rect.x + space_tubes
                        tube.rect.y = random.randint(height_init, height_finish)
                        player.reward+=5
                        player.scores+=0.5
                    self.handle_tube_collision(player, tube, objects)
    def handle_tube_collision(self, player, tube, objects):
        current_object, next_object1, next_object2 = self.collision_handler.get_next_object(player, self.tubes)
        self.collision_handler.update_objects(objects, current_object, next_object1, next_object2)
        if self.collision_handler.check_collision(player, tube):self.collision_handler.handle_collision(player)
    def backgrounds(self):
        for background in [0,360,720,1080]:self.screen.blit(self.image_background, (background, 0))
    def draw(self):
        self.backgrounds()
        self.draw_interfaces()
    def draw_players(self,player):
        self.screen.blit(self.flappy_ghost,(player.rect.x-30,player.rect.y-20))
        self.show_score(player)
    def handle_keys(self):
        for event in pygame.event.get():
            self.event_quit(event)
            self.events(event)
            self.event_keydown(event)
            if self.main==6:self.event_keys(event)
            if self.main==2:self.scroll.events(event)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
    def event_quit(self,event):
        if event.type==pygame.QUIT:self.close_game()
    def close_game(self):
        self.sound_exit.play(loops=0)
        self.game_over,self.exit,self.running=True,True,False
    def event_keydown(self,event):
        if event.type==pygame.KEYDOWN:
            if self.main==3 and event.key==K_p:self.main=-1
            elif self.main==-1 and event.key==K_p:self.main=3
            if self.mode_game["Player"] and event.key==self.config.config_keys["key_jump"]:self.players[0].jump(self.physics.jump_force,self.sound_jump)
            if self.main==-1 and self.mode_game["Training AI"]:
                if event.key==pygame.K_ESCAPE:self.restart()
            if self.main==1 and event.key==K_r:self.change_mains({"main":-1,"command":self.reset})
    def events(self,event):
        if event.type == self.EVENT_BACKGROUND and self.main==-1:
            self.speed_tubes+=0.5
            self.config.config_visuals["value_background"]=random.randint(0,1)
            self.load_images()
    def restart(self):
        if all(not player.active for player in self.players) and self.mode_game["Training AI"]:self.reset(False,1)
        if self.mode_game["Player"] or self.mode_game["AI"]:self.change_mains({"main":1,"color":self.RED,"limit":100,"command":self.reset})
    def reset(self,running=True,type_reset=0):
        self.running=running
        self.objects()
        self.speed_tubes=5
        self.instances()
        if type_reset==0:self.players[0].reset()
    def type_mode(self):
        self.ai_handler.actions_AI(self.models if self.mode_game["Training AI"] else self.model_training)
    def get_reward(self, reward: list) -> list:return self.ai_handler.get_reward(reward)
    def item_repeat_run(self):
        self.handle_keys()
        pygame.display.flip()
        self.clock.tick(self.FPS)
    def run(self):
        self.running = True
        while self.running:self.item_repeat_run(),self.draw()
    def main_run(self):
        if self.mode_game["AI"] or self.mode_game["Training AI"]:self.type_mode()
        for player in self.players:
            if player.active:self.update(player),self.draw_players(player)
        self.creates_tubes()
    def run_with_models(self):
        self.running=True
        while self.running and self.game_over==False:
            self.draw()
            if self.main==-1:self.main_run()
            self.item_repeat_run()
        return self.get_reward([])