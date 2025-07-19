from .Base_Menu import BaseMenu
class VisualsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons['decrease_player_button'] = factory.create_TextButton({"font": self.interface.font3_5,"text": "<","position": (self.interface.players[0].rect.x-40,self.interface.players[0].rect.y+70),"command1":lambda:self.change_items("value_flyers","flyers",-1)})
        self.buttons['increase_player_button'] = factory.create_TextButton({"font": self.interface.font3_5,"text": ">","position": (self.interface.players[0].rect.x+60,self.interface.players[0].rect.y+70),"command1":lambda:self.change_items("value_flyers","flyers",1)})
        self.buttons['decrease_tube_button'] = factory.create_TextButton({"font": self.interface.font3_5,"text": "<","position": (self.WIDTH/2-95,self.HEIGHT/2),"command1":lambda:self.change_items("value_tubes","tubes",-1)})
    def _change_items(self,item,background,number):
        self.config.config_visuals[item]=((self.config.config_visuals[item] + number) % len(self.config.config_visuals[background]))
        self._load_visuals()
    def _load_visuals(self):
        self.interface.load_images()
        self.interface.instances()
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self._items_visuals()
        self.screen.blit(self.interface.font3.render("Visuals", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())
    def _items_visuals(self):
        self.screen.blit(self.interface.flappy_ghost,(self.interface.players[0].rect.x-30,self.interface.players[0].rect.y+50))
        self.screen.blit(self.interface.tubes[0].tube_image,(self.WIDTH/2-50,self.HEIGHT/2))
        self.screen.blit(self.interface.tubes_invert[0].tube_image,(self.WIDTH/2+180,0))