import pygame as pg
from UI import HealthBar
from entity import Entity
from Enemy import Enemy


class Cthulu(Entity, Enemy):
    def __init__(self, x, y, health=100, damage=20, img="Game_Final_Project1/picture/cthulu_SpriteSheet.png"):
        super().__init__(img, x, y)
        self.__atk_frames1 = []
        self.__atk_frames2 = []
        self.__fly_frames = []
        self.__atk_frames_index = 0
        self.__attack_animation_set = 1
        self.__dead_frames = []
        self.__dead_frames_index = 0
        self.__dead_frames_speed = 100
        self.__frames = self.__load_frames(15, 7)
        self.__last_update = 0
        self.__frame_speed = 150
        self.__frame_index = 0
        self.__left_right = "RIGHT"
        self.image = self.__frames[self.__frame_index]
        self.__atk_state = False
        self.__move_state = True
        self.already_dead = False

        self.__atk_speed = 600
        self.__atk_frame_speed = self.__atk_speed // 9
        self.__health = health

        self.__speed = 2
        self.__damage = damage
        self.__direction = pg.math.Vector2()
        self.__velocity = pg.math.Vector2()
        self.__max_health = health
        self.health_bar = HealthBar(self.rect.x, self.rect.y, self.image.get_size()[0] // 2, 15, self.__max_health)
        # self.last_move_rect = self.rect.copy()
        self.last_attack_time = 0
        self.__position = pg.math.Vector2(x, y)

    def __load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        w, h = frame_width * 4, frame_height * 4

        frames = []
        """load walk animation"""
        for i in range(12):
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 1 * frame_height, frame_width, frame_height)), (w, h))
            frames.append(frame)
        """load fly animation"""
        for i in range(6):
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 2 * frame_height, frame_width, frame_height)), (w, h))
            self.__fly_frames.append(frame)
        """load melee attack animation"""
        for i in range(9):
            atk_frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 4 * frame_height, frame_width, frame_height)), (w, h))
            self.__atk_frames1.append(atk_frame)
        """load range attack animation"""
        for i in range(7):
            atk_frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 3 * frame_height, frame_width, frame_height)), (w, h))
            self.__atk_frames2.append(atk_frame)
        """load dead animation"""
        for i in range(11):
            dead_frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 6 * frame_height, frame_width, frame_height)), (w, h))
            self.__dead_frames.append(dead_frame)
        return frames

    def __dead_animation(self, screen, camera):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__dead_frames_speed:
            if self.__dead_frames_index == len(self.__dead_frames)-1:
                self.already_dead = True
            self.__last_update = now
            self.__dead_frames_index = (self.__dead_frames_index + 1) % len(self.__dead_frames)
            if not self.check_alive() and not self.already_dead:
                if self.__left_right == "LEFT":
                    self.image = self.__dead_frames[self.__dead_frames_index]
                else:
                    self.image = pg.transform.flip(self.__dead_frames[self.__dead_frames_index], True, False)
        screen.blit(self.image, camera.apply(self))

    def __walk_animation(self):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__frame_speed:
            self.__last_update = now
            self.__frame_index = (self.__frame_index + 1) % len(self.__frames)

            old_center = self.rect.center
            if self.__left_right == "LEFT":
                self.image = self.__frames[self.__frame_index]
            else:
                self.image = pg.transform.flip(self.__frames[self.__frame_index], True, False)
            self.rect.size = self.image.get_size()
            self.rect.center = old_center

    def __atk_animation(self, screen, camera):
        self.__move_state = False
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__atk_frame_speed:
            print(self.rect.center)
            self.__last_update = now
            if self.__attack_animation_set == 1:

                self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames1)
                if self.__atk_state:
                    if self.__left_right == "LEFT":
                        self.image = self.__atk_frames1[self.__atk_frames_index]
                    else:
                        self.image = pg.transform.flip(self.__atk_frames1[self.__atk_frames_index], True, False)

                if self.__atk_frames_index == len(self.__atk_frames1) - 1:
                    self.__attack_animation_set = 2
                    self.__atk_frames_index = -1
                    self.__move_state = True
            else:

                self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames2)
                if self.__atk_state:
                    if self.__left_right == "LEFT":
                        self.image = self.__atk_frames2[self.__atk_frames_index]
                    else:
                        self.image = pg.transform.flip(self.__atk_frames2[self.__atk_frames_index], True, False)

                if self.__atk_frames_index == len(self.__atk_frames2) - 1:
                    self.__attack_animation_set = 1
                    self.__atk_frames_index = -1
                    self.__move_state = True
                # print("atk", self.__atk_frames_index)
        screen.blit(self.image, camera.apply(self))

    def move(self, player, enemies):
        if self.check_alive():
            enemy_hitbox = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)
            player_hitbox = player.rect.inflate(-player.rect.width * 0.7, -player.rect.height * 0.7)

            if not enemy_hitbox.colliderect(player_hitbox):
                if self.__move_state:
                    self.__atk_state = False
                    if player.rect.x > self.rect.center[0]:
                        self.__left_right = "LEFT"
                    else:
                        self.__left_right = "RIGHT"
                    # self.last_move_rect = self.rect.copy()
                    self.__walk_animation()
                    player_vector = pg.math.Vector2(player.rect.center)
                    enemy_vector = pg.math.Vector2(self.rect.center)
                    distance = enemy_vector.distance_to(player_vector)

                    if distance > 0:
                        self.__direction = (player_vector - enemy_vector).normalize()
                    else:
                        self.__direction = pg.math.Vector2()
                    self.avoid_others(enemies)
                    self.__position += self.__direction * self.__speed

                    self.rect.topleft = (int(self.__position.x), int(self.__position.y))

    def avoid_others(self, enemies):
        avoid_vector = pg.math.Vector2(0, 0)
        for other_enemy in enemies:
            if other_enemy is not self:
                distance = self.__position.distance_to(other_enemy.__position)
                if distance < 50:
                    avoid_vector += (self.__position - other_enemy.__position).normalize()

        if avoid_vector.length() > 0:
            self.__direction += avoid_vector.normalize() * 0.5

    def get_damage(self, bullet):
        enemy_hitbox = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)
        if enemy_hitbox.colliderect(bullet.rect):
            self.__health -= 1
            if self.__health == self.__max_health//2:
                self.__frames = self.__fly_frames
                self.__speed = 4
            return True

    def check_alive(self):
        if self.__health > 0:
            return True
        return False

    def hit_player(self, player):
        if self.check_alive():
            current_time = pg.time.get_ticks()
            enemy_hitbox = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)
            player_hitbox = player.rect.inflate(-player.rect.width * 0.7, -player.rect.height * 0.7)
            if enemy_hitbox.colliderect(player_hitbox):
                self.__atk_state = True
                if current_time - self.last_attack_time > self.__atk_speed:
                    if enemy_hitbox.colliderect(player_hitbox):
                        print("hit")
                        player.health -= self.__damage
                    self.last_attack_time = current_time
                    self.__move_state = False
                    return True
            self.__move_state = True
            return False

    def draw(self, screen, camera):
        if self.check_alive():
            bar_x = camera.apply(self).centerx - self.health_bar.width // 2
            bar_y = camera.apply(self).top
            self.health_bar.draw(screen, self.__health, bar_x, bar_y)
            if self.__atk_state:
                self.__atk_animation(screen, camera)
            else:
                screen.blit(self.image, camera.apply(self))
        elif not self.already_dead:
            self.__dead_animation(screen, camera)

    def get_size(self):
        return self.image.get_size()

    # def collide_other(self, others):
    #     for other in others:
    #         if other != self:
    #             if self.rect.colliderect(other.rect):
    #                 return True
    #     return False

