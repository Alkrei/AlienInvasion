import pygame
import sys
import json
from buttons import Button
from random import randint
from time import sleep
from game import AlienInvasion
from settings import Settings
from fonts import f2, f4
from stars import BigStar, Star
from records import Records

pygame.init()

class MainMenu:
    def __init__(self):
        self.settings = Settings()
        self.surface = pygame.surface.Surface((self.settings.width, self.settings.height))
        self.screen = pygame.display.set_mode((960, 540), pygame.RESIZABLE)
        self.title = pygame.image.load("graphics/Main_Menu.png")
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load("graphics/Aliens/Alien/Design_1/Move/move_1.png"))
        pygame.display.set_caption("AlienInvasion")

        self.press = False
        self.blinking = True

        # space
        self.stars = pygame.sprite.Group()
        self._create_sky()

        # buttons
        self.start_button = Button(self.settings.width // 2 - 128, 850, 256, 64,
                                   self.settings.button_inactive, self.settings.button_active, self.settings, f2, 'Start',
                                   lambda: self.play())
        self.record_button = Button(self.settings.width // 2 + 384, 850, 256, 64,
                                    self.settings.button_inactive, self.settings.button_active, self.settings, f2, 'Score',
                                    lambda: self.record())
        self.quite_button = Button(self.settings.width // 2 - 640, 850, 256, 64,
                                   self.settings.button_inactive, self.settings.button_active, self.settings, f2, 'Quite',
                                   lambda: self.quite())

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
            star = BigStar(self)
        else:
            star = Star(self)
        star_width, star_height = star.rect.size
        coef = randint(-50, 50)
        star.rect.x = star_width + 3 * star_width * column_num + coef
        star.rect.y = star_height + 3 * star_height * row_num + coef
        self.stars.add(star)

    def play(self):
        pygame.mixer.music.stop()
        game = AlienInvasion(self.surface, self.screen, self.settings, self.clock)
        game.run_game()
        with open('saves/difficulty_level.json', 'r') as d_l:
            self.difficulty_level = json.load(d_l)
        pygame.mixer.music.play(-1)

    def record(self):
        records = Records(self.surface, self.screen, self.settings, self.clock)
        records.run()

    def quite(self):
        pygame.quit()
        sys.exit()

    def draw_buttons(self):
        self.start_button.button(self.surface, self.screen)
        self.record_button.button(self.surface, self.screen)
        self.quite_button.button(self.surface, self.screen)

    def draw(self):
        self.surface.fill(self.settings.BLACK)

        self.stars.draw(self.surface)
        self.surface.blit(self.title, self.title.get_rect())
        if self.press:
            self.draw_buttons()
            self.surface.blit(f2.render(f"Difficulty Level: {self.difficulty_level}", False,
                                        self.settings.WHITE), (800, 950))
            self.surface.blit(f4.render(f"{self.settings.by}", False, self.settings.WHITE),
                              (self.settings.width - len(self.settings.by) * 16, self.settings.height - 45))
        else:
            if self.blinking:
                self.surface.blit(f2.render("PRESS START", False, (255, 255, 255)), (850, 850))
                self.blinking = False
            elif not self.blinking:
                self.blinking = True
            sleep(0.5)
        self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
        pygame.display.update()

    def start(self):
        intro = True

        pygame.mixer.music.load("sound/music.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quite()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.press = True
            self.draw()

main_menu = MainMenu()
main_menu.start()
