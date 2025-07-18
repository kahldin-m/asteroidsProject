import pygame # type: ignore
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    updateables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    Player.containers = (
        updateables, 
        drawables
    )
    player = Player(x, y)

    # Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Closing... Goodbye!")
                return
            
        screen.fill("black")
        updateables.update(dt)
        for drawable in drawables:
            drawable.draw(screen)
        pygame.display.flip()
        dt = game_clock.tick(60) / 1000

if __name__ == "__main__":
    main()
