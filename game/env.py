import pygame

birds_images_values = [
    pygame.transform.scale2x(pygame.image.load("/Users/willian/Documents/FlappyIA/game/images/bird1.png")),
    pygame.transform.scale2x(pygame.image.load("/Users/willian/Documents/FlappyIA/game/images/bird2.png")),
    pygame.transform.scale2x(pygame.image.load("/Users/willian/Documents/FlappyIA/game/images/bird3.png"))]

base_image_value = pygame.transform.scale2x(pygame.image.load("/Users/willian/Documents/FlappyIA/game/images/base.png"))
pipe_image_value = pygame.transform.scale2x(pygame.image.load("/Users/willian/Documents/FlappyIA/game/images/pipe.png"))

background_image_value = pygame.transform.scale2x(
    pygame.image.load("/Users/willian/Documents/FlappyIA/game/images/bg.png"))


def window_config():
    return pygame.display.set_mode((550, 800))


def birds_images():
    return birds_images_values


def base_image():
    return base_image_value


def pipe_image():
    return pipe_image_value


def background_image():
    return background_image_value


def font_score():
    pygame.font.init()
    return pygame.font.SysFont("comicsans", 50)
