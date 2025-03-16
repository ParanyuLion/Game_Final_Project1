import pygame as pg
from Player import Player
from background import Background
from game_config import Config
from bullet import Bullet
from Enemy import Enemy
from UI import HealthBar
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
        x = target.rect.centerx - 500
        y = target.rect.centery - 360
        self.camera_rect.topleft = (x, y)


class Run_game:
    def __init__(self):
        """set up game"""
        pg.init()
        pg.display.set_caption('Game')
        self.__screen = pg.display.set_mode((Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT')))
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__running = True
        """background attribute"""
        self.__background = pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Dungeon_tile.png"), (1500, 1500))
        self.bg_width, self.bg_height = self.__background.get_size()
        self.__border_x = 200
        self.__border_y = 180
        """entities attribute"""
        self.player = Player(self.bg_width // 2, self.bg_height // 2)
        self.bullets = []
        self.bullet_size = (20,20)
        self.enemies = []
        self.health_bar = HealthBar(20, 20, 300, 35, self.player.health)
        for i in range(3):
            self.enemies.append(Enemy(x=random.randint(0, 1000), y=random.randint(0, 620),health=10))
        self.camera = Camera(Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT'))
        self.camera.add(self.player, *self.enemies, *self.bullets)
        self.player.draw(self.__screen, self.camera)
        self.__last_shot_time = 0

    def update_all(self):
        self.camera.update(self.player)
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background,
                           (-self.camera.camera_rect.x, -self.camera.camera_rect.y))  # ✅ พื้นหลังสัมพันธ์กับกล้อง
        # self.player.draw(self.__screen, self.camera)
        for entity in self.camera:
            entity.draw(self.__screen, self.camera)

        self.health_bar.draw(self.__screen, self.player.health)
        # self.camera.draw(self.__screen)

    def entities_events(self):
        """"bullets event"""
        for bullet in self.bullets:
            # check that bullets not go out of border
            if (self.bg_width-self.__border_x-self.bullet_size[0] > bullet.rect.centerx > self.__border_x and
                    self.bg_width-self.__border_y - self.bullet_size[1]> bullet.rect.centery > self.__border_y):
                bullet.update()
                for enemy in self.enemies:
                    if enemy.check_alive():
                        if enemy.get_damage(bullet):
                            if bullet in self.bullets:
                                self.camera.remove(bullet)
                                self.bullets.pop(self.bullets.index(bullet))
                    # if enemy.check_dead():
                    #     self.camera.remove(enemy)
                    #     self.enemies.pop(self.enemies.index(enemy))

            else:
                self.camera.remove(bullet)
                self.bullets.pop(self.bullets.index(bullet))

        """enemies event"""
        for enemy in self.enemies:
            enemy.move(self.player, self.enemies)
            if enemy.hit_player(self.player):
                pass

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
                    if event.button == pg.BUTTON_LEFT:
                        now = pg.time.get_ticks()
                        if now-self.__last_shot_time > self.player.atk_speed*4:
                            mouse_pos = pg.mouse.get_pos()

                            mouse_pos_world = (mouse_pos[0] + self.camera.camera_rect.x,
                                               mouse_pos[1] + self.camera.camera_rect.y)
                            if mouse_pos_world[0]<self.player.rect.x:
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
            if key[pg.K_w] and self.player.rect.y > self.__border_y:
                self.player.move("UP")
            if key[pg.K_s] and self.player.rect.y < self.bg_height-80-self.__border_y-20:
                self.player.move("DOWN")
            if key[pg.K_a] and self.player.rect.x > self.__border_x:
                self.player.move("LEFT")
            if key[pg.K_d] and self.player.rect.x < self.bg_width-80-self.__border_x:
                self.player.move("RIGHT")

            pg.display.update()
            clock.tick(Config.get('FPS'))
        pg.quit()


play = Run_game()
play.run_loop()
