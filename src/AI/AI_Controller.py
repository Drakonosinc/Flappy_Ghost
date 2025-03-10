import torch
class AIHandler:
    def __init__(self, game):
        self.game = game
        self.models = []
        
    def get_state(self, player):
        dist_to_tube_x = self.game.object2.x - player.rect.x
        dist_to_tube_y = player.rect.y - self.game.object2.y
        dist_to_tube_invert_y = player.rect.y - self.game.object3.y
        dist_to_tube_to_tube_invert_y = self.game.object3.y - self.game.object2.y
        