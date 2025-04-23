import pygame as pg
from entity import Entity


class Explosion(Entity):
    _cached_frames = None

    def __init__(self, x, y, img="picture/explosion.png"):
        super().__init__(img, x, y)
        if Explosion._cached_frames is None:
            Explosion._cached_frames = self.__load_frames(7, 1)
        self.__frames = Explosion._cached_frames
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


class CthuluExplosion(Entity):
    _cached_frames = None

    def __init__(self, x, y, img="picture/CthuluBullet.png"):
        super().__init__(img,x, y)
        if CthuluExplosion._cached_frames is None:
            CthuluExplosion._cached_frames = self.__load_frames(16, 1)
        self.__frames = CthuluExplosion._cached_frames
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
        for i in range(8,num_frames):
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


class DashEffect(Entity):
    def __init__(self, x, y, img="picture/dash/FX001_01.png"):
        super().__init__(img, x, y)
        image1 = pg.image.load("picture/dash/FX001_01.png").convert_alpha()
        image2 = pg.image.load("picture/dash/FX001_02.png").convert_alpha()
        image3 = pg.image.load("picture/dash/FX001_03.png").convert_alpha()
        image4 = pg.image.load("picture/dash/FX001_04.png").convert_alpha()
        image5 = pg.image.load("picture/dash/FX001_05.png").convert_alpha()
        self.__list_img = [image1, image2, image3, image4, image5]
        self.__frames = self.__load_frames()
        self.__last_update = 0
        self.__frame_speed = 50
        self.__frame_index = 0
        self.finish = True
        self.image = self.__frames[self.__frame_index]

    def __load_frames(self):
        frame_width, frame_height = self.image.get_size()
        size = 3
        w, h = frame_width * size, frame_height * size
        frames = []
        """load animation"""
        for i in self.__list_img:
            frame = pg.transform.scale(i, (w, h))
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


class FireBreatheEffect(Entity):
    _cached_frames = None

    def __init__(self, x, y, img="picture/FireMagic/Fire Breath hit effect SpriteSheet.png"):
        super().__init__(img, x, y)
        if FireBreatheEffect._cached_frames is None:
            FireBreatheEffect._cached_frames = self.__load_frames(5, 1)
        self.__frames = FireBreatheEffect._cached_frames
        self.__last_update = 0
        self.__frame_speed = 100
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
