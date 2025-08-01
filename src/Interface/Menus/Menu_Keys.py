from .Base_Menu import BaseMenu
from pygame.locals import KEYDOWN
class KeysMenu(BaseMenu):
    def __init__(self, interface):
        super().__init__(interface)
        self.utils_keys={"key_jump":False}
        self.buttons = {}
        self.buttons_keys = {}
        self.key = None
    def setup_buttons(self):
        factory = self.interface.button_factory_f2_5
        self.buttons['back'] = factory.create_TextButton({"font": self.interface.font1,"text": "←","position": (35,self.HEIGHT-100),"command1":lambda:self.change_mains({"main":4})})
        self.buttons_keys['space_button'] = factory.create_TextButton({"text": self.config.config_keys["Name_key1"],"position": (35,self.HEIGHT/2-150),"command1":lambda:self.change_keys("key_jump","Name_key1",self.buttons_keys["space_button"])})
        self.buttons['save'] = factory.create_TextButton({"text": "Save config","position": (self.WIDTH/2+80,self.HEIGHT-85),"command1":self.config.save_config})
        self.buttons['default'] = factory.create_TextButton({"text": "Default config","position": (self.WIDTH/2+50,self.HEIGHT-50),"command1":lambda:(self.config.config(keys=True),self.change_mains({"main":6,"command":self.setup_buttons}))})
    def change_keys(self,key,key_name,button=None):
        self.key=key
        self.key_name=key_name
        self.button_key=button
        for k in self.utils_keys.keys():self.utils_keys[k]=False if k!=self.key else not self.utils_keys[self.key]
        self.check_item(self.utils_keys,self.SKYBLUE,self.WHITE,"color",**{"key_jump":self.space_button})
    def event_keys(self,event):
        if self.key!=None and (self.utils_keys[self.key] and event.type==KEYDOWN):
            self.config.config_keys[self.key]=event.key
            self.config.config_keys[self.key_name]=event.unicode.upper()
            self.check_item(self.config.config_keys,self.config.config_keys[self.key_name],self.WHITE,"text",**{self.key:self.button_key})
            self.change_keys(self.key,self.key_name)
    def render(self):
        self.screen.fill(self.interface.BLACK)
        self.screen.blit(self.interface.font3.render("Keys", True, "orange"),(35,self.HEIGHT/2-250))
        self.execute_buttons(*self.buttons.values())