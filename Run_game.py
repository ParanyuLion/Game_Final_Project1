import pygame as pg
from Player import Player
from background import Background as Bgd
from game_config import Config
from bullet import Bullet

from UI import HealthBar
from Slime import Slime
from Minotaur import Minotaur
from Cthulu import Cthulu
import random


class Camera(pg.sprite.Group):
    def __init__(self, width, height):
        super().__init__()
        self.camera_rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target):
        x = target.rect.centerx - Config.get('WIN_WIDTH')//2
        y = target.rect.centery - Config.get('WIN_HEIGHT')//2
        self.camera_rect.topleft = (x, y)


class RunGame:
    def __init__(self):
        """set up game"""
        pg.init()
        pg.display.set_caption('Game')
        self.__screen = pg.display.set_mode((Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT')))
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__running = True

        """background attribute"""
        self.level_name = 'lv1'
        self.__background = Bgd.load_bg(self.level_name)
        self.bg_width, self.bg_height = self.__background.get_size()
        self.__border = Bgd.get(self.level_name, 'border')
        self.__level = 0
        self.__complete_level = False
        """entities attribute"""
        spawn_point = Bgd.get('lv1', 'spawn')
        self.player = Player(spawn_point[0], spawn_point[1])
        self.bullets = []
        self.bullet_size = (20, 20)
        self.enemies = []
        self.health_bar = HealthBar(20, 20, 300, 35, self.player.health)
        self.camera = Camera(Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT'))
        self.camera.add(self.player, *self.enemies, *self.bullets)
        self.player.draw(self.__screen, self.camera)
        self.__last_shot_time = 0
        self.__at_door = False
        # self.count = 0

    def update_all(self):
        self.camera.update(self.player)
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background, (-self.camera.camera_rect.x, -self.camera.camera_rect.y))
        # self.player.draw(self.__screen, self.camera)
        for entity in self.camera:
            entity.draw(self.__screen, self.camera)

        self.health_bar.draw(self.__screen, self.player.health)
        # self.camera.draw(self.__screen)

    def entities_events(self):
        """players event"""
        self.__at_door = self.player.door_collision(Bgd.get(self.level_name, 'door'))

        """"bullets event"""
        for bullet in self.bullets:
            # check that bullets not go out of border
            if (self.__border["RIGHT"] + self.bullet_size[0]*2.5 > bullet.rect.centerx > self.__border["LEFT"] and
                    self.__border["DOWN"] + self.bullet_size[1]*3.5 > bullet.rect.centery > self.__border["UP"]):
                bullet.update()
                for enemy in self.enemies:
                    if enemy.check_alive() and enemy.get_damage(bullet):
                        if bullet in self.bullets:
                            self.camera.remove(bullet)
                            # self.bullets.pop(self.bullets.index(bullet))
                            self.bullets.remove(bullet)
                            self.camera.remove(bullet)
            else:
                self.camera.remove(bullet)
                self.bullets.pop(self.bullets.index(bullet))

        """enemies event"""
        for enemy in self.enemies:
            enemy.move(self.player, self.enemies)
            if enemy.hit_player(self.player):
                pass
            if enemy.already_dead:
                self.enemies.remove(enemy)
                self.camera.remove(enemy)
        if len(self.enemies) == 0:
            self.__complete_level = True
        else:
            self.__complete_level = False

    def set_level(self, name):
        self.__background = Bgd.load_bg(name)
        self.__border = Bgd.get(name, 'border')
        self.player.rect.center = Bgd.get(name, 'spawn')

    def load_level(self):
        self.enemies.clear()
        if self.__level == 1:
            self.level_name = 'lv1'
            for i in range(1):
                self.enemies.append(Cthulu(x=random.randint(0, 1000), y=random.randint(0, 620), health=5))
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif self.__level == 2:
            self.level_name = 'lv2'

            for i in range(2):
                self.enemies.append(Minotaur(x=random.randint(0, 1000), y=random.randint(0, 620), health=5))
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif self.__level == 3:
            self.level_name = 'lv3'
            for i in range(3):
                self.enemies.append(Slime(x=random.randint(0, 1000), y=random.randint(0, 620), health=5))
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif self.__level == 4:
            self.level_name = 'lv2'
            for i in range(4):
                self.enemies.append(Slime(x=random.randint(0, 1000), y=random.randint(0, 620), health=5))
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        else:
            self.level_name = 'lv2'
            for i in range(self.__level):
                self.enemies.append(Slime(x=random.randint(0, 1000), y=random.randint(0, 620), health=5))
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

    def run_loop(self):
        clock = pg.time.Clock()
        while self.__running:
            # start_time = pg.time.get_ticks()
            self.update_all()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.dash()
                    if event.key == pg.K_e and self.__complete_level and self.__at_door:
                        self.__level += 1
                        self.load_level()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        now = pg.time.get_ticks()
                        if now - self.__last_shot_time > self.player.atk_speed * 4:
                            mouse_pos = pg.mouse.get_pos()

                            mouse_pos_world = (mouse_pos[0] + self.camera.camera_rect.x,
                                               mouse_pos[1] + self.camera.camera_rect.y)
                            if mouse_pos_world[0] < self.player.rect.x:
                                self.player.set_left_right("LEFT")
                            else:
                                self.player.set_left_right("RIGHT")
                            self.player.attack()
                            new_bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, mouse_pos_world,
                                                self.bullet_size)
                            self.bullets.append(new_bullet)
                            self.__last_shot_time = now
                            self.camera.add(new_bullet, *self.bullets)

            self.entities_events()
            key = pg.key.get_pressed()
            # print(self.player.player_rect.y, self.player.player_rect.x)
            if key[pg.K_w] and self.player.wall_collision("UP", self.__border["UP"]):
                self.player.move("UP")
            if key[pg.K_s] and self.player.wall_collision("DOWN", self.__border["DOWN"]):
                self.player.move("DOWN")
            if key[pg.K_a] and self.player.wall_collision("LEFT", self.__border["LEFT"]):
                self.player.move("LEFT")
            if key[pg.K_d] and self.player.wall_collision("RIGHT", self.__border["RIGHT"]):
                self.player.move("RIGHT")

            pg.display.flip()
            clock.tick(Config.get('FPS'))
            # end_time = pg.time.get_ticks()  # วัดเวลาสิ้นสุดของเฟรม
            # print(f"Frame time: {end_time - start_time} ms")
    pg.quit()


play = RunGame()
play.run_loop()
