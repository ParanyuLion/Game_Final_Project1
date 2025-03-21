import pygame as pg
class Background:
    __CONFIGS = {
        'lv1': {'image': "Game_Final_Project1/picture/map1.png",
                'border': {"LEFT":59,"RIGHT":1256,"UP": 230,"DOWN":740}, 'spawn': (400,500),
                'door': {'x':(1221, 1256),'y':(418, 586)}}, # door is at right
        'lv2': {'image': "Game_Final_Project1/picture/map2.png",
                'border': {"LEFT":144,"RIGHT":942,"UP": 242,"DOWN":1810}, 'spawn': (200, 1800),
                'door': {'x':(475, 622),'y':(241, 262)}}, # door is at top
        'lv3': {'image': "Game_Final_Project1/picture/map3.png",
                'border': {"LEFT": 100, "RIGHT": 2060, "UP": 247, "DOWN": 912}, 'spawn': (205, 919),
                'door': {'x': (2039, 2065), 'y': (500, 660)}},  # door is at top
        'lv4': {'image': "Game_Final_Project1/picture/dungeon_tile.png",
                'border': {"LEFT": 225, "RIGHT": 1380, "UP": 222, "DOWN": 1356}, 'spawn': (500, 500),
                'door': {'x': (0, 9999), 'y': (0, 9999)}},

    }
    @classmethod
    def get(cls, key1, key2):
        return cls.__CONFIGS[key1][key2]

    @classmethod
    def load_bg(cls, name):
        bg = pg.image.load(Background.get(name, 'image'))
        w,h = bg.get_size()
        return pg.transform.scale(bg, (w*3.5, h*3.5))
