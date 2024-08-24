import random
import pygame
from pygame.sprite import Sprite
from lasers import BombLaser


class Alien(Sprite):
    def __init__(self, game, alien_design, hp=1):
        super().__init__()
        self.screen = game.surface
        self.settings = game.settings
        self.laser_speed = 5
        self.laser_power = 1
        self.hp = hp
        self.score = 10
        self.laser_size = (9, 24)

        # animations
        self.move_sprites = [pygame.image.load(f"graphics/Aliens/Alien/Design_{alien_design}/Move/move_1.png"),
                             pygame.image.load(f"graphics/Aliens/Alien/Design_{alien_design}/Move/move_2.png")]
        self.destroy_sprites = [pygame.image.load(f"graphics/Aliens/Alien/Design_{alien_design}/Destroy/destroy_1.png"),
                                pygame.image.load(f"graphics/Aliens/Alien/Design_{alien_design}/Destroy/destroy_2.png")]
        self.shouted_sprites = [pygame.image.load(f"graphics/Aliens/Alien/Design_{alien_design}/Shouted/shouted_1.png"),
                                pygame.image.load(f"graphics/Aliens/Alien/Design_{alien_design}/Shouted/shouted_2.png")]
        self.laser_type = [pygame.image.load("graphics/Lasers/AlienLaser/laser_1.png"),
                           pygame.image.load("graphics/Lasers/AlienLaser/laser_2.png"),
                           pygame.image.load("graphics/Lasers/AlienLaser/laser_3.png"),
                           pygame.image.load("graphics/Lasers/AlienLaser/laser_4.png")]

        self.current_sprite = 0
        self.image = pygame.transform.scale(self.move_sprites[self.current_sprite], (60, 32))

        # self.image = pygame.transform.scale(pygame.image.load("graphics/Alien.png"),(60,32))
        self.rect = self.image.get_rect()
        self.destroy = False
        self.shouted = False

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.root_pos_x = 0
        self.root_pos_y = 0

        self.x = float(self.rect.x)

    def destroy_animation(self):
        self.destroy = True
        self.current_sprite = 0

    def shouted_animation(self):
        self.shouted = True
        self.current_sprite = 0

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def animation(self):
        if self.destroy:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.destroy_sprites):
                self.kill()
            else:
                self.image = pygame.transform.scale(self.destroy_sprites[int(self.current_sprite)], (60, 32))
        elif self.shouted:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.destroy_sprites):
                self.shouted = False
            else:
                self.image = pygame.transform.scale(self.shouted_sprites[int(self.current_sprite)], (60, 32))
        else:
            self.current_sprite += 0.02

            if self.current_sprite >= len(self.move_sprites):
                self.current_sprite = 0
            self.image = pygame.transform.scale(self.move_sprites[int(self.current_sprite)], (60, 32))

    def update(self):
        self.animation()

        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x


class AlienOfficer(Alien):
    def __init__(self, game, alien_design, hp=1):
        super().__init__(game, alien_design, hp)
        self.laser_speed = 7.5
        self.laser_power = 2
        self.score = 20
        self.laser_size = (12, 27)
        self.move_sprites = [pygame.image.load(f"graphics/Aliens/Officer/Design_{alien_design}/Move/move_1.png"),
                             pygame.image.load(f"graphics/Aliens/Officer/Design_{alien_design}/Move/move_2.png")]
        self.destroy_sprites = [
            pygame.image.load(f"graphics/Aliens/Officer/Design_{alien_design}/Destroy/destroy_1.png"),
            pygame.image.load(f"graphics/Aliens/Officer/Design_{alien_design}/Destroy/destroy_2.png")]
        self.shouted_sprites = [pygame.image.load(f"graphics/Aliens/Officer/Design_{alien_design}/Shouted/shouted_1.png"),
                                pygame.image.load(f"graphics/Aliens/Officer/Design_{alien_design}/Shouted/shouted_2.png")]
        self.laser_type = [pygame.image.load("graphics/Lasers/OfficerLaser/laser_1.png"),
                           pygame.image.load("graphics/Lasers/OfficerLaser/laser_2.png"),
                           pygame.image.load("graphics/Lasers/OfficerLaser/laser_3.png"),
                           pygame.image.load("graphics/Lasers/OfficerLaser/laser_4.png")]
        self.image = pygame.transform.scale(self.move_sprites[self.current_sprite], (60, 32))


