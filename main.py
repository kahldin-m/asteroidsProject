import pygame # type: ignore
from player import Player
from asteroid import Asteroid
from shot import Shot
from asteroidfield import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    # Initialization code
    # ---------------------------------------
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    asteroids = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (
        asteroids,
        updateable,
        drawable
    )
    Player.containers = (
        updateable, 
        drawable
    )
    Shot.containers = (
        updateable,
        drawable,
        shots
    )
    AsteroidField.containers = (
        updateable
        )
    player = Player(x, y)
    asteroid_field = AsteroidField()

    # Game Loop
    # -------------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Closing... Goodbye!")
                return
            
        screen.fill("black")
        updateable.update(dt)

        # Collision checks
        for asteroid in asteroids:
            if asteroid.detect_collision(player):
                print("Game over!")
                pygame.QUIT
                return
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.detect_collision(shot):
                    print("Kaboom!")
                    shot.kill()
                    asteroid.split()

        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = game_clock.tick(60) / 1000

if __name__ == "__main__":
    main()
