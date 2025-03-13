import pygame as pg
import math
from entity import Entity


class Bullet(Entity):
    def __init__(self, x, y, mouse_pos, size):
        super().__init__("Game_Final_Project1/picture/bullet1_strip.png",x, y)
        self.__speed = 10
        self.__size = size
        self.__frame_speed = 100
        self.__frames = self.load_frames(frame_width=10, frame_height=10, num_frames=2)
        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]
        self.__last_update = pg.time.get_ticks()
        # self.rect = self.rect(center=(x,y))
        self.velocity = self.calculate_direction(mouse_pos)
        self.color = (255, 0, 0)

        self.not_hit = True

    def load_frames(self, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = pg.transform.scale(self.image.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)), self.__size)
            frames.append(frame)
        return frames

    def calculate_direction(self, mouse_pos):
        dir_x = (mouse_pos[0] - self.rect.x)
        dir_y = (mouse_pos[1] - self.rect.y)
        vector_length = math.sqrt(dir_x**2 + dir_y**2)
        dir_vector = [(dir_x/vector_length)*self.__speed, (dir_y/vector_length)*self.__speed]
        return dir_vector

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            self.image = self.__frames[self.__frame_index]

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
