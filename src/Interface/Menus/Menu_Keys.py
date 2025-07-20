from .Base_Menu import BaseMenu
from pygame.locals import KEYDOWN
class KeysMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.utils_keys = {key: False for i, key in enumerate(self.config.config_keys.keys()) if i % 2 == 0}
        self.buttons = {}
        self.buttons_keys = {}
        self.key = None