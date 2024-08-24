import pickle
import sys
import pygame
import obstacle
import json
from time import sleep
from random import randint, choice
from game_stats import GameStats
from gun import Gun
from bullet import Bullet
from lasers import Laser
from alien import Alien, AlienElite, AlienOfficer, AlienSniper, AlienJuggernaut, Extra, Bomber, MotherShip, \
    ExtraAlienElite, ExtraAlien, SuperExtra
from stars import BigStar, Star
from fonts import f2, f3
from buttons import Button


class AlienInvasion:
    def __init__(self, surface, screen, settings, clock):
        self.surface = surface
        self.screen = screen
        self.settings = settings
        self.clock = clock

        self.init_data()
        self.gun = pygame.sprite.GroupSingle(Gun(self))
        self.opening = True
        self.game_active = True

        # music setup
        self.bullet_sound = pygame.mixer.Sound('sound/laser.wav')
        self.bullet_sound.set_volume(0.25)
        self.gun_explosion_sound = pygame.mixer.Sound('sound/explosion_gun.wav')
        self.alien_explosion_sound = pygame.mixer.Sound('sound/explosion.wav')
        self.alien_explosion_sound.set_volume(0.25)
        self.extra_explosion_sound = pygame.mixer.Sound('sound/explosion_extra.wav')
        self.powerup = pygame.mixer.Sound('sound/powerup.wav')
        self.explosion_gun_hp = pygame.mixer.Sound('sound/explosion_gun_hp.wav')
        self.explosion_armour = pygame.mixer.Sound('sound/explosion_armour.wav')
        self.explosion_shield = pygame.mixer.Sound('sound/explosion_shield.wav')

        # game_end_setup
        self.game_end_active = False
        self.game_status = ""
        self.text = ""
        self.surf = pygame.image.load("graphics/game_end.png")
        self.main_menu_button = Button(825, 800, 256, 64, self.settings.button_inactive,
                                       self.settings.button_active, self.settings, f2, 'Main Menu', lambda: self.quit_func())

        # Ammo
        self.bullets = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.ALIENLASER = pygame.USEREVENT + 1

        # Alien settings setup
        if self.difficulty_level <= 3:
            self.fleet_rows = randint(4, 6)
            self.last_alien_type = None
            self.extra_event = 0
        elif 3 < self.difficulty_level <= 6:
            self.fleet_rows = 5
            self.medium_alien_type = randint(1, 2)
            self.last_alien_type = None
            self.extra_event = 0
        else:
            self.fleet_rows = 6
            self.extra_event = randint(1, 7)
            if self.extra_event != 7:
                self.medium_alien_type = randint(1, 2)
                self.last_alien_type = choice(["elite", "juggernaut"])
            else:
                self.last_alien_type = "extra"
        columns_coef = self.fleet_rows - 4
        self.fleet_columns = 16 - columns_coef

        # Aliens setup
        self.mother_ship = MotherShip(self)
        self.aliens = pygame.sprite.Group()
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(1000, 1500)

        # Other setup
        self.stars = pygame.sprite.Group()

        # gun setup
        self.live_surf = pygame.transform.scale(pygame.image.load("graphics/Gun_0/Gun_0.png"), (60, 32))
        self.live_x_start_pos = self.settings.width - (self.live_surf.get_size()[0] + 20)
        self.live_y_start_pos = self.settings.height - (self.live_surf.get_size()[0] * 2 + 20)

        self.hp_left_surf = pygame.transform.scale(pygame.image.load("graphics/HP.png"), (36, 32))
        self.hp_x_start_pos = 0 + self.hp_left_surf.get_size()[0]
        self.hp_y_start_pos = self.settings.height - (self.hp_left_surf.get_size()[0] + 20)

        # fleet and space
        self._create_fleet()
        self._create_sky()
        self.fleet_power = 0
        self.fleet_power = len(self.aliens)
        self.speed_rise = 0.5

    def init_data(self):
        with open('saves/score.json', 'r') as score:
            self.score = json.load(score)
        self.game_score = 0
        self.difficulty_level = 1

        if self.score == 0:
            with open('saves/difficulty_level.json', 'w') as d_l:
                json.dump(self.difficulty_level, d_l)

            self._create_obs()
            self.stats = GameStats()
            with open('saves/game_stats.pickle', 'wb') as g_s:
                pickle.dump(self.stats, g_s)
        else:
            with open('saves/difficulty_level.json', 'r') as d_l:
                self.difficulty_level = json.load(d_l)
            with open('saves/game_stats.pickle', 'rb') as g_s:
                self.stats = pickle.load(g_s)
                if self.stats.gun_booster == 1:
                    self.stats.gun_boost_1(self.settings)
                elif self.stats.gun_booster == 2:
                    self.stats.gun_boost_2(self.settings)
            with open('saves/blocks.json', 'r') as b:
                blocks = json.load(b)
                self.blocks = pygame.sprite.Group()
                for key in blocks.keys():
                    block_list = blocks.get(key)
                    block = obstacle.BLock(block_list[0], block_list[1], self.surface, block_list[2], block_list[3])
                    self.blocks.add(block)
        with open('saves/record.json', 'r') as rec:
            self.record_score = json.load(rec)

    def _create_obs(self):
        self.blocks = pygame.sprite.Group()
        self.obstacle_x_pos = [num * (self.settings.width // self.settings.obstacles_amount) for num in
                               range(self.settings.obstacles_amount)]
        self.obstacle = obstacle.Obstacle()
        self.obstacle.create_multiple_obstacles(*self.obstacle_x_pos, x_pos=self.settings.width / 15, y_pos=750,
                                                size=self.settings.block_size, screen=self.surface,
                                                blocks=self.blocks)

    def _create_sky(self):
        star = Star(self)
        star_width, star_height = star.rect.size

        available_space_x = self.settings.width
        number_columns = available_space_x // (3 * star_width)

        available_space_y = (self.settings.height - (0 * self.gun.sprite.rect.height))
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

    def _create_fleet(self):
        number_columns = self.fleet_columns
        number_rows = self.fleet_rows
        for row_num in range(number_rows):
            alien_design = randint(1, 3)
            for column_num in range(number_columns):
                self._create_alien(column_num, row_num, alien_design)

    def _create_medium_aliens(self, alien_design):
        if self.medium_alien_type == 1:
            shield_percentage = randint(1, 4)
            if shield_percentage == 4:
                return AlienOfficer(self, alien_design=alien_design, hp=2)
            else:
                return AlienOfficer(self, alien_design=alien_design)
        elif self.medium_alien_type == 2:
            shield_percentage = randint(1, 4)
            if shield_percentage == 4:
                return AlienSniper(self, alien_design=alien_design, hp=2)
            else:
                return AlienSniper(self, alien_design=alien_design)

    def _create_low_alien(self, alien_design):
        shield_percentage = randint(1, 4)
        if shield_percentage == 4:
            return Alien(self, alien_design=alien_design, hp=2)
        else:
            return Alien(self, alien_design=alien_design)

    def _create_alien(self, column_num, row_num, alien_design):
        if self.difficulty_level <= 3:
            alien = self._create_low_alien(alien_design)
        elif 3 < self.difficulty_level <= 6:
            if row_num == 0 or row_num == 1:
                alien = self._create_medium_aliens(alien_design)
            else:
                alien = self._create_low_alien(alien_design)
        else:
            if self.extra_event == 10:
                if row_num <= 2:
                    alien = ExtraAlienElite(self)
                else:
                    alien = ExtraAlien(self)
            else:
                if row_num == 0:
                    if self.last_alien_type == "elite":
                        alien = AlienElite(self)
                    elif self.last_alien_type == "juggernaut":
                        alien = AlienJuggernaut(self)
                elif row_num == 1 or row_num == 2:
                    alien = self._create_medium_aliens(alien_design)
                else:
                    alien = self._create_low_alien(alien_design)
        alien_width, alien_height = alien.rect.size

        alien.root_pos_x = alien_width + 1.5 * alien_width * column_num
        alien.root_pos_y = alien_height + 2 * alien_height * row_num + 2 * alien_height

        alien.rect.x = alien_width + alien_width * 15 - (alien_width / 2)
        alien.rect.y = alien_height - 3 * alien_height
        alien.x = float(alien.rect.x)
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            alien.rect.x -= (self.settings.alien_speed * self.settings.fleet_direction)
        self.settings.fleet_direction *= -1

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            if event.type == self.ALIENLASER:
                self._alien_shot()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.gun.sprite.mright = True
        elif event.key == pygame.K_LEFT:
            self.gun.sprite.mleft = True
        elif event.key == pygame.K_ESCAPE:
            self.game_active = False
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.gun.sprite.mright = False
        elif event.key == pygame.K_LEFT:
            self.gun.sprite.mleft = False

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.surface.get_rect().bottom:
                self._gun_hit()
                break

    def _check_collisions(self):
        if self.bullets.sprites():
            pygame.sprite.groupcollide(self.bullets, self.blocks, True, True)
            collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
            for list_obj in collision.values():
                for alien in list_obj:
                    if not alien.destroy:
                        alien.hp -= self.settings.gun_damage
                        alien.shouted_animation()
                        self.explosion_shield.play()
                        if alien.hp <= 0:
                            self.game_score += alien.score
                            alien.destroy_animation()
                            self.alien_explosion_sound.play()
            collision = pygame.sprite.groupcollide(self.bullets, self.extra, True, False)
            for list_obj in collision.values():
                for extra in list_obj:
                    if self.last_alien_type == "juggernaut":
                        self.stats.gun_booster = randint(1, 2)
                        if self.stats.gun_booster == 1:
                            self.stats.gun_boost_1(self.settings)
                        elif self.stats.gun_booster == 2:
                            self.stats.gun_boost_2(self.settings)
                        self.gun = pygame.sprite.GroupSingle(Gun(self))
                        self.powerup.play()
                    else:
                        booster = randint(1, 3)
                        if booster == 1:
                            self.stats.booster_1()
                        elif booster == 2:
                            self.stats.booster_2()
                        elif booster == 3:
                            self._create_obs()
                        self.powerup.play()
                    self.game_score += extra.score
                    extra.destroy_animation()
                    self.extra_explosion_sound.play()
            collision = pygame.sprite.groupcollide(self.bullets, self.bombs, True, False)
            for list_obj in collision.values():
                for bomb in list_obj:
                    self.game_score += 10
                    bomb.destroy_animation()
                    self.explosion_gun_hp.play()

        if self.aliens.sprites():
            pygame.sprite.groupcollide(self.aliens, self.blocks, False, True)
        if self.lasers.sprites():
            pygame.sprite.groupcollide(self.lasers, self.blocks, True, True)
            for laser in self.lasers:
                if pygame.sprite.spritecollide(laser, self.gun, False):
                    laser.kill()
                    self.stats.hp -= laser.damage
                    self.explosion_gun_hp.play()
                    if self.stats.hp <= 0:
                        self.gun.sprite.destroy_animation()
                        self._gun_hit()
                    else:
                        self.gun.sprite.damage_animation()
        if self.bombs.sprites():
            collision = pygame.sprite.groupcollide(self.bombs, self.gun, True, False)
            for bomb in collision.keys():
                bomb.destroy_animation()
                self.stats.hp -= bomb.damage
                self.explosion_gun_hp.play()
                if self.stats.hp <= 0:
                    self.gun.sprite.destroy_animation()
                    self._gun_hit()
                else:
                    self.gun.sprite.damage_animation()
            collision = pygame.sprite.groupcollide(self.bombs, self.blocks, False, True)
            for bomb in collision.keys():
                bomb.destroy_animation()
                self.explosion_gun_hp.play()
                self.explosion_armour.play()

    def _check_game(self):
        if len(self.aliens) == 0 and len(self.lasers) == 0 and len(self.bombs) == 0 and len(self.bullets) == 0:
            self.game_active = False
            self.game_end_active = True
            self.game_status = "victory"

    def display_lives(self):
        for live in range(self.stats.guns_left - 1):
            x = self.live_x_start_pos
            y = self.live_y_start_pos + (live * self.live_surf.get_size()[0] + 10)
            self.surface.blit(self.live_surf, (x, y))
        for hp in range(self.stats.hp):
            x = self.hp_x_start_pos + (hp * (self.hp_left_surf.get_size()[0] + 10))
            y = self.hp_y_start_pos
            self.surface.blit(self.hp_left_surf, (x, y))

    def _extra_alien_timer(self):
        if len(self.extra) == 0:
            self.extra_spawn_time -= 1
        if self.extra_spawn_time == 0:
            if self.extra_event != 10:
                if self.last_alien_type == "juggernaut":
                    alien = "control"
                else:
                    alien = "extra"
                if alien == 'extra':
                    sprite = Extra(self, choice(['right', 'left']))
                elif alien == 'control':
                    sprite = Bomber(self, choice(['right', 'left']))
            else:
                sprite = SuperExtra(self, choice(['right', 'left']))
            self.extra.add(sprite)
            self.extra_spawn_time = randint(100, 500)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound.play()

    def _alien_shot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(self, random_alien)
            self.lasers.add(laser_sprite)

    def _gun_hit(self):
        self.gun_explosion_sound.play()
        self.stats.guns_left -= 1
        if self.stats.guns_left != 0:
            self.stats.reset_gun_boost(self.settings)
            self.stats.hp = 3
            pygame.time.set_timer(self.ALIENLASER, 0)

            self.bullets.empty()
            self.lasers.empty()
            self.bombs.empty()
            copy_aliens = self.ending()
            self.gun = pygame.sprite.GroupSingle(Gun(self))

            sleep(0.5)

            while self.opening:
                for alien_copy in copy_aliens:
                    alien_copy.rect.x = alien_copy.root_pos_x
                    alien_copy.rect.y = alien_copy.root_pos_y
                    alien_copy.x = float(alien_copy.rect.x)
                    self.aliens.add(alien_copy)
                    self._update_screen()
                self.opening = False

            sleep(0.5)
            pygame.time.set_timer(self.ALIENLASER, 500)
        else:
            self.bullets.empty()
            self.lasers.empty()
            self.bombs.empty()
            self.end_scene()
            self.game_active = False
            self.game_end_active = True
            self.game_status = "defeat"

    def ending(self):
        self.opening = True
        copy_aliens = self.aliens.copy()
        for alien in self.aliens:
            self.aliens.remove(alien)
            self._update_screen()
        return copy_aliens

    def end_scene(self):
        pygame.time.set_timer(self.ALIENLASER, 0)
        counter = 200
        while counter != 0:
            counter -= 1
            for alien in self.aliens:
                alien.animation()
            self._update_screen()

    def open_scene(self):
        alien_first = self.aliens.sprites()[0]
        self.surface.blit(self.mother_ship.image, self.mother_ship.rect)
        if self.mother_ship.rect.y != 0 - self.mother_ship.rect.height // 2:
            self.mother_ship.rect.y += 1
            alien_first.rect.y += 1
        else:
            if alien_first.rect.y != 0 + 2 * alien_first.rect.height:
                alien_first.rect.y += 1
            else:
                sleep(0.5)
                for alien in self.aliens:
                    alien.rect.x = alien.root_pos_x
                    alien.rect.y = alien.root_pos_y
                    alien.x = float(alien.rect.x)
                    self._update_screen()
                sleep(0.5)
                while self.mother_ship.rect.y != self.mother_ship.root_pos:
                    self.mother_ship.rect.y -= 1
                    self._update_screen()
                self.opening = False

    def _update_alien_speed(self):
        if len(self.aliens) == int(self.fleet_power - (self.fleet_power / 4)):
            self.fleet_power = len(self.aliens)
            self.settings.alien_speed += self.speed_rise

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_lasers(self):
        self.lasers.update()
        self.bombs.update()

        for laser in self.lasers.copy():
            if laser.rect.top >= self.settings.height:
                self.lasers.remove(laser)
        for bomb in self.bombs.copy():
            if bomb.rect.bottom >= self.settings.height:
                self.bombs.remove(bomb)
                self.explosion_gun_hp.play()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.gun.sprite, self.aliens):
            self.gun.sprite.destroy_animation()
            self._gun_hit()

        self._check_aliens_bottom()

    def quit_func(self):
        self.game_end_active = False

    def _update_screen(self):
        self.surface.fill(self.settings.bc_color)
        self.stars.draw(self.surface)
        self.extra.draw(self.surface)
        self.aliens.draw(self.surface)
        self.surface.blit(self.mother_ship.image, self.mother_ship.rect)
        self.gun.sprite.blit()
        self.display_lives()
        for bullet in self.bullets.sprites():
            bullet.draw()
        for laser in self.lasers.sprites():
            laser.draw()
        for block in self.blocks:
            block.draw()
        for bomb in self.bombs.sprites():
            bomb.draw()
        self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
        pygame.display.update()
        self.clock.tick(self.settings.FPS)

    def defeat_game_status(self):
        self.text = "Defeat"
        with open("saves/score.json", "w") as score:
            self.score = 0
            json.dump(self.score, score)
        while self.game_end_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_func()
            self.stars.draw(self.surface)
            self.extra.draw(self.surface)
            self.aliens.draw(self.surface)
            self.gun.sprite.blit()
            self.display_lives()

            self.surface.blit(self.surf, self.surf.get_rect())
            self.surface.blit(f2.render(f"Record: {self.record_score}", False, self.settings.WHITE),
                              (self.surface.get_rect().centerx - 590, 400))
            self.surface.blit(f2.render(f"Score: {self.score}", False, self.settings.RED),
                              (self.surface.get_rect().centerx - 590, 600))
            self.surface.blit(f3.render(self.text, False, self.settings.WHITE),
                              (self.surface.get_rect().centerx - (len(self.text) * 25), 200))
            self.main_menu_button.button(self.surface, self.screen)
            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
            pygame.display.update()
            self.clock.tick(self.settings.FPS)
        with open('saves/game_stats.pickle', 'wb') as g_s:
            self.stats.reset()
            pickle.dump(self.stats, g_s)
        with open('saves/difficulty_level.json', 'w') as d_l:
            self.difficulty_level = self.settings.difficulty_level
            json.dump(self.difficulty_level, d_l)

    def victory_game_status(self):
        self.text = "Victory"
        result = self.score + self.game_score
        while self.game_end_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_func()
            self.stars.draw(self.surface)
            self.extra.draw(self.surface)
            self.aliens.draw(self.surface)
            self.gun.sprite.blit()
            self.display_lives()

            self.surface.blit(self.surf, self.surf.get_rect())
            if result > self.record_score:
                self.surface.blit(f2.render(f"Record: {self.record_score}", False, self.settings.WHITE),
                                  (self.surface.get_rect().centerx - 590, 400))
                self.surface.blit(f2.render(f"Score: {self.score} + {self.game_score} = {result}", False,
                                            self.settings.YELLOW), (self.surface.get_rect().centerx - 590, 600))
                self.surface.blit(f2.render("NEW RECORD", False, self.settings.YELLOW),
                                  (self.surface.get_rect().centerx - 590, 500))
            else:
                self.surface.blit(f2.render(f"Record: {self.record_score}", False, self.settings.YELLOW),
                                  (self.surface.get_rect().centerx - 590, 400))
                self.surface.blit(f2.render(f"Score: {self.score} + {self.game_score} = {result}", False,
                                            self.settings.WHITE), (self.surface.get_rect().centerx - 590, 600))
            self.surface.blit(f3.render(self.text, False, self.settings.WHITE),
                              (self.surface.get_rect().centerx - (len(self.text) * 25), 200))
            self.main_menu_button.button(self.surface, self.screen)
            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
            pygame.display.update()
            self.clock.tick(self.settings.FPS)
        with open('saves/score.json', 'w') as score:
            self.score += self.game_score
            json.dump(self.score, score)
            if self.score > self.record_score:
                with open('saves/record.json', 'w') as record_score:
                    json.dump(self.score, record_score)
        with open('saves/game_stats.pickle', 'wb') as g_s:
            pickle.dump(self.stats, g_s)
        with open('saves/blocks.json', 'w') as b:
            x = 0
            blocks = {}
            for block in self.blocks:
                x += 1
                blocks[x] = [block.size, block.color, block.x, block.y]
            json.dump(blocks, b)
        with open('saves/difficulty_level.json', 'w') as d_l:
            self.difficulty_level += 1
            json.dump(self.difficulty_level, d_l)

    def run_game(self):
        while self.opening:
            self.open_scene()
            self._update_screen()
        sleep(0.5)
        pygame.time.set_timer(self.ALIENLASER, 500)
        pygame.mixer.music.load("sound/music.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        while self.game_active:
            self._check_events()
            self._check_game()
            self.gun.sprite.update()
            self._update_bullets()
            self._update_lasers()
            self._check_collisions()
            self._extra_alien_timer()
            self.extra.update()
            self._update_alien_speed()
            self._update_aliens()
            self._update_screen()
        pygame.time.set_timer(self.ALIENLASER, 0)
        pygame.mixer.music.stop()
        if self.game_status == "victory":
            self.victory_game_status()
        elif self.game_status == "defeat":
            self.defeat_game_status()
