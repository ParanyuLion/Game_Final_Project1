import pygame as pg
import random
from UI import HealthBar
from entity import Entity
import math


class Enemy(Entity):
    def __init__(self,x,y, health=10, damage=2):
        super().__init__("Game_Final_Project1/picture/blue_slime1.png",x,y, 80)
        self.__health = health
        self.__speed = 1.5
        self.__damage = damage
        self.__direction = pg.math.Vector2()
        self.__velocity = pg.math.Vector2()
        self.health_bar = HealthBar(self.rect.x, self.rect.y, 100, 15, self.__health)
        self.last_move_rect = self.rect.copy()
        self.last_attack_time = 0
        self.__position = pg.math.Vector2(x,y)

    def move(self, player):
        self.last_move_rect = self.rect.copy()

        player_vector = pg.math.Vector2(player.rect.center)
        enemy_vector = pg.math.Vector2(self.rect.center)
        distance = enemy_vector.distance_to(player_vector)

        if distance > 0:
            self.__direction = (player_vector - enemy_vector).normalize()
        else:
            self.__direction = pg.math.Vector2()

        self.__position += self.__direction * self.__speed
        self.rect.topleft = (int(self.__position.x), int(self.__position.y))

    def get_damage(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.__health -= 1
            return True

    def check_dead(self):
        if self.__health <= 0:
            return True
        return False

    def hit_player(self, player):
        current_time = pg.time.get_ticks()
        if self.rect.colliderect(player.rect):
            if current_time - self.last_attack_time > 500:
                player.health -= self.__damage
                self.last_attack_time = current_time
                return True

    def draw(self, screen,camera):
        self.health_bar.draw(screen, self.__health, self.rect.x, self.rect.y)
        screen.blit(self.image, self.rect)

    def get_size(self):
        return self.image.get_size()
