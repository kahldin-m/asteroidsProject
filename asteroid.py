import math, pygame # type: ignore
import random
import circleshape
from constants import (
    ASTEROID_BASE_COLOR, ASTEROID_HIGHLIGHT_COLOR, ASTEROID_FLASH_FREQUENCY,
    ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
)

class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.flash_timer = 0.0

    def draw(self, screen):
        # 1) Compute blend factor (0…1)
        phase = (math.sin(2 * math.pi * ASTEROID_FLASH_FREQUENCY * self.flash_timer) + 1) / 2
        # 2) Create Color objects and lerp
        base      = pygame.Color(*ASTEROID_BASE_COLOR)
        highlight = pygame.Color(*ASTEROID_HIGHLIGHT_COLOR)
        color     = base.lerp(highlight, phase)
        # 3) Draw onto a small SRCALPHA surface
        size = int(self.radius * 2 + 4)
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(surf, color, center, self.radius, 2)
        # 4) Blit centered on the asteroid’s position
        top_left = (self.position.x - center[0], self.position.y - center[1])
        screen.blit(surf, top_left)

    def update(self, dt):
        self.flash_timer += dt
        self.position += (self.velocity * dt)
        self.check_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20.0, 50.0)
        angle1 = self.velocity.rotate(random_angle)
        angle2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        baby_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        baby_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        baby_asteroid1.velocity = angle1 * 1.2
        baby_asteroid2.velocity = angle2 * 1.2
