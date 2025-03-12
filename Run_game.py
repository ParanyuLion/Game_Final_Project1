import pygame as pg
import Player as player
from background import Background
from game_config import Config
from bullet import Bullet
from Enemy import Enemy
from UI import HealthBar
import random

import pygame as pg


class Camera(pg.sprite.Group):
    def __init__(self, width, height):
        super().__init__()
        self.camera_rect = pg.Rect(0, 0, width, height)  # ✅ ขนาดของโลกเกม
        self.width = width
        self.height = height

    def apply(self, entity):
        """ ปรับตำแหน่งของ Entity ให้สัมพันธ์กับกล้อง """
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target):
        """ อัปเดตตำแหน่งของกล้องให้ติดตาม Player """
        x = target.rect.centerx - self.width // 2
        y = target.rect.centery - self.height // 2
        self.camera_rect.topleft = (x, y)  # ✅ ป้องกันการขยับพิกเซลผิดเพี้ยน


class Run_game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Game')
        self.__screen = pg.display.set_mode((Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT')))
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__background = pg.image.load(Background.get("FOREST"))
        self.player = player.Player(Config.get('WIN_WIDTH') // 2, Config.get('WIN_HEIGHT') // 2)

        self.__running = True
        self.bullets = []
        self.enemies = []
        self.health_bar = HealthBar(20, 20, 300, 35, self.player.health)
        for i in range(3):
            self.enemies.append(Enemy(x=random.randint(0, 1000), y=random.randint(0, 620)))
        self.camera = Camera(1000, 1000)
        self.camera.add(self.player, *self.enemies, *self.bullets)
        self.player.draw(self.__screen, self.camera)

    def update_all(self):
        self.camera.update(self.player)
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background,
                           (-self.camera.camera_rect.x, -self.camera.camera_rect.y))  # ✅ พื้นหลังสัมพันธ์กับกล้อง
        # self.player.draw(self.__screen, self.camera)
        for entity in self.camera:
            entity.draw(self.__screen, self.camera)

        self.health_bar.draw(self.__screen, self.player.health)
        self.camera.draw(self.__screen)

    def entities_events(self):
        """"bullets event"""
        for bullet in self.bullets:
            if 1000 > bullet.rect.centerx > 0 and 1000 > bullet.rect.centery > 0:
                bullet.update()
                for enemy in self.enemies:
                    if enemy.get_damage(bullet):
                        if bullet in self.bullets:
                            self.camera.remove(bullet)
                            self.bullets.pop(self.bullets.index(bullet))
                    if enemy.check_dead():
                        self.camera.remove(enemy)
                        self.enemies.pop(self.enemies.index(enemy))

            else:
                self.camera.remove(bullet)
                self.bullets.pop(self.bullets.index(bullet))

        """enemies event"""
        for enemy in self.enemies:
            enemy.move(self.player)

            if enemy.hit_player(self.player):
                print(self.player.health)

    def run_loop(self):
        clock = pg.time.Clock()
        while self.__running:
            self.update_all()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.dash()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    width, height = self.player.get_size()
                    self.player.attack()
                    new_bullet = Bullet(self.player.rect.x + width // 2,
                                        self.player.rect.y + height // 2,
                                        mouse_pos, (20, 20))
                    self.bullets.append(new_bullet)
                    self.camera.add(new_bullet, *self.bullets)

            self.entities_events()
            key = pg.key.get_pressed()
            # print(self.player.player_rect.y, self.player.player_rect.x)
            if key[pg.K_w] and self.player.rect.y > 0:
                self.player.move("UP")
            if key[pg.K_s] and self.player.rect.y < Config.get('WIN_HEIGHT'):
                self.player.move("DOWN")
            if key[pg.K_a] and self.player.rect.x > 0:
                self.player.move("LEFT")
            if key[pg.K_d] and self.player.rect.x < Config.get('WIN_WIDTH'):
                self.player.move("RIGHT")

            pg.display.update()
            clock.tick(Config.get('FPS'))
        pg.quit()


play = Run_game()
play.run_loop()
