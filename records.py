import pygame
import json
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
from random import randint
from stars import Big_Star, Star
from fonts import f2, f3


class Records:
    def __init__(self, screen, settings, clock):
        self.text = "Records"
        self.screen = screen
        self.settings = settings
        self.clock = clock
        with open("saves/score.json", "r") as score:
            self.score = json.load(score)
        with open("saves/record.json", "r") as record_score:
            self.record_score = json.load(record_score)

        self.stars = pygame.sprite.Group()
        self._create_sky()
        self.record_active = True

        self.manager = pygame_gui.UIManager((self.screen.get_size()), 'managers/score.json')
        self.Main_menu_button = UIButton(relative_rect=pygame.Rect(
                                         (self.screen.get_rect().centerx - 654, 800), (256, 64)),
                                         text="Main Menu",
                                         manager=self.manager,
                                         object_id=ObjectID(class_id="button"))

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
            star = Big_Star(self)
        else:
            star = Star(self)
        star_width, star_height = star.rect.size
        coef = randint(-50, 50)
        star.rect.x = star_width + 3 * star_width * column_num + coef
        star.rect.y = star_height + 3 * star_height * row_num + coef
        self.stars.add(star)

    def run(self):
        while self.record_active:
            time_delta = self.clock.tick(self.settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.Main_menu_button:
                        self.record_active = False

                self.manager.process_events(event)

            self.screen.fill(self.settings.bc_color)
            self.stars.draw(self.screen)

            self.screen.blit(f2.render(f"Record: {self.record_score}", False, self.settings.YELLOW),
                             (self.screen.get_rect().centerx - 590, 400))
            self.screen.blit(f2.render(f"Score: {self.score}", False, self.settings.WHITE),
                             (self.screen.get_rect().centerx - 590, 600))
            self.screen.blit(f3.render(self.text, False, self.settings.WHITE),
                             (self.screen.get_rect().centerx - (len(self.text) * 25), 200))
            self.manager.draw_ui(self.screen)

            self.manager.update(time_delta)
            pygame.display.update()
