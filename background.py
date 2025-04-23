import pygame as pg


class Background:
    __CONFIGS = {
        1: {'image': "picture/background/map1.png",
            'border': {"LEFT": 59, "RIGHT": 1256, "UP": 230, "DOWN": 740}, 'spawn': (400, 500),
            'door': {'x': (1221, 1260), 'y': (418, 586)},
            'enemy_spawn': {'x': (620, 1060), 'y': (300, 500)}},
        2: {'image': "picture/background/map2.png",
            'border': {"LEFT": 144, "RIGHT": 942, "UP": 242, "DOWN": 1810}, 'spawn': (200, 1800),
            'door': {'x': (475, 622), 'y': (220, 262)},
            'enemy_spawn': {'x': (200, 800), 'y': (100, 700)}},
        3: {'image': "picture/background/map3.png",
            'border': {"LEFT": 100, "RIGHT": 2060, "UP": 247, "DOWN": 912}, 'spawn': (205, 919),
            'door': {'x': (2039, 2065), 'y': (500, 660)},
            'enemy_spawn': {'x': (500, 1900), 'y': (330, 800)}},
        4: {'image': "picture/background/map4.png",
            'border': {"LEFT": 100, "RIGHT": 2306, "UP": 247, "DOWN": 914}, 'spawn': (186, 557),
            'door': {'x': (2257, 2348), 'y': (489, 643)},
            'enemy_spawn': {'x': (800, 2000), 'y': (330, 700)}},
        10: {'image': "picture/background/dungeon_tile.png",
             'border': {"LEFT": 225, "RIGHT": 1380, "UP": 222, "DOWN": 1356}, 'spawn': (500, 500),
             'door': {'x': (0, 9999), 'y': (0, 9999)},
             'enemy_spawn': {'x': (500, 1900), 'y': (330, 800)}},
        'MainMenu': {'image': "picture/background/menu.png",
                     'border': {"LEFT": 9999, "RIGHT": 9999, "UP": 9999, "DOWN": 9999}},
        'GameOver': {'image': "Game_Final_Project1/picture/background/game_over_bg.png",
                     'border': {"LEFT": 9999, "RIGHT": 9999, "UP": 9999, "DOWN": 9999}},
        'shop': {'image': "picture/background/shop_bg.png",
                 'door': {'x': (0, 9999), 'y': (0, 9999)},
                 'border': {"LEFT": 9999, "RIGHT": 9999, "UP": 9999, "DOWN": 9999}, 'spawn': (500, 500)},
        'setting': {'image': "picture/background/setting_bg.png",
                 'door': {'x': (0, 9999), 'y': (0, 9999)},
                 'border': {"LEFT": 9999, "RIGHT": 9999, "UP": 9999, "DOWN": 9999}, 'spawn': (500, 500)},
    }

    @classmethod
    def get(cls, key1, key2):
        return cls.__CONFIGS[key1][key2]

    @classmethod
    def load_bg(cls, name):
        bg = pg.image.load(Background.get(name, 'image'))
        w, h = bg.get_size()
        if name == 'shop':
            return pg.transform.scale(bg, (w * 1, h * 1))
        return pg.transform.scale(bg, (w * 3.5, h * 3.5))

    @classmethod
    def load_menu(cls, name):
        bg = pg.image.load(Background.get(name, 'image'))
        w, h = bg.get_size()
        if name == 'GameOver':
            return pg.transform.scale(bg, (w * 1, h * 1))
        elif name == 'setting':
            return pg.transform.scale(bg, (w * 1, h * 1))
        return pg.transform.scale(bg, (w * 4.7, h * 4.7))
