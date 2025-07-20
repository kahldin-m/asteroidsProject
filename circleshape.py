import pygame # type: ignore

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def detect_collision(self, other):
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        if distance < self.radius + other.radius:
            return True
        return False
    
    def check_bounds(self, screen_width=1280, screen_height=720):
        if self.position.x < -self.radius:
            self.position.x = screen_width + self.radius
        elif self.position.x > screen_width + self.radius:
            self.position.x = -self.radius
            
        if self.position.y < -self.radius:
            self.position.y = screen_height + self.radius
        elif self.position.y > screen_height + self.radius:
            self.position.y = -self.radius