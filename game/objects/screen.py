import pygame
from game.env import background_image


def window(win):
    clock = pygame.time.Clock()
    clock.tick(65)

    win.blit(background_image(), (0, 0))


def draw_game_over_screen(win):
    font = pygame.font.Font(None, 50)
    text = font.render("GAME OVER", True, (255, 255, 255))
    win.blit(text, (370 - text.get_width(), 400 - text.get_height()))
    pygame.display.flip()


