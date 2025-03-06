import pygame as pg
from game_config import Config
class Player:
    def __init__(self, health=100):
        self.health = health
        # self.__positions = [0,0]
        self.player_char = pg.image.load("Game_Final_Project1/picture/beast.png")
        self.player_rect = self.player_char.get_rect()
        self.player_rect.center = (Config.get("WIN_WIDTH") // 2, Config.get("WIN_HEIGHT") // 2)
        self.last_move_rect = self.player_rect.copy()
        self.move_direction = "RIGHT"
        self.__speed = 2
        self.__dash_speed = 120

    def move(self, dir):
        self.last_move_rect = self.player_rect.copy()

        if dir == "UP":
            self.player_rect.y -= self.__speed
            self.move_direction = "UP"
        if dir == "LEFT":
            self.player_rect.x -= self.__speed
            self.move_direction = "LEFT"
        if dir == "RIGHT":
            self.player_rect.x += self.__speed
            self.move_direction = "RIGHT"
        if dir == "DOWN":
            self.player_rect.y += self.__speed
            self.move_direction = "DOWN"

    def attack(self):
        pass

    def dash(self):
        self.last_move_rect = self.player_rect.copy()
        if self.move_direction == "UP":
            self.player_rect.y -= self.__dash_speed

        if self.move_direction == "LEFT":
            self.player_rect.x -= self.__dash_speed

        if self.move_direction == "RIGHT":
            self.player_rect.x += self.__dash_speed

        if self.move_direction == "DOWN":
            self.player_rect.y += self.__dash_speed

    def draw(self, screen):
        screen.blit(self.player_char, self.player_rect)




