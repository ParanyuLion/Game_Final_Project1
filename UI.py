import pygame as pg


class HealthBar(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, max_hp):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.border = height // 8
        self.font_size = self.height // 2 + self.border + 5
        self.font = pg.font.SysFont('Arial', self.font_size, bold=True)

    def draw(self, screen, hp, x=None, y=None):
        ratio = hp / self.max_hp
        text = self.font.render(f"{hp}/{self.max_hp}", True, (0, 0, 0))

        if x is None and y is None:
            pg.draw.rect(screen, "black", (
            self.x - self.border, self.y - self.border, self.width + self.border * 2, self.height + self.border * 2))
            pg.draw.rect(screen, (160, 0, 0), (self.x, self.y, self.width, self.height))

            pg.draw.rect(screen, "black", (
            self.x - self.border, self.y - self.border, self.width * ratio + self.border * 2,
            self.height + self.border * 2))
            pg.draw.rect(screen, (121, 215, 57), (self.x, self.y, self.width * ratio, self.height))
            pg.draw.rect(screen, (106, 190, 48), (self.x, self.y + 10, self.width * ratio, self.height - 10))
            pg.draw.rect(screen, (89, 174, 30), (self.x, self.y + self.height - 10, self.width * ratio, 10))

            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)
        else:
            pg.draw.rect(screen, "black", (
            x - self.border, y - self.border, self.width + self.border * 2, self.height + self.border * 2))
            pg.draw.rect(screen, (180, 0, 0), (x, y, self.width, self.height))
            pg.draw.rect(screen, "black", (
            x - self.border, y - self.border, self.width * ratio + self.border * 2, self.height + self.border * 2))
            # pg.draw.rect(screen, (100, 255, 0), (x, y, self.width * ratio, self.height))
            pg.draw.rect(screen, (121, 215, 57), (x, y, self.width * ratio, self.height))
            # pg.draw.rect(screen, (106, 190, 48), (x, y + 10, self.width * ratio, self.height - 10))
            # pg.draw.rect(screen, (89, 174, 30), (x, y + self.height - 10, self.width * ratio, 10))

            text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
            screen.blit(text, text_rect)


class ManaBar(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, max_mana):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_mana = max_mana
        self.border = height // 8
        self.font_size = self.height // 2 + self.border + 5
        self.font = pg.font.SysFont('Arial', self.font_size, bold=True)

    def draw(self, screen, mana):
        ratio = mana / self.max_mana
        text = self.font.render(f"{mana}/{self.max_mana}", True, (0, 0, 0))

        pg.draw.rect(screen, "black", (self.x - self.border, self.y - self.border, self.width + self.border * 2, self.height + self.border * 2))
        pg.draw.rect(screen, (160, 0, 0), (self.x, self.y, self.width, self.height))

        pg.draw.rect(screen, "black", (self.x - self.border, self.y - self.border, self.width * ratio + self.border * 2,
                                       self.height + self.border * 2))
        pg.draw.rect(screen, (36, 109, 208), (self.x, self.y, self.width * ratio, self.height))
        pg.draw.rect(screen, (34, 100, 189), (self.x, self.y + 10, self.width * ratio, self.height - 10))
        pg.draw.rect(screen, (30, 87, 164), (self.x, self.y + self.height - 10, self.width * ratio, 10))

        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)
