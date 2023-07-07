import pygame


class Gun(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.timer = None
        self.screen = game.screen
        self.settings = game.settings
        self.booster = self.settings.gun_booster
        self.image = pygame.transform.scale(pygame.image.load(f"graphics/Gun_{self.booster}/Gun_{self.booster}.png"), (60, 32))
        self.destroy_sprites = [pygame.image.load(f"graphics/Gun_{self.booster}/Destroy/destroy_1.png"),
                                pygame.image.load(f"graphics/Gun_{self.booster}/Destroy/destroy_2.png")]
        self.damage_sprites = [pygame.image.load(f"graphics/Gun_{self.booster}/Damage/damage_1.png"),
                               pygame.image.load(f"graphics/Gun_{self.booster}/Damage/damage_2.png")]
        self.rect = self.image.get_rect(midbottom=self.screen.get_rect().midbottom)
        self.root_x = self.rect.x
        self.rect.y -= 64
        self.current_sprite = 0
        self.mright = False
        self.mleft = False
        self.destroy = False
        self.get_damage = False
        self.x = float(self.rect.x)

    def damage_animation(self):
        self.get_damage = True
        self.current_sprite = 0
        self.timer = 100

    def destroy_animation(self):
        self.destroy = True
        self.current_sprite = 0

    def update(self):
        if self.mright and self.rect.right < self.screen.get_rect().right:
            self.x += self.settings.gun_speed
        if self.mleft and self.rect.left > 0:
            self.x -= self.settings.gun_speed
        self.rect.x = self.x

    def blit(self):
        if self.destroy:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.destroy_sprites):
                self.current_sprite = 0
            else:
                self.image = pygame.transform.scale(self.destroy_sprites[int(self.current_sprite)], (60, 32))
        elif self.get_damage:
            self.timer -= 1
            if self.timer == 0:
                self.get_damage = False
                self.image = pygame.transform.scale(pygame.image.load(f"graphics/Gun_{self.booster}/Gun_{self.booster}.png"), (60, 32))
            else:
                self.current_sprite += 0.1

                if self.current_sprite >= len(self.destroy_sprites):
                    self.current_sprite = 0
                else:
                    self.image = pygame.transform.scale(self.damage_sprites[int(self.current_sprite)], (60, 32))

        self.screen.blit(self.image, self.rect)

    def center_gun(self):
        self.rect.x = self.root_x
        self.x = float(self.rect.x)
