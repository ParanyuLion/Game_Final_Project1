import pygame as pg


class Entity(pg.sprite.Sprite):
    def __init__(self, image_path, x, y, size=None):
        super().__init__()
        self.image = pg.image.load(image_path)
        if size is not None:
            self.image = pg.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass

