import json,os
from pygame.locals import *
class Config():
    def __init__(self):self.base_dir = os.path.dirname(os.path.dirname(__file__))
    def load_config(self):
        try:
            self.config_path = os.path.join(self.base_dir, "Config")
            with open(os.path.join(self.config_path,"config.json"), 'r') as file:config = json.load(file)
            self.config_visuals = config["config_visuals"]
            self.config_keys = config["config_keys"]
            self.config_sounds = config["config_sounds"]
            self.config_AI = config["config_AI"]
        except:self.config(alls=True),self.save_config()
    def config(self,visuals=False,keys=False,sounds=False,AI=False,alls=False):
        if visuals or alls:self.config_visuals={"background":["bg.png","bg_night.png"],"value_background":0,
                            "flyers":["flappy_ghost.png"],"value_flyers":0,
                            "tubes":["tube.png"],"value_tubes":0}
        if keys or alls:self.config_keys={"key_jump":K_SPACE,"Name_key1":"SPACE"}
        if sounds or alls:self.config_sounds={"sound_menu":True,"sound_game":True}
        if AI or alls:self.config_AI={"generation_value":100,"population_value":20,"try_for_ai":3,"model_save":False}
    def save_config(self):
        self.config_path = os.path.join(self.base_dir, "Config")
        config = {"config_visuals": self.config_visuals,"config_keys": self.config_keys,"config_sounds":self.config_sounds,"config_AI":self.config_AI}
        with open(os.path.join(self.config_path,"config.json"), 'w') as file:json.dump(config, file, indent=4)