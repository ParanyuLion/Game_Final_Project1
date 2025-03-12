import pygame as pg
from game_config import Config


class Player:
    def __init__(self, x, y, health=100):
        self.health = health
        self.__player_pic = pg.image.load("Game_Final_Project1/picture/AnimationSheet_Character.png")
        self.__atk_frames = []
        self.__atk_frames_index = 0

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
        self.atk_state = False


    def load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.__player_pic.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        frames = []
        for i in range(num_frames):
            frame = pg.transform.scale(self.__player_pic.subsurface(pg.Rect(i * frame_width, 3 * frame_height, frame_width, frame_height)), (80,80))
            frames.append(frame)
        for i in range(num_frames):
            atk_frames = pg.transform.scale(self.__player_pic.subsurface(pg.Rect(i * frame_width, 8 * frame_height, frame_width, frame_height)),(80, 80))
            self.__atk_frames.append(atk_frames)
        return frames

    def walk_animation(self):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            if self.move_direction == "RIGHT":
                self.__current_frame = self.__frames[self.__frame_index]
            else:
                self.__current_frame = pg.transform.flip(self.__frames[self.__frame_index], True, False)

    def atk_animation(self, screen):
        for i in range(len(self.__atk_frames)):
            now = pg.time.get_ticks()
            if now - self.__last_update > 1:
                self.__last_update = now
                self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames)
                if self.atk_state:
                    self.__current_frame = self.__atk_frames[self.__atk_frames_index]
                    print("atk", self.__atk_frames_index)
            screen.blit(self.__current_frame, self.player_rect)
            if self.__atk_frames_index == 7:
                self.atk_state = False
                break

    def move(self, dir):
        print(self.__frame_index)
        self.walk_animation()
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
        self.atk_state = True


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
        """attack animation"""
        if self.atk_state:
            self.atk_animation(screen)
        else:
            """normal animation"""
            screen.blit(self.__current_frame, self.player_rect)

    def get_size(self):
        return self.__current_frame.get_size()
