import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    def __init__(self, game, alien):
        super().__init__()
        self.screen = game.screen
        self.laser_speed = alien.laser_speed
        self.damage = alien.laser_power
        self.laser_size = alien.laser_size

        self.current_sprite = 0
        self.animation = alien.laser_type

        self.image = pygame.transform.scale(self.animation[self.current_sprite], self.laser_size)
        self.rect = self.image.get_rect(center=alien.rect.center)

        self.y = float(self.rect.y)

    def update(self):
        self.current_sprite += 0.1

        if self.current_sprite >= len(self.animation):
            self.current_sprite = 0

        self.image = pygame.transform.scale(self.animation[int(self.current_sprite)], self.laser_size)

        self.y += self.laser_speed
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)


class BombLaser(Sprite):
    def __init__(self, game, alien):
        super().__init__()
        self.screen = game.screen
        self.laser_speed = alien.laser_speed
        self.damage = alien.laser_power
        self.destroy = False

        self.current_sprite = 0
        self.animation = alien.laser_type
        self.laser_size = alien.laser_size
        self.image = pygame.transform.scale(self.animation[self.current_sprite], self.laser_size)
        self.rect = self.image.get_rect(center=alien.rect.center)

        self.destroy_sprites = [pygame.image.load("graphics/Lasers/Bomb/destroy_1.png"),
                                pygame.image.load("graphics/Lasers/Bomb/destroy_2.png")]

        self.y = float(self.rect.y)

    def destroy_animation(self):
        self.destroy = True

    def update(self):
        if self.destroy:
            self.current_sprite += 0.025

            if self.current_sprite >= len(self.destroy_sprites):
                self.kill()
            else:
                self.image = pygame.transform.scale(self.destroy_sprites[int(self.current_sprite)], (120, 64))
        else:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.animation):
                self.current_sprite = 0

            self.image = pygame.transform.scale(self.animation[int(self.current_sprite)], self.laser_size)

            self.y += self.laser_speed
            self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)
