import pygame as pg
from game_config import Config


class Player:
    def __init__(self, x, y, health=100):
        self.health = health
        self.__player_pic = pg.image.load("Game_Final_Project1/picture/AnimationSheet_Character.png")
        self.__frames = self.load_frames(8, 9)
        self.__frame_speed = 100
        self.__frame_index = 0
        self.__current_frame = self.__frames[self.__frame_index]
        self.__last_update = 0
        self.player_rect = self.__current_frame.get_rect(center=(x, y))
        self.last_move_rect = self.player_rect.copy()
        self.move_direction = "RIGHT"
        self.__speed = 2
        self.__dash_speed = 120

    def load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.__player_pic.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        frames = []
        for i in range(num_frames):
            frame = pg.transform.scale(self.__player_pic.subsurface(pg.Rect(i * frame_width, 3 * frame_height, frame_width, frame_height)), (80,80))
            frames.append(frame)
        return frames

    def move(self, dir):
        print(self.__frame_index)
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            if self.move_direction == "RIGHT":
                self.__current_frame = self.__frames[self.__frame_index]
            else:
                self.__current_frame = pg.transform.flip(self.__frames[self.__frame_index], True, False)

        self.last_move_rect = self.player_rect.copy()

        if dir == "UP":
            self.player_rect.y -= self.__speed
            # self.move_direction = "UP"
        if dir == "LEFT":
            self.player_rect.x -= self.__speed
            self.move_direction = "LEFT"
        if dir == "RIGHT":
            self.player_rect.x += self.__speed
            self.move_direction = "RIGHT"
        if dir == "DOWN":
            self.player_rect.y += self.__speed
            # self.move_direction = "DOWN"

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
        screen.blit(self.__current_frame, self.player_rect)

    def get_size(self):
        return self.__current_frame.get_size()
