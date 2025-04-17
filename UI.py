import pygame as pg
from Player import Player
from SoundManager import SoundManager
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


class Gold:
    def __init__(self, x, y, player):
        self.__x = x
        self.__y = y
        self.__player = player
        self.__font_size = 25
        self.__font = pg.font.SysFont('calibri', self.__font_size, bold=True)
        self.__img = pg.transform.scale(
            pg.image.load('Game_Final_Project1/picture/Coin.png').convert_alpha(), (40, 40))
        self.__img_size = self.__img.get_size()

    def draw(self, screen, x=None, y=None):
        if x is None and y is None:
            screen.blit(self.__img, (self.__x-self.__img_size[0], self.__y-self.__img_size[1]//2))
            text = self.__font.render(f"{self.__player.gold}", True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(self.__x, self.__y-self.__img_size[1]//3))
            screen.blit(text, text_rect)
        else:
            screen.blit(self.__img, (x - self.__img_size[0], y - self.__img_size[1] // 2))
            text = self.__font.render(f"{self.__player.gold}", True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(x, y - self.__img_size[1] // 3))
            screen.blit(text, text_rect)


class Inventory:
    def __init__(self, x, y, player, fire_breathe):
        self.player = player
        self.fire_breathe = fire_breathe
        self.x = x
        self.y = y
        self.font_size = 20
        self.font = pg.font.SysFont('calibri', self.font_size, bold=True)
        self.item_size = (70, 70)
        self.inventory_slot = pg.transform.scale(
            pg.image.load('Game_Final_Project1/picture/InventorySlot.png').convert_alpha(), (80, 80))
        self.list_item = [{'key': 'CLICK',
                           'img': pg.transform.scale(pg.image.load("Game_Final_Project1/picture/MagicIcon/ShootingIcon.png").convert_alpha(),
                                                     self.item_size), 'value': None},
                          {'key': '1',
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
        self.__bg_rect = pg.Rect(x-50, y-50, self.__num_slots * 80,  80)

    def get_value(self, value):
        if value == 'heal_potion':
            return self.player.health_potion
        if value == 'mana_potion':
            return self.player.mana_potion
        if value == 'fire_breathe':
            return self.player.unlock_fire_breathe
        if value == 'thunder_strike':
            return self.player.unlock_thunder_strike
        else:
            return True

    def draw(self, screen):
        pg.draw.rect(screen, (44, 44, 44), (self.x-5, self.y-5, self.__num_slots * 80 + 10, 120), border_radius=10)
        pg.draw.rect(screen, (112, 112, 112), (self.x - 5, self.y - 5, self.__num_slots * 80 + 10, 120), width=2,
                     border_radius=10)
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

            """overlay cooldown"""
            key = item['key']
            if key in self.player.last_activate:
                now = pg.time.get_ticks()
                last_used = self.player.last_activate[key]
                duration = self.player.cooldown_durations.get(key, 0)
                time_since_used = now - last_used

                if time_since_used < duration:
                    cooldown_ratio = 1 - (time_since_used / duration)
                    overlay = pg.Surface(self.item_size, pg.SRCALPHA)
                    overlay.fill((0, 0, 0, 180))
                    overlay_height = int(self.item_size[1] * cooldown_ratio)
                    overlay_rect = pg.Rect(0, 0, self.item_size[0], overlay_height)
                    if key != '1' and key != '2':
                        screen.blit(overlay.subsurface(overlay_rect), (
                            self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                            self.y + (slot_width - self.item_size[1]) / 2 + (self.item_size[1] - overlay_height)
                        ))
                    elif key == '1' and self.player.health_potion > 0:
                        screen.blit(overlay.subsurface(overlay_rect), (
                            self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                            self.y + (slot_width - self.item_size[1]) / 2 + (self.item_size[1] - overlay_height)
                        ))
                    elif key == '2' and self.player.mana_potion > 0:
                        screen.blit(overlay.subsurface(overlay_rect), (
                            self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                            self.y + (slot_width - self.item_size[1]) / 2 + (self.item_size[1] - overlay_height)
                        ))

                elif key == 'Q' and self.fire_breathe.activate:
                    overlay = pg.Surface(self.item_size, pg.SRCALPHA)
                    overlay.fill((0, 0, 0, 180))
                    overlay_height = int(self.item_size[1])
                    overlay_rect = pg.Rect(0, 0, self.item_size[0], overlay_height)
                    screen.blit(overlay.subsurface(overlay_rect), (
                        self.x + i * 80 + (slot_width - self.item_size[0]) / 2,
                        self.y + (slot_width - self.item_size[1]) / 2 + (self.item_size[1] - overlay_height)
                    ))
            text = self.font.render(f"[{(item['key'])}]", True, (255, 255, 255))
            # screen.blit(text, (self.x + i * 80 + 29, self.y + 90))
            text_rect = text.get_rect(center=(self.x + i * 80 + slot_width / 2, self.y + 95))
            screen.blit(text, text_rect)


class InteractUI:
    @staticmethod
    def draw_interact_door(screen):
        x,y = Config.get('WIN_WIDTH')//2+30, Config.get('WIN_HEIGHT')//2-30
        width, height = 150, 50
        pg.draw.rect(screen, (44, 44, 44), (x,y, width, height), border_radius=5)
        pg.draw.rect(screen, (112, 112, 112), (x-2,y-2, width+4, height+4), width=3,border_radius=5)
        font = pg.font.SysFont('calibri', 20, bold=True)
        text = font.render(f"Press E to enter", True, (255, 255, 255))
        text_rect = text.get_rect(center=(x+width//2,y+height//2))
        screen.blit(text, text_rect)



