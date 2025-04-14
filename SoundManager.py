import pygame as pg


class SoundManager:
    __instance = None

    @staticmethod
    def get_instance():
        if SoundManager.__instance is None:
            SoundManager()
        return SoundManager.__instance

    def __init__(self):
        if SoundManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SoundManager.__instance = self

        pg.mixer.init()
        self.sounds = {
            "bgm": {"type": "music", "path": "Game_Final_Project1/Sound/bg_music.wav"},
            "CthuluTheme": {"type": "music", "path": "Game_Final_Project1/Sound/CthuluTheme.mp3"},
            "game_over_music": {"type": "music", "path": "Game_Final_Project1/Sound/game_over_music.mp3"},
            "game_over_sound": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/game_over_sound.mp3"),
                           "volume": 1},


            "PlayerMove": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/PlayerMove.wav"),
                           "volume": 0.3},
            "PlayerAttack": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/PlayerAttack.wav"),
                             "volume": 1},
            "PlayerDash": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/PlayerDash.wav"),
                           "volume": 1},
            "FireBreathe": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/FireBreathe.wav"),
                            "volume": 1},
            "ThunderStrike": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/ThunderStrike.wav"),
                              "volume": 1},
            "PlayerBulletHit": {"type": "effect",
                                "sound": pg.mixer.Sound("Game_Final_Project1/Sound/PlayerBulletHit.wav"),
                                "volume": 0.3},

            "Buy": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/Buy.wav"), "volume": 1},
            "CantBuy": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/CantBuy.wav"),
                        "volume": 1},
            "UseItem": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/UseItem.wav"),
                        "volume": 1},
            "DoorOpen": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/DoorOpen.mp3"),
                         "volume": 1},
            "DoorClose": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/DoorClose.mp3"),
                          "volume": 1},
            "Hover": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/Hover.wav"),
                          "volume": 1},
            "AtkBuff": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/AtkBuff.wav"),
                          "volume": 0.7},
            "SpeedBuff": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/SpeedBuff.wav"),
                      "volume": 0.5},

            "Dead": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/Dead.wav"),
                     "volume": 0.6},
            "SlimeAttack": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/SlimeAttack.wav"),
                            "volume": 1},
            "DemonBulletHit": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/Explosion.mp3"),
                               "volume": 0.1},
            "DemonShoot": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/DemonShoot.wav"),
                           "volume": 0.2},
            "MinotaurAtk": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/Slash1.wav"),
                            "volume": 0.6},
            "CthuluAtk": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/Slash2.wav"),
                          "volume": 0.6},
            "CthuluShoot": {"type": "effect", "sound": pg.mixer.Sound("Game_Final_Project1/Sound/CthuluShoot.wav"),
                            "volume": 0.6},
            "CthuluBulletHit": {"type": "effect",
                                "sound": pg.mixer.Sound("Game_Final_Project1/Sound/CthuluBulletHit.wav"),
                                "volume": 0.2},
            "CthuluChangePhase": {"type": "effect",
                                  "sound": pg.mixer.Sound("Game_Final_Project1/Sound/CthuluChangePhase.wav"),
                                  "volume": 1},
        }
        self.music_volume = 0.2
        self.effect_volume = 0.5

    def load_sound(self, name, path, is_music=False):
        if is_music:
            self.sounds[name] = {"type": "music", "path": path}
        else:
            self.sounds[name] = {"type": "effect", "sound": pg.mixer.Sound(path)}
            self.sounds[name]["sound"].set_volume(self.effect_volume)

    def play_sound(self, name):
        if name in self.sounds and self.sounds[name]["type"] == "effect":
            self.sounds[name]["sound"].set_volume(self.effect_volume * self.sounds[name]["volume"])
            self.sounds[name]["sound"].play()

    def play_music(self, name, loop=-1):
        if name in self.sounds and self.sounds[name]["type"] == "music":
            pg.mixer.music.load(self.sounds[name]["path"])
            pg.mixer.music.set_volume(self.music_volume)
            pg.mixer.music.play(loop)

    def stop_music(self):
        pg.mixer.music.stop()

    def set_music_volume(self, volume):
        self.music_volume = volume
        pg.mixer.music.set_volume(volume)

    def set_effect_volume(self, volume):
        self.effect_volume = volume
        for data in self.sounds.values():
            if data["type"] == "effect":
                data["sound"].set_volume(volume)

    def stop_all(self):
        pg.mixer.stop()
        pg.mixer.music.stop()
