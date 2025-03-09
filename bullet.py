import pygame


class Bullet:
    def __init__(self, x, y, dir,radius):
        self.x = x
        self.y = y
        self.__direction = [0,0]
        self.calculate_direction(dir)
        self.velocity = (20 * self.__direction[0], 20 * self.__direction[1])
        self.color = (255,0,0)
        self.radius = radius

    def calculate_direction(self, dir):
        if dir == 'LEFT':
            self.__direction = [-1, 0]
        if dir == 'RIGHT':
            self.__direction = [1, 0]
        if dir == 'UP':
            self.__direction = [0, -1]
        if dir == 'DOWN':
            self.__direction = [0, 1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
