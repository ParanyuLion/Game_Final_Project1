import pygame as pg
import math


class Bullet:
    def __init__(self, x, y, mouse_pos, size):
        self.__speed = 10
        self.__size = size
        self.__frame_speed = 50
        self.__bullet_pic = pg.image.load("Game_Final_Project1/picture/bullet1_strip.png")
        self.__frames = self.load_frames(frame_width=10, frame_height=10, num_frames=2)
        self.__frame_index = 0
        self.__current_frame = self.__frames[self.__frame_index]
        self.__last_update = pg.time.get_ticks()
        self.bullet_rect = self.__bullet_pic.get_rect(center=(x,y))
        self.velocity = self.calculate_direction(mouse_pos)
        self.color = (255, 0, 0)

        self.not_hit = True

    def load_frames(self, frame_width, frame_height, num_frames):
        """ ตัดเฟรมออกจาก Sprite Sheet """
        frames = []
        for i in range(num_frames):
            frame = pg.transform.scale(self.__bullet_pic.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)), self.__size)
            frames.append(frame)
        return frames

    def calculate_direction(self, mouse_pos):
        dir_x = (mouse_pos[0] - self.bullet_rect.x)
        dir_y = (mouse_pos[1] - self.bullet_rect.y)
        vector_length = math.sqrt(dir_x**2 + dir_y**2)
        dir_vector = [(dir_x/vector_length)*self.__speed, (dir_y/vector_length)*self.__speed]
        return dir_vector

    def update(self):
        self.bullet_rect.x += self.velocity[0]
        self.bullet_rect.y += self.velocity[1]
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            self.__current_frame = self.__frames[self.__frame_index]

    def draw(self, screen):
        screen.blit(self.__current_frame, self.bullet_rect)
