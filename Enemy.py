import pygame as pg
import random


class Enemy:
    def __init__(self, health=100):
        self.health = health
        self.speed = 0.01
        self.enemy_char = pg.transform.scale(pg.image.load("Game_Final_Project1/picture/blue_slime1.png"), (80,80))
        self.enemy_rect = self.enemy_char.get_rect()
        self.enemy_rect.center = (random.randint(0,1000),(random.randint(0,620)))
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
            self.enemy_rect.x += -(self.enemy_rect.x + width//2-pos[0])*self.speed
            self.enemy_rect.y += -(self.enemy_rect.y + width//2-pos[1])*self.speed
            print(-(self.enemy_rect.x + width//2-pos[0])*self.speed)

    def hit_player(self, pos):
        width, height = self.get_size()

        if (abs(self.enemy_rect.x + width//2 - pos[0]) < 100) and (abs(self.enemy_rect.y + height//2 - pos[1]) < 100):
            # print(width, height)
            # print("pos e", self.enemy_rect.x, self.enemy_rect.y)
            # print((self.enemy_rect.x + width//2 - pos[0]) ,(self.enemy_rect.y + height//2 - pos[1]))
            return True

    def draw(self, screen):
        screen.blit(self.enemy_char, self.enemy_rect)

    def get_size(self):
        return self.enemy_char.get_size()
