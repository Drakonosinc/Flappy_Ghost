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
        return np.array([
            player.rect.x, player.rect.y,
            self.game.object2.x, self.game.object2.y,
            self.game.object3.x, self.game.object3.y,
            self.game.object4.x, self.game.object4.y,
            self.game.object5.x, self.game.object5.y,
            dist_to_tube_x, dist_to_tube_y,
            dist_to_tube_invert_y, dist_to_tube_to_tube_invert_y,
            player.dy, self.game.speed_tubes
        ])
