from game_config import Config
import pygame as pg


class Camera(pg.sprite.Group):
    def __init__(self, width, height):
        super().__init__()
        self.camera_rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target):
        x = target.rect.centerx - Config.get('WIN_WIDTH') // 2
        y = target.rect.centery - Config.get('WIN_HEIGHT') // 2
        self.camera_rect.topleft = (x, y)
