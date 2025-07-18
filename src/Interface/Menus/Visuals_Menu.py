from .Base_Menu import BaseMenu
class VisualsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
    def _change_items(self,item,background,number):
        self.config.config_visuals[item]=((self.config.config_visuals[item] + number) % len(self.config.config_visuals[background]))
        self.load_visuals()
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self._items_visuals()
        self.screen.blit(self.interface.font3.render("Visuals", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())
    def _items_visuals(self):
        self.screen.blit(self.interface.flappy_ghost,(self.interface.players[0].rect.x-30,self.interface.players[0].rect.y+50))
        self.screen.blit(self.interface.tubes[0].tube_image,(self.WIDTH/2-50,self.HEIGHT/2))
        self.screen.blit(self.interface.tubes_invert[0].tube_image,(self.WIDTH/2+180,0))