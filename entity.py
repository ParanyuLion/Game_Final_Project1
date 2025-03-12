import pygame as pg


class Entity(pg.sprite.Sprite):
    def __init__(self, image_path, x, y, size=None):
        super().__init__()
        self.image = pg.image.load(image_path)
        if size is not None:
            self.image = pg.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(x, y))

    def update_camera(self, dir, speed):
        if dir == "UP":
            self.rect.y -= speed
        if dir == "LEFT":
            self.rect.x -= speed
        if dir == "RIGHT":
            self.rect.x += speed
        if dir == "DOWN":
            self.rect.y += speed

