import pygame as pg
from entity import Entity


class FireBreath(Entity):
    _cached_frames = None

    def __init__(self, x, y):
        super().__init__("Game_Final_Project1/picture/FireMagic/Fire Breath SpriteSheet.png", x, y)
        self.__speed = 20
        self.__frame_speed = 100
        if FireBreath._cached_frames is None:
            FireBreath._cached_frames = self.__load_frames(8, 3)
            FireBreath._cached_frames_flipped = [
                pg.transform.flip(frame, True, False) for frame in FireBreath._cached_frames
            ]

        self.__frames = FireBreath._cached_frames
        self.__frames_flipped = FireBreath._cached_frames_flipped
        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]
        self.__last_update = pg.time.get_ticks()
        self.not_hit = True
        self.activate = False
        self.end_effect = False
        self.last_hit = 0
        self.direction = "RIGHT"
        self.rect = self.rect.inflate((-self.rect.width * 0.5, self.rect.height * 0.4))

    def set_position(self, player_rect, direction):
        flame_width, flame_height = self.image.get_size()
        self.direction = direction
        if direction == "RIGHT":
            self.rect.x = player_rect.centerx
        else:
            self.rect.x = player_rect.centerx - flame_width
        self.rect.y = player_rect.top - flame_height // 2

    def __load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        size = 5
        w, h = frame_width * size, frame_height * size
        frames = []
        """load animation"""
        for i in range(4):
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 1 * frame_height, frame_width, frame_height)), (w, h))
            frames.append(frame)
        return frames

    def hit_enemy(self, enemies):
        now = pg.time.get_ticks()
        if now - self.last_hit > self.__frame_speed * 2 and self.activate:
            hit_list = [enemy for enemy in enemies if
                        self.rect.colliderect(enemy.rect.inflate((-self.rect.width, -self.rect.height)))]

            for enemy in hit_list:
                enemy.health -= 2
            self.last_hit = now

    def __run_animation(self):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            self.image = self.__frames[self.__frame_index] if self.direction == "RIGHT" else self.__frames_flipped[
                self.__frame_index]

    def draw(self, screen, camera):
        if self.activate:
            self.__run_animation()
            screen.blit(self.image, camera.apply(self))

            # pg.draw.rect(screen, (255, 0, 0), camera.apply(self), 2)
