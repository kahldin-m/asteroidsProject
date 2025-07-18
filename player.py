from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN
from shot import Shot
import circleshape
import pygame # type: ignore

class Player(circleshape.CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0
        self.shot_timer = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate_player(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        self.rotation = self.rotation % 360

    def move_player(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_timer < 0:
            self.shot_timer = PLAYER_SHOOT_COOLDOWN
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot.velocity = forward * PLAYER_SHOT_SPEED
    
    def update(self, dt):
        self.shot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate_player(-dt)
            # print(self.rotation)
        if keys[pygame.K_d]:
            self.rotate_player(dt)
            # print(self.rotation)
        if keys[pygame.K_w]:
            self.move_player(dt)
            # print(self.position)
        if keys[pygame.K_s]:
            self.move_player(-dt)
            # print(self.position)
        if keys[pygame.K_SPACE]:
            self.shoot()
