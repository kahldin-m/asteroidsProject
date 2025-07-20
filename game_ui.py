import pygame # type: ignore

pygame.font.init()
score_font = pygame.font.SysFont("Arial", 24)

def draw_score(surface, score):
    surface.blit(score_font.render(f"Score: {score}", True, (0, 0, 0)), (10,10))

def draw_main_menu(surface, x, y):
    font = pygame.font.SysFont("Arial", 48)
    text1 = font.render("Bubblegun", True, (0, 5, 250))
    text2 = score_font.render("How To Play: ", True, (0, 25, 200))
    text3 = score_font.render("Get power-ups and use them with R", True, (0, 0, 0))
    text4 = score_font.render("Spacebar to Play or Q to Quit", True, (0, 0, 0))
    text5 = score_font.render("Shoot bubbles with SPACEBAR", True, (0, 0, 0))

    surface.blit(text1, (x - text1.get_width()//2, y - 200))
    surface.blit(text2, (x - text2.get_width()//2 - text5.get_width()//2, y - 100))
    surface.blit(text3, (x - text3.get_width()//2, y - 50))
    surface.blit(text4, (x - text4.get_width()//2, y))
    surface.blit(text5, (x - text5.get_width()//2 + text2.get_width()//2, y - 100))


def draw_pause_menu(surface, x, y):
    font = pygame.font.SysFont("Arial", 40)
    text1 = font.render("PAUSED", True, (0, 50, 150))
    text2 = score_font.render("Spacebar to Continue", True, (0, 0, 0))
    
    surface.blit(text1, (x - text1.get_width()//2, y - 100))
    surface.blit(text2, (x - text2.get_width()//2, y))


def draw_game_over(surface, x, y, score, highscore):
    font = pygame.font.SysFont("Arial", 48)
    text1 = font.render("GAME OVER", True, (255, 0, 0))
    text2 = score_font.render(f"Score: {score} | Highscore: {highscore}", True, (0, 0, 0))
    text3 = score_font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))

    surface.blit(text1, (x - text1.get_width()//2, y - 100))
    surface.blit(text2, (x - text2.get_width()//2, y))
    surface.blit(text3, (x - text3.get_width()//2, y + 35))


def load_highscore(filename="highscore.txt"):
    try:
        with open(filename, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0  # Default if highscore file is missing or corrupt
    

def save_highscore(score, hiscore, filename="highscore.txt"):
    if score > hiscore:
        print("!---!---New Highscore---!---!")
        with open(filename, "w") as file:
            file.write(str(score) + "\n")