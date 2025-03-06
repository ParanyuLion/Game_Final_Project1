import pygame as pg
import Player as player
from background import Background
from game_config import Config


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

    def update_all(self):
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background, (0, 0))
        self.player.draw(self.__screen)

    def run_loop(self):
        while self.__running:
            self.update_all()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.dash()
            key = pg.key.get_pressed()
            # print(self.player.player_rect.y, self.player.player_rect.x)
            if key[pg.K_w] and self.player.player_rect.y > 0:
                self.player.move("UP")
            if key[pg.K_s] and self.player.player_rect.y < Config.get('WIN_HEIGHT')-160:
                self.player.move("DOWN")
            if key[pg.K_a] and self.player.player_rect.x > 0:
                self.player.move("LEFT")
            if key[pg.K_d] and self.player.player_rect.x < Config.get('WIN_WIDTH')-160:
                self.player.move("RIGHT")

            pg.display.update()
        pg.quit()


play = Run_game()
play.run_loop()
