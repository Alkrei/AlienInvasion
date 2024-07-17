import pygame
import sys
import pygame_gui
import json
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
from random import randint
from time import sleep
from game import AlienInvasion
from settings import Settings
from fonts import f2, f4
from stars import Big_Star, Star
from records import Records

pygame.init()


class MainMenu:
    def __init__(self):
        self.Start_button = None
        self.Records_button = None
        self.Quite_button = None
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_icon(pygame.image.load("graphics/Aliens/Alien/Design_1/Move/move_1.png"))
        pygame.display.set_caption("AlienInvasion")
        self.manager = pygame_gui.UIManager((self.screen.get_size()), 'managers/main_menu.json')
        self.settings = Settings()
        self.settings.width = self.screen.get_rect().width
        self.settings.height = self.screen.get_rect().height
        self.clock = pygame.time.Clock()
        self.press = False
        self.blinking = True

        self.stars = pygame.sprite.Group()
        self._create_sky()

        self.button_inactive = pygame.image.load("graphics/button_inactive.png")
        self.button_active = pygame.image.load("graphics/button_active.png")
        self.title = pygame.image.load("graphics/Main_Menu.png")

        with open('saves/difficulty_level.json', 'r') as d_l:
            self.difficulty_level = json.load(d_l)

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

    def draw(self):
        time_delta = self.clock.tick(self.settings.FPS)
        self.screen.fill(self.settings.BLACK)

        self.stars.draw(self.screen)
        self.screen.blit(self.title, self.title.get_rect())
        if self.press:
            self.manager.draw_ui(self.screen)
            self.screen.blit(f2.render(f"Difficulty Level: {self.difficulty_level}", False,
                                       self.settings.WHITE), (800, 950))
            self.screen.blit(f4.render(f"{self.settings.by}", False, self.settings.WHITE),
                             (self.screen.get_rect().width-len(self.settings.by)*16, self.screen.get_rect().bottom-45))
        else:
            if self.blinking:
                self.screen.blit(f2.render("PRESS START", False, (255, 255, 255)), (850, 850))
                self.blinking = False
            elif not self.blinking:
                self.blinking = True
            sleep(0.5)

        self.manager.update(time_delta)
        pygame.display.update()

    def start(self):
        intro = True

        pygame.mixer.music.load("sound/music.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.press:
                            self.press = True
                            self.Start_button = UIButton(relative_rect=pygame.Rect(((self.settings.width // 2 - 128),
                                                                                    850), (256, 64)),
                                                         text="Start",
                                                         manager=self.manager,
                                                         object_id=ObjectID(class_id="button"))
                            self.Records_button = UIButton(relative_rect=pygame.Rect(((self.settings.width // 2 + 384),
                                                                                      850), (256, 64)),
                                                           text="Score",
                                                           manager=self.manager,
                                                           object_id=ObjectID(class_id="button"))
                            self.Quite_button = UIButton(relative_rect=pygame.Rect(((self.settings.width // 2 - 640),
                                                                                    850), (256, 64)),
                                                         text="Quite",
                                                         manager=self.manager,
                                                         object_id=ObjectID(class_id="button"))
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.Start_button:
                        pygame.mixer.music.stop()
                        game = AlienInvasion(self.screen, self.clock)
                        game.run_game()
                        with open('saves/difficulty_level.json', 'r') as d_l:
                            self.difficulty_level = json.load(d_l)
                        pygame.mixer.music.play(-1)
                    if event.ui_element == self.Records_button:
                        records = Records(self.screen, self.settings, self.clock)
                        records.run()
                    if event.ui_element == self.Quite_button:
                        pygame.quit()
                        sys.exit()

                self.manager.process_events(event)
            self.draw()


main_menu = MainMenu()
main_menu.start()
