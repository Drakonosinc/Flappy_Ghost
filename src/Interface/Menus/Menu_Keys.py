from .Base_Menu import BaseMenu
from pygame.locals import KEYDOWN
class KeysMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.utils_keys = {key: False for i, key in enumerate(self.config.config_keys.keys()) if i % 2 == 0}
        self.buttons = {}
        self.buttons_keys = {}
        self.key = None
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Keys", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())