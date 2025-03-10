import pygame as pg
import random
from UI import HealthBar


class Enemy:
    def __init__(self, health=10, damage=5):
        self.__health = health
        self.__speed = 0.01
        self.__damage = damage
        self.__enemy_char = pg.transform.scale(pg.image.load("Game_Final_Project1/picture/blue_slime1.png"), (80,80))
        self.enemy_rect = self.__enemy_char.get_rect()
        self.enemy_rect.center = (random.randint(0,1000),(random.randint(0,620)))
        self.health_bar = HealthBar(self.enemy_rect.x, self.enemy_rect.y, 100, 15, self.__health)
        self.last_move_rect = self.enemy_rect.copy()

    def move(self, pos):
        self.last_move_rect = self.enemy_rect.copy()
        width, height = self.get_size()
        # if self.enemy_rect.x + width//2 < pos[0]:
        #     self.enemy_rect.x += self.speed
        # elif self.enemy_rect.x + width//2 > pos[0]:
        #     self.enemy_rect.x -= self.speed
        #     self.enemy_rect.y -= self.speed
        # if self.enemy_rect.y + height//2 < pos[1]:
        #     self.enemy_rect.y += self.speed
        # elif self.enemy_rect.y + height//2 > pos[1]:
        #     self.enemy_rect.y -= self.speed
        if self.enemy_rect.x + width//2 != pos[0] or self.enemy_rect.y + height//2 != pos[1]:
            self.enemy_rect.x += (pos[0]-(self.enemy_rect.x + width//2))*self.__speed
            self.enemy_rect.y += (pos[1]-(self.enemy_rect.y + width//2))*self.__speed
            # print(-(self.enemy_rect.x + width//2-pos[0])*self.speed)

    def get_damage(self, pos):
        width, height = self.get_size()
        if (abs(self.enemy_rect.x + width // 2 - pos[0]) < 40) and (abs(self.enemy_rect.y + height // 2 - pos[1]) < 40):
            self.__health -= 1
            return True

    def check_dead(self):
        if self.__health <= 0:
            return True

    def hit_player(self, pos):
        width, height = self.get_size()
        if (abs(self.enemy_rect.x + width//2 - pos[0]) < 60) and (abs(self.enemy_rect.y + height//2 - pos[1]) < 60):
            # print(width, height)
            # print("pos e", self.enemy_rect.x, self.enemy_rect.y)
            # print((self.enemy_rect.x + width//2 - pos[0]) ,(self.enemy_rect.y + height//2 - pos[1]))
            return True

    def draw(self, screen):
        self.health_bar.draw(screen, self.__health, self.enemy_rect.x, self.enemy_rect.y)
        screen.blit(self.__enemy_char, self.enemy_rect)

    def get_size(self):
        return self.__enemy_char.get_size()
