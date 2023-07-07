import pygame
from PIL import Image
from pygame.sprite import Sprite


class BLock(Sprite):
    def __init__(self, size, color, screen,  x, y):
        super().__init__()
        self.size = size
        self.color = color
        self.screen = screen
        self.x = x
        self.y = y

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Obstacle:
    def __init__(self):
        self.img = Image.open("graphics/Obstacle.png")

    def create_multiple_obstacles(self, *offset, x_pos, y_pos, size, screen, blocks):
        for offset_x in offset:
            self.create_obstacle(x_pos, y_pos, offset_x, size, screen, blocks)

    def create_obstacle(self, x_pos, y_pos, offset_x, size, screen, blocks):
        for row in range(self.img.width):
            for col in range(self.img.height):
                color = self.img.getpixel((row, col))
                if color != (0, 0, 0, 0):
                    x = x_pos + row * size + offset_x
                    y = y_pos + col * size
                    block = BLock(size, color, screen, x, y)
                    blocks.add(block)
