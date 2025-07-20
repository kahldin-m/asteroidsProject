import pygame # type: ignore
from shot import Shot
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_ui import (
    draw_score, draw_main_menu, draw_game_over, draw_pause_menu, 
    load_highscore, save_highscore
)

def close_game(score, highscore):
    save_highscore(score, highscore)
    print("Closing... Goodbye!")
    return False

def initialize_game(center_x, center_y):
    # Create groups
    asteroids = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set containers
    Asteroid.containers = (asteroids, updateable, drawable)
    Player.containers = (updateable, drawable)
    Shot.containers = (updateable, drawable, shots)
    # AsteroidField.containers = (updateable,)
    
    player = Player(center_x, center_y)
    field = AsteroidField(asteroids)
    updateable.add(field)

    # Reset score for game restarts
    return {
        "player":       player, 
        "field":        field,
        "asteroids":    asteroids, 
        "updateable":   updateable,
        "drawable":     drawable,
        "shots":        shots,
        "score":        0
        }

def handle_menu(window, cx, cy):  # center_x(y)
    window.fill("white")
    draw_main_menu(window, cx, cy)
    pygame.display.flip()


def handle_playing(window, dt, state):
    window.fill("white")
    state["updateable"].update(dt)

    # Collision check: player dies
    for ast in state["asteroids"]:
        if ast.detect_collision(state["player"]):
            print("Game over!")
            return "game_over"

    # Collision check: shot hits bubble
    for ast in state["asteroids"]:
        for shot in state["shots"]:
            if ast.detect_collision(shot):
                # kills_bubble += 1
                state["score"] += 10
                print("Kaboom!")
                shot.kill()
                ast.split()

    # Draw all spires and score
    for sprite in state["drawable"]:
        sprite.draw(window)
    draw_score(window, state["score"])
    pygame.display.flip()

    return "playing"
    

def handle_paused(window, cx, cy, state):
    window.fill((150, 150, 150))
    draw_pause_menu(window, cx, cy)
    draw_score(window, state["score"])
    for sprite in state["drawable"]:
        sprite.draw(window)
    pygame.display.flip()

def handle_game_over(window, cx, cy, score, hiscore):
    window.fill("white")
    draw_game_over(window, cx, cy, score, hiscore)
    pygame.display.flip()


def main():
    # Setup local variables
    # ---------------------------------------
    # print("Starting Asteroids!")
    # print(f"Screen width: {SCREEN_WIDTH}")
    # print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock()
    center_x, center_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    hiscore = load_highscore()
    dt = 0
    kills_bubble = 0

    game_state = "menu"
    game_data = None     # Holds dict from intitialize_game()
    

    # Run main Game Loop
    # -------------------------------------------
    running = True
    while running:
        dt = game_clock.tick(60) / 1000  # Delta Time

        # 1) Always handle Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = close_game(
                    game_data["score"] if game_data else 0,
                    hiscore
                )

            # 2) Handle Keypresses by state
            if event.type == pygame.KEYDOWN:

                # Quit from menu, paused or game_over
                if game_state in ("menu", "paused", "game_over") and event.key == pygame.K_q:
                    running = close_game(
                        game_data["score"] if game_data else 0,
                        hiscore
                    )
                    break
                if game_state == "paused" and event.key == pygame.K_l:
                    running = close_game(
                        game_data["score"] if game_data else 0,
                        hiscore
                    )
                    break

                # Start from menu or restart from game_over
                if game_state == "menu" and event.key == pygame.K_SPACE:
                    game_data = initialize_game(center_x, center_y)
                    game_state = "playing"
                    break

                # Pause/Unpause from playing
                if game_state == "playing" and event.key == pygame.K_ESCAPE:
                    game_state = "paused"
                    break
                if event.key == pygame.K_SPACE and game_state == "paused":
                    game_state = "playing"
                    break

                # Restart from game_over
                if game_state == "game_over" and event.key == pygame.K_r:
                    game_data = initialize_game(center_x, center_y)
                    game_state = "playing"
                    break

                
        # if running flipped to False or we hit a break, skip drawing/updating
        if not running or event.type == pygame.QUIT:
            continue

        # 3) State-based logic and rendering
        if game_state == "menu":
            handle_menu(game_window, center_x, center_y)

        elif game_state == "playing":
            game_state = handle_playing(game_window, dt, game_data)

        elif game_state == "paused":
            handle_paused(game_window, center_x, center_y, game_data)

        elif game_state == "game_over":
            handle_game_over(
                game_window, center_x, center_y, 
                game_data["score"], hiscore
            )            

            
    print("Cleaning up!")
    pygame.quit()

if __name__ == "__main__":
    main()
