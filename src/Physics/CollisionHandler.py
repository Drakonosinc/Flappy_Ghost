class CollisionHandler:
    def __init__(self, game):
        self.game = game
        self.sound_death = game.sound_death
    def check_collision(self, object1, object2):return object1.check_collision(object2)
    def handle_collision(self, player, reward=-25):
        self.sound_death.play(loops=0)
        player.reward += reward
        player.active = False
        self.game.restart()
    def get_next_tubes(self, player, tubes):
        sorted_tubes = sorted(tubes, key=lambda t: t.rect.x)
        for i, tube in enumerate(sorted_tubes):
            if tube.rect.x > player.rect.x:
                current_tube = tube
                next_tube1 = sorted_tubes[i + 1] if i + 1 < len(sorted_tubes) else None
                next_tube2 = sorted_tubes[i + 2] if i + 2 < len(sorted_tubes) else None
                return current_tube, next_tube1, next_tube2
        return None, None, None
    