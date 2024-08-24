import pygame
import json
from random import randint
from buttons import Button
from stars import BigStar, Star
from fonts import f2, f3


class Records:
    def __init__(self, surface, screen, settings, clock):
        self.surface = surface
        self.screen = screen
        self.settings = settings
        self.clock = clock
        self.quite = False

        with open("saves/score.json", "r") as score:
            self.score = json.load(score)
        with open("saves/record.json", "r") as record_score:
            self.record_score = json.load(record_score)

        self.stars = pygame.sprite.Group()
        self._create_sky()

        # buttons
        self.main_menu_button = Button((self.screen.get_rect().centerx - 654), 800, 256, 64,
                                       self.settings.button_inactive, self.settings.button_active, self.settings, f2, 'Main Menu',
                                       lambda: self.quite_func())

    def _create_sky(self):
        star = Star(self)
        star_width, star_height = star.rect.size

        available_space_x = self.settings.width
        number_columns = available_space_x // (3 * star_width)

        available_space_y = self.settings.height
        number_rows = available_space_y // (3 * star_height)
        for row_num in range(number_rows):
            for column_num in range(number_columns):
                self._create_star(column_num, row_num)

    def _create_star(self, column_num, row_num):
        x = randint(0, 100)
        if x > 80:
            star = BigStar(self)
        else:
            star = Star(self)
        star_width, star_height = star.rect.size
        coef = randint(-50, 50)
        star.rect.x = star_width + 3 * star_width * column_num + coef
        star.rect.y = star_height + 3 * star_height * row_num + coef
        self.stars.add(star)

    def quite_func(self):
        self.quite = True

    def draw(self):
        self.surface.fill(self.settings.bc_color)
        self.stars.draw(self.surface)

        self.surface.blit(f2.render(f"Record: {self.record_score}", False, self.settings.YELLOW),
                         (self.surface.get_rect().centerx - 590, 400))
        self.surface.blit(f2.render(f"Score: {self.score}", False, self.settings.WHITE),
                         (self.surface.get_rect().centerx - 590, 600))
        self.surface.blit(f3.render("Records", False, self.settings.WHITE),
                         (self.surface.get_rect().centerx - (len("Records") * 25), 200))
        self.main_menu_button.button(self.surface, self.screen)
        self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
        pygame.display.update()

    def run(self):
        while not self.quite:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quite_func()
            self.draw()
