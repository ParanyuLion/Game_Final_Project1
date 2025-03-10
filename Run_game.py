import pygame as pg
import Player as player
from background import Background
from game_config import Config
from bullet import Bullet
from Enemy import Enemy
from UI import HealthBar


class Run_game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Game')
        self.__screen = pg.display.set_mode((Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT')))
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__background = pg.image.load(Background.get("FOREST"))
        self.player = player.Player()
        self.player.draw(self.__screen)
        self.__running = True
        self.bullets = []
        self.enemies = []
        self.health_bar = HealthBar(20, 20, 300, 35, self.player.health)
        for i in range(3):
            self.enemies.append(Enemy())

    def update_all(self):
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background, (0, 0))
        self.player.draw(self.__screen)
        for bullet in self.bullets:
            bullet.draw(self.__screen)

        for enemies in self.enemies:
            enemies.draw(self.__screen)

        self.health_bar.draw(self.__screen, self.player.health)

    def entities_events(self):
        """"bullets event"""
        for bullet in self.bullets:
            if 1000 > bullet.bullet_rect.centerx > 0 and 1000 > bullet.bullet_rect.centery > 0:
                bullet.update()
                for enemy in self.enemies:
                    if enemy.get_damage((bullet.bullet_rect.x, bullet.bullet_rect.y)):
                        if bullet in self.bullets:
                            self.bullets.pop(self.bullets.index(bullet))
                    if enemy.check_dead():
                        self.enemies.pop(self.enemies.index(enemy))
            else:
                self.bullets.pop(self.bullets.index(bullet))

        """"enemies event"""
        for enemy in self.enemies:
            enemy.move((self.player.player_rect.centerx , self.player.player_rect.centery))

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
                    self.bullets.append(Bullet(self.player.player_rect.x + width // 2,
                                               self.player.player_rect.y + height // 2,
                                               mouse_pos, (20, 20)))

            self.entities_events()
            key = pg.key.get_pressed()
            # print(self.player.player_rect.y, self.player.player_rect.x)
            if key[pg.K_w] and self.player.player_rect.y > 0:
                self.player.move("UP")
            if key[pg.K_s] and self.player.player_rect.y < Config.get('WIN_HEIGHT') - 160:
                self.player.move("DOWN")
            if key[pg.K_a] and self.player.player_rect.x > 0:
                self.player.move("LEFT")
            if key[pg.K_d] and self.player.player_rect.x < Config.get('WIN_WIDTH') - 160:
                self.player.move("RIGHT")

            pg.display.update()
            clock.tick(Config.get('FPS'))
        pg.quit()


play = Run_game()
play.run_loop()
