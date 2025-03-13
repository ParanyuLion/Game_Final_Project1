import pygame as pg


class HealthBar(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, max_hp):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.border = height//8
        self.font_size = self.height//2+self.border+5
        self.font = pg.font.SysFont('Arial', self.font_size, bold=True)

    def draw(self, screen, hp, x=None, y=None):
        ratio = hp / self.max_hp
        text = self.font.render(f"{hp}/{self.max_hp}", True, (0, 0, 0))

        if x is None and y is None:
            pg.draw.rect(screen, "black", (self.x - self.border, self.y - self.border, self.width + self.border*2, self.height + self.border*2))
            pg.draw.rect(screen, (180,0,0), (self.x, self.y, self.width, self.height))
            pg.draw.rect(screen, "black", (self.x - self.border, self.y - self.border, self.width* ratio + self.border * 2, self.height + self.border * 2))
            pg.draw.rect(screen, (100,255,0), (self.x, self.y, self.width * ratio, self.height))

            text_rect = text.get_rect(center=(self.x+self.width//2, self.y+self.height//2))
            screen.blit(text, text_rect)
        else:
            pg.draw.rect(screen, "black", (x - self.border, y - self.border, self.width + self.border * 2, self.height + self.border * 2))
            pg.draw.rect(screen, (180, 0, 0), (x, y, self.width, self.height))
            pg.draw.rect(screen, "black", (x - self.border, y - self.border, self.width * ratio + self.border * 2,self.height + self.border * 2))
            pg.draw.rect(screen, (100, 255, 0), (x, y, self.width * ratio, self.height))

            text_rect = text.get_rect(center=(x+self.width//2, y+self.height//2))
            screen.blit(text, text_rect)

