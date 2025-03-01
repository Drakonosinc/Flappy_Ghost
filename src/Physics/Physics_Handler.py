class PhysicsHandler:
    def __init__(self, gravity=0.25, jump_force=-12):
        self.gravity = gravity
        self.jump_force = jump_force
    def apply_gravity(self, player):
        player.dy += self.gravity
        player.rect.y += player.dy
