import pygame as pg
from Player import Player
from game_config import Config


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
                self.x - self.border, self.y - self.border, self.width + self.border * 2,
                self.height + self.border * 2))
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


class ManaBar:
    def __init__(self, x, y, width, height, max_mana):
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

        pg.draw.rect(screen, "black", (
            self.x - self.border, self.y - self.border, self.width + self.border * 2, self.height + self.border * 2))
        pg.draw.rect(screen, (160, 0, 0), (self.x, self.y, self.width, self.height))

        pg.draw.rect(screen, "black", (self.x - self.border, self.y - self.border, self.width * ratio + self.border * 2,
                                       self.height + self.border * 2))
        pg.draw.rect(screen, (36, 109, 208), (self.x, self.y, self.width * ratio, self.height))
        pg.draw.rect(screen, (34, 100, 189), (self.x, self.y + 10, self.width * ratio, self.height - 10))
        pg.draw.rect(screen, (30, 87, 164), (self.x, self.y + self.height - 10, self.width * ratio, 10))

        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)


class Inventory:
    def __init__(self, x, y, width, height, player):
        self.player = player
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = height // 8
        self.font_size = 20
        self.font = pg.font.SysFont('calibri', self.font_size, bold=True)
        self.item_size = (70, 70)
        self.inventory_slot = pg.transform.scale(
            pg.image.load('Game_Final_Project1/picture/InventorySlot.png').convert_alpha(), (80, 80))
        self.list_item = [{'key': '1',
                           'img': pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/HealPotion.png"),
                                                     self.item_size), 'value': 'heal_potion'},
                          {'key': '2',
                           'img': pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/ManaPotion.png"),
                                                     self.item_size), 'value': 'mana_potion'},
                          {'key': 'Q',
                           'img': pg.transform.scale(
                               pg.image.load("Game_Final_Project1/picture/MagicIcon/FireBreathIcon.png"),
                               self.item_size), 'value': 'fire_breathe'},
                          {'key': 'R',
                           'img': pg.transform.scale(
                               pg.image.load("Game_Final_Project1/picture/MagicIcon/ThunderStrikeIcon.png"),
                               self.item_size), 'value': 'thunder_strike'},
                          {'key': 'SPACE',
                           'img': pg.transform.scale(
                               pg.image.load("Game_Final_Project1/picture/dash/DashIcon.png").convert_alpha(),
                               self.item_size), 'value': None},
                          ]
        self.__num_slots = len(self.list_item)

    def get_value(self, value):
        if value == 'heal_potion':
            return self.player.health_potion
        if value == 'mana_potion':
            return self.player.mana_potion
        if value == 'fire_breathe':
            return self.player.unlock_fire_breathe
        if value == 'thunder_strike':
            return self.player.unlock_fire_breathe
        else:
            return True

    def draw(self, screen, player):
        slot_width, slot_height = self.inventory_slot.get_size()
        total_width = self.__num_slots * slot_width
        self.x = (Config.get('WIN_WIDTH') - total_width) // 2
        for i, item in enumerate(self.list_item):
            screen.blit(self.inventory_slot, (self.x + i * 80, self.y))
            if not isinstance(self.get_value(item['value']), bool):
                text = self.font.render(f"{self.get_value(item['value'])}", True, (255, 255, 255))
                screen.blit(text, (self.x + i * 80 + 8, self.y + 5 + 5))
                if self.get_value(item['value']) == 0:
                    img = item['img'].copy()
                    img.set_alpha(50)
                    screen.blit(img, (self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                                      self.y + (slot_width - self.item_size[0]) / 2))
                else:
                    screen.blit(item['img'], (self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                                              self.y + (slot_width - self.item_size[0]) / 2))

            else:
                if self.get_value(item['value']):
                    screen.blit(item['img'], (self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                                              self.y + (slot_width - self.item_size[0]) / 2))
                else:
                    img = item['img'].copy()
                    img.set_alpha(50)
                    screen.blit(img, (self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                                      self.y + (slot_width - self.item_size[0]) / 2))
                    text = self.font.render(f"Locked", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(self.x + i * 80 + slot_width / 2, self.y + slot_width / 2))
                    screen.blit(text, text_rect)
            text = self.font.render(f"[{(item['key'])}]", True, (255, 255, 255))
            # screen.blit(text, (self.x + i * 80 + 29, self.y + 90))
            text_rect = text.get_rect(center=(self.x + i * 80 + slot_width / 2, self.y + 95))
            screen.blit(text, text_rect)
