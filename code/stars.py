import pygame
from pygame.sprite import Sprite


class BigStar(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.surface
        self.image = pygame.transform.scale(pygame.image.load("graphics/Big_Star.png"), (30, 16))
        self.rect = self.image.get_rect()


class Star(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.surface
        self.image = pygame.transform.scale(pygame.image.load("graphics/Star.png"), (30, 16))
        self.rect = self.image.get_rect()
