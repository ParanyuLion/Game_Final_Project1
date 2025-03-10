import pygame as pg
import math


class Bullet:
    def __init__(self, x, y, mouse_pos,radius):
        self.x = x
        self.y = y
        self.__speed = 20
        self.velocity = self.calculate_direction(mouse_pos)
        self.color = (255, 0, 0)
        self.radius = radius
        self.not_hit = True

    def calculate_direction(self, mouse_pos):
        dir_x = (mouse_pos[0] - self.x)
        dir_y = (mouse_pos[1] - self.y)
        vector_length = math.sqrt(dir_x**2 + dir_y**2)
        dir_vector = [(dir_x/vector_length)*self.__speed, (dir_y/vector_length)*self.__speed]
        return dir_vector

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)
