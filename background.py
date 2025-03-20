import pygame as pg
class Background:
    __CONFIGS = {
        'lv1': {'image': "Game_Final_Project1/picture/dungeon_tile.png",
                'border': {"LEFT":225,"RIGHT":1380,"UP": 222,"DOWN":1356}, 'spawn': (500,500)},
        'lv2': {'image': "Game_Final_Project1/picture/map1.png",
                'border': {"LEFT":59,"RIGHT":1256,"UP": 230,"DOWN":740}, 'spawn': (400,500), 'door':()},
        'lv3': {'image': "Game_Final_Project1/picture/map2.png",
                'border': {"LEFT":144,"RIGHT":942,"UP": 242,"DOWN":1810}, 'spawn': (200, 1800)}
    }
    @classmethod
    def get(cls, key1, key2):
        return cls.__CONFIGS[key1][key2]

    @classmethod
    def load_bg(cls, name):
        bg = pg.image.load(Background.get(name, 'image'))
        w,h = bg.get_size()
        return pg.transform.scale(bg, (w*3.5, h*3.5))