class AlienSniper(Alien):
    def __init__(self, game, alien_design, hp=1):
        super().__init__(game, alien_design, hp)
        self.laser_speed = 10
        self.laser_power = 1
        self.score = 20
        self.laser_size = (12, 27)
        self.move_sprites = [pygame.image.load(f"graphics/Aliens/Sniper/Design_{alien_design}/Move/move_1.png"),
                             pygame.image.load(f"graphics/Aliens/Sniper/Design_{alien_design}/Move/move_2.png")]
        self.destroy_sprites = [
            pygame.image.load(f"graphics/Aliens/Sniper/Design_{alien_design}/Destroy/destroy_1.png"),
            pygame.image.load(f"graphics/Aliens/Sniper/Design_{alien_design}/Destroy/destroy_2.png")]
        self.shouted_sprites = [pygame.image.load(f"graphics/Aliens/Sniper/Design_{alien_design}/Shouted/shouted_1.png"),
                                pygame.image.load(f"graphics/Aliens/Sniper/Design_{alien_design}/Shouted/shouted_2.png")]
        self.laser_type = [pygame.image.load("graphics/Lasers/SniperLaser/laser_1.png"),
                           pygame.image.load("graphics/Lasers/SniperLaser/laser_2.png"),
                           pygame.image.load("graphics/Lasers/SniperLaser/laser_3.png"),
                           pygame.image.load("graphics/Lasers/SniperLaser/laser_4.png")]
        self.image = pygame.transform.scale(self.move_sprites[self.current_sprite], (60, 32))


class AlienElite(Alien):
    def __init__(self, game, hp=1):
        super().__init__(game, hp)
        self.laser_speed = 7.5
        self.laser_power = 3
        self.score = 30
        self.laser_size = (15, 30)
        self.move_sprites = [pygame.image.load("graphics/Aliens/Elite/Move/move_1.png"),
                             pygame.image.load("graphics/Aliens/Elite/Move/move_2.png")]
        self.destroy_sprites = [pygame.image.load("graphics/Aliens/Elite/Destroy/destroy_1.png"),
                                pygame.image.load("graphics/Aliens/Elite/Destroy/destroy_2.png")]
        self.laser_type = [pygame.image.load("graphics/Lasers/EliteLaser/laser_1.png"),
                           pygame.image.load("graphics/Lasers/EliteLaser/laser_2.png")]
        self.image = pygame.transform.scale(self.move_sprites[self.current_sprite], (60, 32))


class ExtraAlienElite(Alien):
    def __init__(self, game, hp=1):
        super().__init__(game, hp)
        self.laser_speed = 10
        self.laser_power = 3
        self.hp = 2
        self.score = 50
        self.laser_size = (15, 30)
        self.move_sprites = [pygame.image.load("graphics/Aliens/ExtraElite/Move/move_1.png"),
                             pygame.image.load("graphics/Aliens/ExtraElite/Move/move_2.png")]
        self.destroy_sprites = [pygame.image.load("graphics/Aliens/ExtraElite/Destroy/destroy_1.png"),
                                pygame.image.load("graphics/Aliens/ExtraElite/Destroy/destroy_2.png")]
        self.laser_type = [pygame.image.load("graphics/Lasers/ExtraEliteLaser/laser_1.png"),
                           pygame.image.load("graphics/Lasers/ExtraEliteLaser/laser_2.png")]
        self.shouted_sprites = [pygame.image.load("graphics/Aliens/ExtraElite/Shouted/shouted_1.png"),
                                pygame.image.load("graphics/Aliens/ExtraElite/Shouted/shouted_2.png")]
        self.image = pygame.transform.scale(self.move_sprites[self.current_sprite], (60, 32))


class ExtraAlien(Alien):
    def __init__(self, game, hp=1):
        super().__init__(game, hp)
        self.laser_speed = 7.5
        self.laser_power = 3
        self.hp = 2
        self.score = 40
        self.laser_size = (15, 30)
        self.move_sprites = [pygame.image.load("graphics/Aliens/ExtraAlien/Move/move_1.png"),
                             pygame.image.load("graphics/Aliens/ExtraAlien/Move/move_2.png")]
        self.destroy_sprites = [pygame.image.load("graphics/Aliens/ExtraAlien/Destroy/destroy_1.png"),
                                pygame.image.load("graphics/Aliens/ExtraAlien/Destroy/destroy_2.png")]
        self.laser_type = [pygame.image.load("graphics/Lasers/ExtraLaser/laser_1.png"),
                           pygame.image.load("graphics/Lasers/ExtraLaser/laser_2.png")]
        self.shouted_sprites = [pygame.image.load("graphics/Aliens/ExtraAlien/Shouted/shouted_1.png"),
                                pygame.image.load("graphics/Aliens/ExtraAlien/Shouted/shouted_2.png")]
        self.image = pygame.transform.scale(self.move_sprites[self.current_sprite], (60, 32))


class AlienJuggernaut(Alien):
    def __init__(self, game, hp=1):
        super().__init__(game, hp)
        self.laser_speed = 5
        self.laser_power = 2
        self.hp = 2
        self.score = 30
        self.laser_size = (15, 33)
        self.move_sprites = [pygame.image.load("graphics/Aliens/Juggernaut/Move/move_1.png"),
                             pygame.image.load("graphics/Aliens/Juggernaut/Move/move_2.png")]
        self.destroy_sprites = [pygame.image.load("graphics/Aliens/Juggernaut/Destroy/destroy_1.png"),
                                pygame.image.load("graphics/Aliens/Juggernaut/Destroy/destroy_2.png")]
        self.shouted_sprites = [pygame.image.load("graphics/Aliens/Juggernaut/Shouted/shouted_1.png"),
                                pygame.image.load("graphics/Aliens/Juggernaut/Shouted/shouted_2.png")]
        self.laser_type = [pygame.image.load("graphics/Lasers/JuggernautLaser/laser_1.png"),
                           pygame.image.load("graphics/Lasers/JuggernautLaser/laser_2.png")]
        self.image = pygame.transform.scale(self.move_sprites[self.current_sprite], (60, 32))


