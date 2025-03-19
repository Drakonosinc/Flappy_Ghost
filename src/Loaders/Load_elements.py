import pygame,os
from pygame.locals import *
from AI.Genetic_Algorithm import *
from .Config_Loader import *
class objects():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.config=Config()
        self.config.load_config()
        self.config_screen()
        self.load_images()
        self.load_fonts()
        self.load_sounds()
        self.define_colors()
        self.new_events()
    def config_screen(self):
        self.width,self.height=800,600
        self.screen=pygame.display.set_mode((self.width,self.height))
    def load_AI(self):
        self.model_path=os.path.join(self.config.base_dir, "AI/best_model.pth")
        self.model_training = load_model(self.model_path, 16, 1) if os.path.exists(self.model_path) else None
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
        self.image_path = os.path.join(self.config.base_dir, "images")
        self.image_background=pygame.image.load(os.path.join(self.image_path,self.config.config_visuals["background"][self.config.config_visuals["value_background"]]))
        self.flappy_ghost=pygame.image.load(os.path.join(self.image_path,self.config.config_visuals["flyers"][self.config.config_visuals["value_flyers"]]))
        self.flappy_ghost=pygame.transform.scale(self.flappy_ghost,(100,100))
    def load_fonts(self):
        self.font_path = os.path.join(self.config.base_dir, "fonts")
        self.font=pygame.font.Font(None,25)
        self.font1=pygame.font.SysFont("times new roman", 80)
        self.font2=pygame.font.Font(None,35)
        self.font2_5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),30)
        self.font3=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),60)
        self.font3_5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),30)
        self.font4=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),75)
        self.font5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),20)
        self.font5_5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),20)
    def load_sounds(self):
        self.sound_path = os.path.join(self.config.base_dir, "sounds")
        self.sound_jump=pygame.mixer.Sound(os.path.join(self.sound_path,"jump.aiff"))
        self.sound_touchletters=pygame.mixer.Sound(os.path.join(self.sound_path,"touchletters.wav"))
        self.sound_buttonletters=pygame.mixer.Sound(os.path.join(self.sound_path,"buttonletters.mp3"))
        self.sound_exit=pygame.mixer.Sound(os.path.join(self.sound_path,"exitbutton.wav"))
        self.sound_back=pygame.mixer.Sound(os.path.join(self.sound_path,"sound_back.wav"))
        self.sound_back_game=pygame.mixer.Sound(os.path.join(self.sound_path,"sound_back_game.wav"))
        self.sound_death=pygame.mixer.Sound(os.path.join(self.sound_path,"death.wav"))
        self.sound_back.set_volume(0.4)
        self.sound_back_game.set_volume(0.4)
    def new_events(self):
        self.EVENT_BACKGROUND = pygame.USEREVENT + 2
        pygame.time.set_timer(self.EVENT_BACKGROUND,10000)