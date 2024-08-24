class Settings:
    def __init__(self):
        self.FPS = 60
        self.width = 1920
        self.height = 1011

        # gun
        self.gun_speed = 5
        self.gun_damage = 1
        self.gun_booster = 0

        self.bullet_speed = 20
        self.bullet_w = 3
        self.bullet_h = 12
        self.bullet_color = (0, 255, 0)
        self.bullets_allowed = 1

        # aliens
        self.alien_speed = 1
        self.fleet_drop_speed = 32
        """направление флота 1(право) -1(лево)"""
        self.fleet_direction = 1
        self.difficulty_level = 1

        self.extra_speed_positive = 2
        self.extra_speed_negative = -2
        self.bomber_speed_positive = 1
        self.bomber_speed_negative = -1

        # obstacles
        self.obstacles_amount = 4
        self.block_size = 12

        # color
        self.bc_color = (0, 0, 0)
        self.WHITE = "#ffffff"
        self.BLACK = "#000000"
        self.RED = "#f14f50"
        self.YELLOW = "#ffe200"

        # images
        self.button_inactive = "graphics/button_inactive.png"
        self.button_active = "graphics/button_active.png"

        # info
        self.by = "Created by Alkrei"
        self.engine = "Pygame-ce"
        self.version = "2.0"
