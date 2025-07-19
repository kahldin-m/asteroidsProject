import pygame # type: ignore
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "black", self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def check_bounds(self, screen_width=1280, screen_height=720):
        if (
            self.position.x < 0 or self.position.x > screen_width or
            self.position.y < 0 or self.position.y > screen_height
        ):
            self.kill()