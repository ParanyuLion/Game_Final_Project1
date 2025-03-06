class Config:
    __CONFIGS = {
        'WIN_WIDTH': 1000,
        'WIN_HEIGHT': 620,
        'FPS': 60,
        'BG_COLOR': (0,0,0)
    }
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]
