import pygame # type: ignore

pygame.font.init()
score_font = pygame.font.SysFont("Arial", 24)

def draw_score(surface, score):
    text_surface = score_font.render(f"Score: {score}", True, (0, 0, 0))
    surface.blit(text_surface, (10,10))


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