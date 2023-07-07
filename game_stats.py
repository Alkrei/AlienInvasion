class GameStats:
    def __init__(self):
        self.guns_left = 3
        self.hp = 3

        self.gun_booster = 0

    def reset(self):
        self.guns_left = 3
        self.hp = 3

    def reset_gun_boost(self, settings):
        settings.gun_damage = 1
        settings.gun_speed = 5

        settings.gun_booster = 0
        self.gun_booster = 0

        settings.bullet_speed = 20
        settings.bullets_allowed = 1

    def gun_boost_1(self, settings):
        settings.gun_damage = 1
        settings.gun_speed = 10

        settings.gun_booster = 1
        self.gun_booster = 1

        settings.bullet_speed = 30
        settings.bullets_allowed = 3

    def gun_boost_2(self, settings):
        settings.gun_damage = 3
        settings.gun_speed = 7.5

        settings.gun_booster = 2
        self.gun_booster = 2

        settings.bullet_speed = 15
        settings.bullets_allowed = 2

    def booster_1(self):
        self.hp = 3

    def booster_2(self):
        if self.guns_left != 3:
            self.guns_left += 1
