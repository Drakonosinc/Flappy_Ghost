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
    def get_next_object(self, player, objects):
        sorted_objects = sorted(objects, key=lambda t: t.rect.x)
        for i, object in enumerate(sorted_objects):
            if object.rect.x > player.rect.x:
                current_object = object
                next_object1 = sorted_objects[i + 1] if i + 1 < len(sorted_objects) else None
                next_object2 = sorted_objects[i + 2] if i + 2 < len(sorted_objects) else None
                return current_object, next_object1, next_object2
        return None, None, None
    def update_objects(self, objects, current_object, next_object1, next_object2):
        if current_object:setattr(self.game, objects, current_object.rect)
        if next_object1:setattr(self.game, "object4", next_object1.rect)
        if next_object2:setattr(self.game, "object5", next_object2.rect)