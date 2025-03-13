class CollisionHandler:
    def __init__(self, game):
        self.game = game
        self.sound_death = game.sound_death
    def check_collision(self, object1, object2):return object1.check_collision(object2)
    