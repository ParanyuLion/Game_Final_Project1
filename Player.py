import pygame as pg
# from game_config import Config
from entity import Entity
from SoundManager import SoundManager
import time


class Player(Entity):

    def __init__(self, x, y, health=100):
        super().__init__("Game_Final_Project1/picture/AnimationSheet_Character.png", x, y)
        self.max_health = health
        self.health = health
        self.score = 0
        self.max_mana = 100
        self.mana = 100
        self.gold = 500
        self.speed = 5
        self.damage = 1
        self.health_potion = 5
        self.mana_potion = 5
        self.unlock_fire_breathe = False
        self.unlock_thunder_strike = False
        self.fire_breathe_damage = int(round(self.damage*1.25))
        self.thunder_strike_damage = int(round(self.damage * 1.75))
        self.__atk_frames = []
        self.__atk_frames_index = 0

        self.__last_update = 0
        self.__frames = self.__load_frames(8, 9)
        self.__frame_speed = 100
        self.__frame_index = 0
        self.image = self.__frames[self.__frame_index]

        self.rect = self.image.get_rect(center=(x, y))
        self.last_move_rect = self.rect.copy()
        self.move_direction = "RIGHT"
        self.left_right = "RIGHT"

        self.__dash_speed = 120
        self.dash_cooldown = 1000
        self.distance_per_min = 0
        self.last_walk_sound = 0
        self.__walk_sound_cooldown = 300

        self.atk_speed = 30
        self.atk_state = False
        self.walk_state = False
        self.idle_state = True
        self.last_activate = {
            'CLICK': -99999,
            '1': -99999,
            '2': -99999,
            'Q': -99999,
            'R': -99999,
            'SPACE': -99999,
        }
        self.cooldown_durations = {
            'CLICK': 220,
            '1': 2500,
            '2': 2500,
            'Q': 1,
            'R': 2000,
            'SPACE': 1000,

        }

        self.potion_images = {
            "health_potion": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/HealPotion.png"),
                                                (40, 40)),
            "mana_potion": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/ManaPotion.png"),
                                              (40, 40)),
        }
        self.drink_state = False
        self.drink_start_time = 0
        self.drink_duration = 600
        self.current_potion_img = None

    def can_use_skill(self, key):
        now = pg.time.get_ticks()
        return now - self.last_activate.get(key) >= self.cooldown_durations.get(key)

    def use_skill(self, key):
        if self.can_use_skill(key) and not self.drink_state:
            self.last_activate[key] = pg.time.get_ticks()
            return True
        return False

    def __load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        frames = []
        """load walk animation"""
        for i in range(num_frames):
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 3 * frame_height, frame_width, frame_height)), (80, 80))
            frames.append(frame)
        """load attack animation"""
        for i in range(num_frames):
            atk_frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 8 * frame_height, frame_width, frame_height)), (80, 80))
            self.__atk_frames.append(atk_frame)

        return frames

    def walk_animation(self):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)
            if self.left_right == "RIGHT":
                self.image = self.__frames[self.__frame_index]
            else:
                self.image = pg.transform.flip(self.__frames[self.__frame_index], True, False)

    def atk_animation(self, screen, camera):
        for i in range(len(self.__atk_frames)):
            now = pg.time.get_ticks()
            if now - self.__last_update > self.atk_speed:
                self.__last_update = now
                self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames)
                if self.atk_state:
                    if self.left_right == "RIGHT":
                        self.image = self.__atk_frames[self.__atk_frames_index]
                    else:
                        self.image = pg.transform.flip(self.__atk_frames[self.__atk_frames_index], True, False)
                    # print("atk", self.__atk_frames_index)
            screen.blit(self.image, camera.apply(self))
            if self.__atk_frames_index == 7:
                self.atk_state = False
                break

    def door_collision(self, door):
        if (door['x'][0] <= self.rect.x <= door['x'][1]) and (door['y'][0] <= self.rect.y <= door['y'][1]):
            return True
        return False

    def wall_collision(self, direction, wall):
        # print(self.rect.x, self.rect.y)
        if direction == "LEFT":
            if wall < self.rect.x:
                return True
            return False
        elif direction == "RIGHT":
            if wall > self.rect.x:
                return True
            return False
        elif direction == "UP":
            if wall < self.rect.y:
                return True
            return False
        elif direction == "DOWN":
            if wall > self.rect.y:
                return True
            return False

    def move(self, direction):
        # print(self.__frame_index)
        self.walk_animation()
        self.last_move_rect = self.rect.copy()
        self.walk_state = True
        self.idle_state = False
        now = pg.time.get_ticks()
        if now - self.last_walk_sound > self.__walk_sound_cooldown:
            SoundManager.get_instance().play_sound("PlayerMove")
            self.last_walk_sound = now
        if direction == "UP":
            self.rect.y -= self.speed
            self.distance_per_min += self.speed
            if not self.atk_state:
                self.move_direction = "UP"
        if direction == "LEFT":
            self.rect.x -= self.speed
            self.distance_per_min += self.speed
            if not self.atk_state:
                self.move_direction = "LEFT"
                self.left_right = "LEFT"
        if direction == "RIGHT":
            self.rect.x += self.speed
            self.distance_per_min += self.speed
            if not self.atk_state:
                self.move_direction = "RIGHT"
                self.left_right = "RIGHT"
        if direction == "DOWN":
            self.rect.y += self.speed
            self.distance_per_min += self.speed
            if not self.atk_state:
                self.move_direction = "DOWN"

    def attack(self):
        SoundManager.get_instance().play_sound("PlayerAttack")
        self.atk_state = True

    def dash(self, border):
        predict_rect = self.rect.copy()
        # self.last_move_rect = self.rect.copy()
        SoundManager.get_instance().play_sound("PlayerDash")
        if self.move_direction == "UP":
            predict_rect.y -= self.__dash_speed
            if predict_rect.y > border[self.move_direction]:
                self.rect.y -= self.__dash_speed
            else:
                self.rect.y = border[self.move_direction]

        if self.move_direction == "LEFT":
            predict_rect.x -= self.__dash_speed
            if predict_rect.x > border[self.move_direction]:
                self.rect.x -= self.__dash_speed
            else:
                self.rect.x = border[self.move_direction]

        if self.move_direction == "RIGHT":
            predict_rect.x += self.__dash_speed
            if predict_rect.x < border[self.move_direction]:
                self.rect.x += self.__dash_speed
            else:
                self.rect.x = border[self.move_direction]

        if self.move_direction == "DOWN":
            predict_rect.y += self.__dash_speed
            if predict_rect.y < border[self.move_direction]:
                self.rect.y += self.__dash_speed
            else:
                self.rect.y = border[self.move_direction]

    def draw(self, screen, camera):
        if self.atk_state:
            self.atk_animation(screen, camera)
        else:
            screen.blit(self.image, camera.apply(self))

        if self.drink_state:
            now = pg.time.get_ticks()
            if now - self.drink_start_time < self.drink_duration:
                if self.current_potion_img:
                    img_rect = self.current_potion_img.get_rect(center=camera.apply(self).center)
                    screen.blit(self.current_potion_img, img_rect)
            else:
                self.drink_state = False
                self.current_potion_img = None

    def get_size(self):
        return self.image.get_size()

    def set_left_right(self, direction):
        self.left_right = direction

    def drink_potion(self, potion):
        now = pg.time.get_ticks()
        SoundManager.get_instance().play_sound("UseItem")
        if not self.drink_state and potion == 'health_potion' and self.health_potion > 0:
            self.health_potion -= 1
            self.health += 20
            if self.health > self.max_health:
                self.health = self.max_health
            self.drink_state = True
            self.drink_start_time = now
            self.current_potion_img = self.potion_images["health_potion"]
        elif not self.drink_state and potion == 'mana_potion' and self.mana_potion > 0:
            self.mana_potion -= 1
            self.mana += 20
            if self.mana > self.max_mana:
                self.mana = self.max_mana
            self.drink_state = True
            self.drink_start_time = now
            self.current_potion_img = self.potion_images["mana_potion"]

    def get_shoot(self, bullet):
        if self.rect.colliderect(bullet):
            self.health -= bullet.damage
            return True

    def reset_game(self):
        self.health = 100
        self.mana = 100
        self.gold = 500
        self.speed = 5
        self.damage = 1
        self.health_potion = 5
        self.mana_potion = 5
        self.unlock_fire_breathe = False
        self.unlock_thunder_strike = False
