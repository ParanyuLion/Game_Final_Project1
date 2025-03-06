class Background:
    __CONFIGS = {
        'FOREST': "Game_Final_Project1/picture/bg1.png"
    }
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]