class Extra(Sprite):
    def __init__(self, game, side):
        super().__init__()
        self.screen = game.surface
        self.settings = game.settings
        self.current_sprite = 0
        self.destroy = False
        self.score = 40

        self.image = pygame.transform.scale(pygame.image.load("graphics/Aliens/Extra/Extra.png"), (64, 32))
        self.destroy_sprites = [pygame.image.load("graphics/Aliens/Extra/Destroy/destroy_1.png"),
                                pygame.image.load("graphics/Aliens/Extra/Destroy/destroy_2.png")]
        y = 50
        if side == 'right':
            x = self.settings.width + 50
            self.speed = self.settings.extra_speed_negative
        else:
            x = -50
            self.speed = self.settings.extra_speed_positive

        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = float(self.rect.x)

    def destroy_animation(self):
        self.destroy = True

    def update(self):
        self.rect.x += self.speed
        if self.destroy:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.destroy_sprites):
                self.kill()
            else:
                self.image = pygame.transform.scale(self.destroy_sprites[int(self.current_sprite)], (96, 32))
        # if self.rect.centerx > 0 and self.rect.centerx < self.settings.width:


class SuperExtra(Sprite):
    def __init__(self, game, side):
        super().__init__()
        self.screen = game.surface
        self.settings = game.settings
        self.current_sprite = 0
        self.destroy = False
        self.score = 60

        self.image = pygame.transform.scale(pygame.image.load("graphics/Aliens/Extra/SuperExtra.png"), (64, 32))
        self.destroy_sprites = [pygame.image.load("graphics/Aliens/Extra/SuperExtraDestroy/destroy_1.png"),
                                pygame.image.load("graphics/Aliens/Extra/SuperExtraDestroy/destroy_2.png")]
        y = 50
        if side == 'right':
            x = self.settings.width + 50
            self.speed = self.settings.extra_speed_negative
        else:
            x = -50
            self.speed = self.settings.extra_speed_positive

        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = float(self.rect.x)

    def destroy_animation(self):
        self.destroy = True

    def update(self):
        self.rect.x += self.speed
        if self.destroy:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.destroy_sprites):
                self.kill()
            else:
                self.image = pygame.transform.scale(self.destroy_sprites[int(self.current_sprite)], (96, 32))


class Bomber(Extra):
    def __init__(self, game, side):
        super().__init__(game, side)
        self.laser_speed = 3
        self.laser_power = 3
        self.score = 40
        self.lasers = game.bombs
        self.laser_size = (24, 24)
        self.laser_timer = random.randint(50, 100)
        self.laser_type = [pygame.image.load("graphics/Lasers/Bomb/bomb_1.png"),
                           pygame.image.load("graphics/Lasers/Bomb/bomb_2.png")]
        self.image = pygame.transform.scale(pygame.image.load("graphics/Aliens/Bomber/Bomber.png"), (60, 32))
        self.destroy_sprites = [pygame.image.load("graphics/Aliens/Bomber/Destroy/destroy_1.png"),
                                pygame.image.load("graphics/Aliens/Bomber/Destroy/destroy_2.png")]
        if side == 'right':
            self.x = self.settings.width + 50
            self.speed = self.settings.bomber_speed_negative
        else:
            self.x = -50
            self.speed = self.settings.bomber_speed_positive

    def laser(self):
        bomb_sprite = BombLaser(self, self)
        self.lasers.add(bomb_sprite)

    def update(self):
        self.rect.x += self.speed
        if self.destroy:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.destroy_sprites):
                self.kill()
            else:
                self.image = pygame.transform.scale(self.destroy_sprites[int(self.current_sprite)], (60, 32))
        self.laser_timer -= 1
        if self.laser_timer == 0:
            self.laser()
            self.laser_timer = random.randint(50, 300)


class MotherShip(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.surface
        self.settings = game.settings
        self.type = game.last_alien_type
        if self.type == "juggernaut":
            self.image = pygame.transform.scale(pygame.image.load("graphics/Aliens/Extra/JuggernautExtra.png"),
                                                (240, 128))
        elif self.type == "extra":
            self.image = pygame.transform.scale(pygame.image.load("graphics/Aliens/Extra/SuperExtra.png"), (240, 128))
        else:
            self.image = pygame.transform.scale(pygame.image.load("graphics/Aliens/Extra/Extra.png"), (240, 128))
        self.rect = self.image.get_rect()

        self.rect.x = self.screen.get_rect().centerx - (self.rect.width // 2)
        self.rect.y = 0 - self.rect.height
        self.root_pos = 0 - self.rect.height

        self.x = float(self.rect.x)
