from Loaders.Load_elements import *
from .Elements_interface import *
from .Menus import *
class interface(load_elements,BaseMenu):
    def __init__(self):
        load_elements.__init__(self)
        BaseMenu.__init__(self,self)
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys, 7=sound menu
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.initialize_menus()
    def initialize_menus(self):
        self.main_menu = MainMenu(self)
        self.game_over_menu = GameOver(self)
        self.game_mode_menu = GameMode(self)
        self.pause_menu = Pause(self)
        self.options_menu = OptionsMenu(self)
        self.visuals_menu = VisualsMenu(self)
        self.keys_menu = KeysMenu(self)
        self.sounds_menu = SoundsMenu(self)
    def play_music(self):
        self.check_sounds()
        self.sound_back.set_volume(0.5)
    def draw_interfaces(self):
        menu_routes = {
            0: self.main_menu.render,
            1: self.game_over_menu.render,
            2: self.game_mode_menu.render,
            3: self.pause_menu.render,
            4: self.options_menu.render,
            5: self.visuals_menu.render,
            6: self.keys_menu.render,
            7: self.sounds_menu.render,}
        if self.main in menu_routes:menu_routes[self.main]()
        self.draw_generation()
    def draw_buttons(self):
        self.button_factory_f2_5 = ElementsFactory({"screen": self.screen,"font": self.font2_5,"hover_color": self.GOLDEN,"sound_hover": self.sound_buttonletters,"sound_touch": self.sound_touchletters})
        self.main_menu.setup_buttons()
        self.game_over_menu.setup_buttons()
        self.game_mode_menu.setup_buttons()
        self.pause_menu.setup_buttons()
        self.options_menu.setup_buttons()
        self.visuals_menu.setup_buttons()
        self.keys_menu.setup_buttons()
        self.sounds_menu.setup_buttons()
    def draw_generation(self):
        if self.main==-1 and self.mode_game["Training AI"]:self.screen.blit(self.font3_5.render(f"Generation: {int(self.generation)}", True, "orange"),(35,0))
    def check_sounds(self):
        self.sound_back_game.stop()
        self.sound_back.play(loops=-1) if self.sounds_menu.sound_type["value_menu"] else None
    def show_score(self,player):
        if self.main==-1 or self.main==1:self.screen.blit(self.font.render(f"Score: {int(player.scores)}", True, "orange"),(35,self.height-50))