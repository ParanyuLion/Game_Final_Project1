import pygame as pg
from entity import Entity


class Explosion(Entity):
    def __init__(self, x, y, img="Game_Final_Project1/picture/explosion.png"):
        super().__init__(img, x, y)
        self.__frames = self.__load_frames(7, 1)
        self.__last_update = 0
        self.__frame_speed = 50
        self.__frame_index = 0
        self.finish = False
        self.image = self.__frames[self.__frame_index]

    def __load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        size = 3
        w, h = frame_width * size, frame_height * size
        frames = []
        """load animation"""
        for i in range(num_frames):
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 0 * frame_height, frame_width, frame_height)), (w, h))
            frames.append(frame)
        return frames

    def __run_animation(self):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            old_center = self.rect.center
            self.image = self.__frames[self.__frame_index]
            self.rect.size = self.image.get_size()
            self.rect.center = old_center
        if self.__frame_index == len(self.__frames) - 1:
            self.finish = True

    def draw(self, screen, camera):
        if not self.finish:
            self.__run_animation()
            screen.blit(self.image, camera.apply(self))

