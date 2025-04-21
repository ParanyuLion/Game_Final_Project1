import pygame as pg
from UI import HealthBar
from bullet import CthuluBullet
from Enemy import Enemy
from SoundManager import SoundManager


class Cthulu(Enemy):
    _cached_frames = None
    _atk_frames1_left = []
    _atk_frames1_right = []
    _atk_frames2_left = []
    _atk_frames2_right = []
    _dead_frames = []
    _fly_frames = []

    def __init__(self, x, y, health=100, damage=20, img="Game_Final_Project1/picture/enemy/cthulu_SpriteSheet.png"):
        super().__init__(x, y, health=health, damage=damage, img=img)
        self.gold_drop = 500
        self.score = 100
        # self.__atk_frames1 = []
        # self.__atk_frames2 = []
        # self.__fly_frames = []
        self.__atk_frames_index = 0
        self.__attack_animation_set = 1
        # self.__dead_frames = []
        self.__dead_frames_index = 0
        self.__dead_frames_speed = 100
        if Cthulu._cached_frames is None:
            Cthulu._cached_frames = self._load_frames(15, 7)

        self.__frames = Cthulu._cached_frames
        self.__atk_frames1_left = Cthulu._atk_frames1_left
        self.__atk_frames1_right = Cthulu._atk_frames1_right
        self.__atk_frames2_left = Cthulu._atk_frames2_left
        self.__atk_frames2_right = Cthulu._atk_frames2_right
        self.__dead_frames = Cthulu._dead_frames
        self.__fly_frames = Cthulu._fly_frames
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
        self.health = health
        self.__range_atk_count = 0
        self.__range_atk_cooldown = 2500
        self.__last_range_atk = 0

        self.__speed = 2
        self.__damage = damage
        self.__range_damage = int(self.__damage / 1.5)
        self.__direction = pg.math.Vector2()
        self.__velocity = pg.math.Vector2()
        self.__max_health = health
        self.health_bar = HealthBar(self.rect.x, self.rect.y, self.image.get_size()[0] // 2, 15, self.__max_health)
        # self.last_move_rect = self.rect.copy()
        self.last_attack_time = 0
        self.__position = pg.math.Vector2(x, y)
        self.__player_in_range = False
        self.__distance = 0

    def _load_frames(self, num_frames, num_movement):
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
            Cthulu._fly_frames.append(frame)
        """load melee attack animation"""
        for i in range(9):  # melee attack
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 4 * frame_height, frame_width, frame_height)), (w, h))
            Cthulu._atk_frames1_left.append(frame)
            Cthulu._atk_frames1_right.append(pg.transform.flip(frame, True, False))

        """load range attack animation"""
        for i in range(7):  # range attack
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 3 * frame_height, frame_width, frame_height)), (w, h))
            Cthulu._atk_frames2_left.append(frame)
            Cthulu._atk_frames2_right.append(pg.transform.flip(frame, True, False))
        """load dead animation"""
        for i in range(11):
            dead_frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 6 * frame_height, frame_width, frame_height)), (w, h))
            Cthulu._dead_frames.append(dead_frame)
        return frames

    def _dead_animation(self, screen, camera):
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

    def _walk_animation(self):
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

    def _atk_animation(self, screen, camera):
        self.__move_state = False
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__atk_frame_speed:
            # print(self.rect.center)
            self.__last_update = now
            if self.__attack_animation_set == 1:

                self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames1_left)
                if self.__atk_state:
                    if self.__left_right == "LEFT":
                        self.image = self.__atk_frames1_left[self.__atk_frames_index]
                    else:
                        self.image = self.__atk_frames1_right[self.__atk_frames_index]
                if self.__atk_frames_index == len(self.__atk_frames1_left) - 1:
                    # self.__attack_animation_set = 2
                    self.__atk_frames_index = 0
                    self.__move_state = True
            else:

                self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames2_left)
                if self.__atk_state:
                    if self.__left_right == "LEFT":
                        self.image = self.__atk_frames2_left[self.__atk_frames_index]
                    else:
                        self.image = self.__atk_frames2_right[self.__atk_frames_index]
                if self.__atk_frames_index == len(self.__atk_frames2_left) - 1:
                    # self.__attack_animation_set = 2
                    self.__atk_frames_index = 0
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
                    self._walk_animation()
                    player_vector = pg.math.Vector2(player.rect.center)
                    enemy_vector = pg.math.Vector2(self.rect.center)
                    self.__distance = enemy_vector.distance_to(player_vector)

                    if self.__distance > 0:
                        self.__direction = (player_vector - enemy_vector).normalize()
                    else:
                        self.__direction = pg.math.Vector2()
                    self._avoid_others(enemies)
                    self.__position += self.__direction * self.__speed

                    self.rect.topleft = (int(self.__position.x), int(self.__position.y))

    def _avoid_others(self, enemies):
        avoid_vector = pg.math.Vector2(0, 0)
        for other_enemy in enemies:
            if isinstance(other_enemy, Cthulu):
                if other_enemy is not self and abs(self.__position.x - other_enemy.__position.x) < 100:
                    distance = self.__position.distance_to(other_enemy.__position)
                    if distance < 50:
                        avoid_vector += (self.__position - other_enemy.__position).normalize()

        if avoid_vector.length() > 0:
            self.__direction += avoid_vector.normalize() * 0.5

    def get_damage(self, bullet, damage):
        enemy_hitbox = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.5)
        if enemy_hitbox.colliderect(bullet.rect):
            self.health -= damage
            if self.health <= 0 and not self.already_dead:
                SoundManager.get_instance().play_sound("Dead")
            if self.health <= self.__max_health // 2 and self.__frames != self.__fly_frames:
                SoundManager.get_instance().play_sound("CthuluChangePhase")
                self.__frames = self.__fly_frames
                self.__speed = 8
            return True

    def check_alive(self):
        if self.health > 0:
            return True
        return False

    def __atk_algorithm(self, player):

        now = pg.time.get_ticks()
        if player.drink_state:
            self.__attack_animation_set = 2
            return None
        if self.__distance < 250:
            self.__attack_animation_set = 1
            return None
        if now - self.__last_range_atk > self.__range_atk_cooldown:
            if self.__range_atk_count >= 3:
                self.__last_range_atk = now
                self.__range_atk_count = 0
                self.__attack_animation_set = 1
            else:
                self.__attack_animation_set = 2

        else:
            self.__attack_animation_set = 1

    def hit_player(self, player, bullets, camera):
        if self.check_alive():
            self.__atk_algorithm(player)
            if self.__attack_animation_set == 1:
                current_time = pg.time.get_ticks()
                enemy_hitbox = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)
                player_hitbox = player.rect.inflate(-player.rect.width * 0.7, -player.rect.height * 0.7)
                if enemy_hitbox.colliderect(player_hitbox):
                    self.__atk_state = True
                    if current_time - self.last_attack_time > self.__atk_speed:
                        SoundManager.get_instance().play_sound("CthuluAtk")
                        player.health -= self.__damage
                        self.last_attack_time = current_time
                        self.__move_state = False
                        return False
                self.__move_state = True
                return False
            else:
                current_time = pg.time.get_ticks()
                self.__atk_state = True
                if current_time - self.last_attack_time > self.__atk_speed:
                    bullet = CthuluBullet(self.rect.centerx, self.rect.centery, player, (4, 4), damage=self.__range_damage)
                    bullets.append(bullet)
                    camera.add(bullet)
                    SoundManager.get_instance().play_sound("CthuluShoot")
                    self.last_attack_time = current_time
                    self.__move_state = False
                    self.__range_atk_count += 1
                    return False



    def draw(self, screen, camera):
        if self.check_alive():
            bar_x = camera.apply(self).centerx - self.health_bar.width // 2
            bar_y = camera.apply(self).top
            self.health_bar.draw(screen, self.health, bar_x, bar_y)
            if self.__atk_state:
                self._atk_animation(screen, camera)
            else:
                screen.blit(self.image, camera.apply(self))
        elif not self.already_dead:
            self._dead_animation(screen, camera)
        # pg.draw.rect(screen, (0, 255, 0), camera.apply(self), 2)

    def get_size(self):
        return self.image.get_size()

    # def collide_other(self, others):
    #     for other in others:
    #         if other != self:
    #             if self.rect.colliderect(other.rect):
    #                 return True
    #     return False

