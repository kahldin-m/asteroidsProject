import pygame # type: ignore
from player import Player
from game_ui import draw_score, load_highscore, save_highscore
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

    game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    dt = 0
    player_score = 0
    kills_bubble = 0
    current_highscore = load_highscore()
    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2


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
    
    player = Player(center_x, center_y)
    asteroid_field = AsteroidField()

    # Game Loop
    # -------------------------------------------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore(player_score, current_highscore)
                print("Closing... Goodbye!")
                running = False
            
        game_window.fill("white")
        
        updateable.update(dt)
        for shot in shots:
            shot.check_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Collision checks
        for asteroid in asteroids:
            if asteroid.detect_collision(player):
                save_highscore(player_score, current_highscore)
                print("Game over!")
                pygame.QUIT
                running = False

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.detect_collision(shot):
                    kills_bubble += 1
                    player_score += 10
                    print("Kaboom!")
                    shot.kill()
                    asteroid.split()

        for sprite in drawable:
            sprite.draw(game_window)

        draw_score(game_window, player_score)
        pygame.display.flip()
        dt = game_clock.tick(60) / 1000

if __name__ == "__main__":
    main()
