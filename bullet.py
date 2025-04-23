import pygame as pg
import math
from entity import Entity


class Bullet(Entity):
    _cached_frames = None

    def __init__(self, x, y, mouse_pos, size):
        super().__init__("picture/bullet1_strip.png",x, y)
        self.__speed = 20
        self.__size = size
        self.__frame_speed = 100
        if Bullet._cached_frames is None:
            Bullet._cached_frames = self.load_frames(frame_width=10, frame_height=10, num_frames=2)
        self.__frames = Bullet._cached_frames
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


class DemonBullet(Entity):
    _cached_frames = None

    def __init__(self, x, y, player, size, damage=10):
        super().__init__("Game_Final_Project1/picture/DemonBullet.png",x, y)
        self.damage = damage
        self.__speed = 20
        self.__size = size
        self.__frame_speed = 100
        if DemonBullet._cached_frames is None:
            DemonBullet._cached_frames = self.load_frames(num_frames=8)
        self.__frames = DemonBullet._cached_frames
        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]
        self.__last_update = pg.time.get_ticks()

        # self.rect = self.rect(center=(x,y))
        self.velocity = self.calculate_direction(player)
        self.color = (255, 0, 0)
        self.rect = self.rect.inflate(-self.rect.width * 0.9, -self.rect.height * 0)

        self.not_hit = True

    def load_frames(self, num_frames):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height
        w, h = frame_width * 2, frame_height * 2
        frames = []
        for i in range(num_frames):
            frame = pg.transform.scale(self.image.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)), (w,h))
            frames.append(frame)
        return frames

    def calculate_direction(self, player):
        dir_x = (player.rect.centerx - self.rect.centerx)
        dir_y = (player.rect.centery - self.rect.centery)
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

class DemonBullet(Entity):
    _cached_frames = None

    def __init__(self, x, y, player, size, damage=10):
        super().__init__("Game_Final_Project1/picture/DemonBullet.png",x, y)
        self.damage = damage
        self.__speed = 15
        self.__size = size
        self.__frame_speed = 100
        if DemonBullet._cached_frames is None:
            DemonBullet._cached_frames = self.load_frames(num_frames=8)
        self.__frames = DemonBullet._cached_frames
        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]
        self.__last_update = pg.time.get_ticks()

        # self.rect = self.rect(center=(x,y))
        self.velocity = self.calculate_direction(player)
        self.color = (255, 0, 0)
        self.rect = self.rect.inflate(-self.rect.width * 0.9, -self.rect.height * 0)

        self.not_hit = True

    def load_frames(self, num_frames):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height
        w, h = frame_width * 2, frame_height * 2
        frames = []
        for i in range(num_frames):
            frame = pg.transform.scale(self.image.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)), (w,h))
            frames.append(frame)
        return frames

    def calculate_direction(self, player):
        dir_x = (player.rect.centerx - self.rect.centerx)
        dir_y = (player.rect.centery - self.rect.centery)
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


class CthuluBullet(Entity):
    _cached_frames = None

    def __init__(self, x, y, player, size, damage=10):
        super().__init__("Game_Final_Project1/picture/CthuluBullet.png", x, y)
        self.damage = damage
        self.__speed = 10
        self.__size = size
        self.__frame_speed = 100
        if CthuluBullet._cached_frames is None:
            CthuluBullet._cached_frames = self.load_frames(num_frames=16)
        self.__frames = CthuluBullet._cached_frames
        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]
        self.__last_update = pg.time.get_ticks()

        # self.rect = self.rect(center=(x,y))
        self.velocity = self.calculate_direction(player)
        self.color = (255, 0, 0)
        self.rect = self.rect.inflate(-self.rect.width * 0.8, +self.rect.height * 2.5)

        self.not_hit = True

    def load_frames(self, num_frames):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height
        w, h = frame_width * self.__size[0], frame_height * self.__size[1]
        frames = []
        for i in range(10):
            frame = pg.transform.scale(self.image.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)), (w,h))
            frames.append(frame)
        return frames

    def calculate_direction(self, player):
        dir_x = (player.rect.centerx - self.rect.centerx)
        dir_y = (player.rect.centery - self.rect.centery)
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
        # pg.draw.rect(screen, (0, 255, 0), camera.apply(self), 2)


