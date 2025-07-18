from .Base_Menu import BaseMenu
class VisualsMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.buttons = {}
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self._items_visuals()
        self.screen.blit(self.interface.font3.render("Visuals", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())