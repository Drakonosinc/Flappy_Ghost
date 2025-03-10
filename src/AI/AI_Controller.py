import torch
import numpy as np
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
            player.dy, self.game.speed_tubes])
    def AI_actions(self, player, action):player.dy = action[0] * 10
    def actions_AI(self, models):
        def actions(player, model):
            state = self.get_state(player)
            action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
            self.AI_actions(player, action)
        try:
            for player, model in zip(self.game.players, models):
                if player.active:actions(player, model)
        except:actions(self.game.players[0], models)
    def get_reward(self, reward: list) -> list:
        for player in self.game.players:
            reward.append(player.reward)
            player.reward = 0
            player.reset(40, 40)
        return reward