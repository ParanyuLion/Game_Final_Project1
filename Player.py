import pygame as pg
from game_config import Config
from entity import Entity


class Player(Entity):
    def __init__(self, x, y, health=100):
        super().__init__("Game_Final_Project1/picture/AnimationSheet_Character.png",x, y)
        self.health = health
        self.__atk_frames = []
        self.__atk_frames_index = 0
        self.__frames = self.load_frames(8, 9)
        self.__frame_speed = 100
        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]
        self.__last_update = 0
        self.rect = self.image.get_rect(center=(x, y))
        self.last_move_rect = self.rect.copy()
        self.move_direction = "RIGHT"
        self.__left_right = "RIGHT"
        self.__speed = 2
        self.__dash_speed = 120
        self.atk_speed = 30
        self.atk_state = False
        self.walk_state = False
        self.idle_state = True

    def load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        frames = []
        for i in range(num_frames):
            frame = pg.transform.scale(self.image.subsurface(pg.Rect(i * frame_width, 3 * frame_height, frame_width, frame_height)), (80,80))
            frames.append(frame)
        for i in range(num_frames):
            atk_frames = pg.transform.scale(self.image.subsurface(pg.Rect(i * frame_width, 8 * frame_height, frame_width, frame_height)),(80, 80))
            self.__atk_frames.append(atk_frames)
        return frames

    def walk_animation(self):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            if self.__left_right == "RIGHT":
                self.image = self.__frames[self.__frame_index]
            else:
                self.image = pg.transform.flip(self.__frames[self.__frame_index], True, False)

    def atk_animation(self, screen, camera):
        for i in range(len(self.__atk_frames)):
            now = pg.time.get_ticks()
            if now - self.__last_update > self.atk_speed:
                self.__last_update = now
                self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames)
                if self.atk_state:
                    if self.__left_right == "RIGHT":
                        self.image = self.__atk_frames[self.__atk_frames_index]
                    else:
                        self.image = pg.transform.flip(self.__atk_frames[self.__atk_frames_index], True, False)
                    print("atk", self.__atk_frames_index)
            screen.blit(self.image, camera.apply(self))
            if self.__atk_frames_index == 7:
                self.atk_state = False
                break

    def move(self, dir):
        print(self.__frame_index)
        self.walk_animation()
        self.last_move_rect = self.rect.copy()
        self.walk_state = True
        self.idle_state = False

        if dir == "UP":
            self.rect.y -= self.__speed
            if not self.atk_state:
                self.move_direction = "UP"
        if dir == "LEFT":
            self.rect.x -= self.__speed
            if not self.atk_state:
                self.move_direction = "LEFT"
                self.__left_right = "LEFT"
        if dir == "RIGHT":
            self.rect.x += self.__speed
            if not self.atk_state:
                self.move_direction = "RIGHT"
                self.__left_right = "RIGHT"
        if dir == "DOWN":
            self.rect.y += self.__speed
            if not self.atk_state:
                self.move_direction = "DOWN"

    def attack(self):
        self.atk_state = True

    def dash(self):
        self.last_move_rect = self.rect.copy()
        if self.move_direction == "UP":
            self.rect.y -= self.__dash_speed

        if self.move_direction == "LEFT":
            self.rect.x -= self.__dash_speed

        if self.move_direction == "RIGHT":
            self.rect.x += self.__dash_speed

        if self.move_direction == "DOWN":
            self.rect.y += self.__dash_speed

    def draw(self, screen, camera):
        """attack animation"""
        if self.atk_state:
            self.atk_animation(screen, camera)
        else:
            """normal animation"""
            screen.blit(self.image, camera.apply(self))

    def get_size(self):
        return self.image.get_size()

    def set_left_right(self, dir):
        self.__left_right = dir

