import pygame,random,os,sys
from pygame.locals import *
import numpy as np
from Genetic_Algorithm import *
class objects():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.config()
        self.width=800
        self.height=600
        self.load_images()
        self.load_fonts()
        self.load_sounds()
        self.define_colors()
        self.new_events()
    def config(self):
        self.config_visuals={"background":["bg.png","bg_night.png"],
                            "value_background":0}
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
        self.image_background=pygame.image.load(os.path.join(self.image_path,self.config_visuals["background"][self.config_visuals["value_background"]]))
    def load_fonts(self):
        self.font_path = os.path.join(os.path.dirname(__file__), "fonts")
        self.font=pygame.font.Font(None,25)
        self.font2=pygame.font.Font(None,35)
        self.font2_5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),30)
        self.font3=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),60)
        self.font4=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),75)
        self.font5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),20)
    def load_sounds(self):
        self.sound_path = os.path.join(os.path.dirname(__file__), "sounds")
        self.sound_touchletters=pygame.mixer.Sound(os.path.join(self.sound_path,"touchletters.wav"))
        self.sound_buttonletters=pygame.mixer.Sound(os.path.join(self.sound_path,"buttonletters.mp3"))
    def new_events(self):
        self.EVENT_BACKGROUND = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENT_BACKGROUND,10000)
class Tube(objects):
    def __init__(self,x,y,angle,width_image,height_image):
        super().__init__()
        self.load_tube(x,y,angle,width_image,height_image)
    def load_tube(self,x,y,angle,width_image,height_image):
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
        self.load_flappy_ghost()
    def load_flappy_ghost(self):
        self.image=pygame.image.load(os.path.join(self.image_path,"flappy_ghost.png"))
        self.image=pygame.transform.scale(self.image,(100,100))
class Game(objects):
    def __init__(self,model=None):
        super().__init__()
        self.model=model
        self.screen=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys
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
        self.button_states={}
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
            if tube.x==self.object1.x:
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
        for background in [0,360,720,1080]:
            self.screen.blit(self.image_background, (background, 0))
    def draw(self):
        self.backgrounds()
        self.screen.blit(self.flap_ghost.image,(self.object1.x-30,self.object1.y-20))
        self.filt(50)
        self.main_menu()
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
        if event.type==pygame.QUIT:self.game_over=True
    def event_keydown(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:self.restart()
            if event.key==pygame.K_SPACE:self.jump()
    def events(self,event):
        if event.type == self.EVENT_BACKGROUND and self.main==-1:
            self.config_visuals["value_background"]=random.randint(0,1)
            self.load_images()
    def get_state(self):
        return np.array([self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y])
    def IA_actions(self,action):
        if action[0]>0 and self.object2.top > 0 or action[0]<0 and self.object2.bottom < self.height:self.jump()
    def restart(self):
        self.instances()
        self.objects()
        self.creates_tubes()
        self.scores=0
        self.reward=0
        self.running=False
    def filt(self,number):
        background=pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        background.fill((0,0,0,number))
        self.screen.blit(background,(0,0))
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.button(self.screen,-1,self.font2_5,"PLAY",self.WHITE,(self.width/2-80,self.height/2-150),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
            self.button(self.screen,None,self.font2_5,"QUIT",self.WHITE,(self.width/2-80,self.height/2-115),self.GOLDEN,sound_hover=self.sound_buttonletters,sound_touch=self.sound_touchletters)
    def game_over_menu(self):
        if self.main==1:
            pass
    def mode_game_menu(self):
        if self.main==2:
            pass
    def pausa_menu(self):
        if self.main==3:
            pass
    def menu_options(self):
        if self.main==4:
            pass
    def visuals_menu(self):
        if self.main==5:
            pass
    def keys_menu(self):
        if self.main==6:
            pass
    def button(self,screen,main:int,font,text:str,color,position,color2=None,pressed=True,command=None,detect_mouse=True,command2=None,sound_hover=None,sound_touch=None):
        button_id = (text, position)
        if button_id not in self.button_states:self.button_states[button_id] = {'hover_played': False, 'click_played': False, 'is_hovering': False}
        state = self.button_states[button_id]
        button=screen.blit(font.render(text,True,color),position)
        is_hovering_now = button.collidepoint(self.mouse_pos)
        if detect_mouse:
            if is_hovering_now:
                screen.blit(font.render(text,True,color2),position)
                if not state['is_hovering']:
                    if not state['hover_played']:
                        sound_hover.play(loops=0)
                        state['hover_played'] = True
                    state['is_hovering'] = True
            else:state['is_hovering'],state['hover_played']=False,False
        self.pressed_button(button,pressed,is_hovering_now,state,sound_touch,main,command,command2)
    def pressed_button(self,button,pressed,is_hovering_now,state,sound_touch,main,command=None,command2=None):
        if self.pressed_mouse[0] and pressed:
            if is_hovering_now:
                if not state['click_played']:
                    sound_touch.play(loops=0)
                    state['click_played'] = True
                    if main!=None:self.main=main
                    if command!=None:command()
                    if command2!=None:command2()
            else:state['click_played'] = False
        if not pressed:return button
    # def button_arrow(self,main,position,position2,color,number:int,number2=None,pressed=True,detect_mouse=True,command=None):
    #     arrow_button=pygame.draw.polygon(self.screen, color, position)
    #     if detect_mouse:
    #         if arrow_button.collidepoint(self.mouse_pos):
    #             pygame.draw.polygon(self.screen, self.WHITE, position2)
    #             if self.notsound_playing[number]:
    #                 self.sound_buttonletters.play(loops=0)
    #                 self.notsound_playing[number]=False
    #         else:self.notsound_playing[number]=True
    #     if self.pressed_mouse[0] and pressed:
    #         if arrow_button.collidepoint(self.mouse_pos):
    #             if self.notsound_playing[number2]:
    #                 self.sound_touchletters.play(loops=0)
    #                 self.notsound_playing[number2]=False
    #                 if main!=None:self.main=main
    #                 if command!=None:command()
    #         else:self.notsound_playing[number2]=True
    #     if pressed==False:return arrow_button
    def type_mode(self):
        state=self.get_state()
        action = self.model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.IA_actions(action)
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
if __name__=="__main__":
    input_size = 6 
    output_size = 2 
    game=Game()
    best_model = genetic_algorithm(game, input_size, output_size)
    game.model = best_model
pygame.quit()
sys.exit()