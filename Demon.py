import pygame as pg
from background import Background as Bgd
from bullet import DemonBullet, CthuluBullet
from UI import HealthBar
from Enemy import Enemy
from SoundManager import SoundManager


class Demon(Enemy):
    _cached_frames = None
    _atk_frames = []
    _dead_frames = []

    def __init__(self, x, y, health=100, damage=10, img="Game_Final_Project1/picture/enemy/Demon/FLYING.png", level=1,
                 bullets=None, camera=None):
        super().__init__(x, y, health=health, damage=damage, img=img)
        self.gold_drop = 100
        self.score = 35
        self.__atk_frames_index = 0
        self.__dead_frames_index = 0
        self.__dead_frames_speed = 100
        if Demon._cached_frames is None:
            Demon._cached_frames = self._load_frames(4, 1)

        self.__frames = Demon._cached_frames
        self.__atk_frames = Demon._atk_frames
        self.__dead_frames = Demon._dead_frames
        self.__last_update = 0
        self.__frame_speed = 150
        self.__frame_index = 0
        self.__left_right = "RIGHT"
        self.image = self.__frames[self.__frame_index]
        self.bullets = bullets
        self.__player_in_range = False
        self.__close_to_player = False
        self.__atk_state = False
        self.__move_state = True
        self.already_dead = False

        self.__atk_speed = 600
        self.__atk_frame_speed = self.__atk_speed // 8
        self.health = health
        self.__camera = camera
        self.__speed = 4
        self.__damage = damage
        self.__direction = pg.math.Vector2()
        self.__velocity = pg.math.Vector2()
        self.__max_health = health
        self.health_bar = HealthBar(self.rect.x, self.rect.y, self.image.get_size()[0] // 1.2, 15, self.__max_health)
        self.last_attack_time = 0
        self.__position = pg.math.Vector2(x, y)
        self.__current_level = level
        self.__border = Bgd.get(self.__current_level, 'border')

    def _load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        w, h = frame_width * 2, frame_height * 2
        frames = []
        """load walk animation"""
        walk_sheet = pg.image.load("Game_Final_Project1/picture/enemy/Demon/FLYING.png")
        for i in range(4):
            frame = pg.transform.scale(
                walk_sheet.subsurface(pg.Rect(i * frame_width, 0 * frame_height, frame_width, frame_height)), (w, h))
            frames.append(frame)
        """load range attack animation"""
        atk_sheet = pg.image.load("Game_Final_Project1/picture/enemy/Demon/ATTACK.png")
        for i in range(8):
            atk_frame = pg.transform.scale(
                atk_sheet.subsurface(pg.Rect(i * frame_width, 0 * frame_height, frame_width, frame_height)), (w, h))
            Demon._atk_frames.append(atk_frame)
        """load dead animation"""
        dead_sheet = pg.image.load("Game_Final_Project1/picture/enemy/Demon/DEATH.png")
        for i in range(6):
            dead_frame = pg.transform.scale(
                dead_sheet.subsurface(pg.Rect(i * frame_width, 0 * frame_height, frame_width, frame_height)), (w, h))
            Demon._dead_frames.append(dead_frame)
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

            self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames)
            if self.__atk_state:
                if self.__left_right == "LEFT":
                    self.image = self.__atk_frames[self.__atk_frames_index]
                else:
                    self.image = pg.transform.flip(self.__atk_frames[self.__atk_frames_index], True, False)

            if self.__atk_frames_index == len(self.__atk_frames) - 1:
                self.__attack_animation_set = 2
                self.__atk_frames_index = -1
                self.__move_state = True
        screen.blit(self.image, camera.apply(self))

    def move(self, player, enemies):
        if self.check_alive():
            enemy_hitbox = self.rect.inflate(-self.rect.width * 0.7, -self.rect.height * 0.7)
            player_hitbox = player.rect.inflate(-player.rect.width * 0.7, -player.rect.height * 0.7)

            if not enemy_hitbox.colliderect(player_hitbox):
                if self.__move_state or self.__close_to_player:
                    self.__atk_state = False
                    if player.rect.x > self.rect.center[0]:
                        self.__left_right = "RIGHT"
                    else:
                        self.__left_right = "LEFT"
                    # self.last_move_rect = self.rect.copy()
                    self._walk_animation()
                    player_vector = pg.math.Vector2(player.rect.center)
                    enemy_vector = pg.math.Vector2(self.rect.center)
                    distance = enemy_vector.distance_to(player_vector)

                    if distance > 470:
                        self.__direction = (player_vector - enemy_vector).normalize()
                        self.__player_in_range = False
                        self.__close_to_player = False
                    elif (distance < 450 and (self.__border['LEFT']+5 <= self.rect.x <= self.__border['RIGHT']-5) and
                          (self.__border['UP']+5 <= self.rect.y <= self.__border['DOWN']-5)):
                        self.__direction = (-player_vector + enemy_vector).normalize()
                        self.__close_to_player = True
                    else:
                        self.__direction = pg.math.Vector2()
                        self.__player_in_range = True
                        self.__close_to_player = False
                    self._avoid_others(enemies)
                    self.__position += self.__direction * self.__speed

                    self.rect.topleft = (int(self.__position.x), int(self.__position.y))

    def _avoid_others(self, enemies):
        avoid_vector = pg.math.Vector2(0, 0)
        for other_enemy in enemies:
            if isinstance(other_enemy, Demon):
                if other_enemy is not self and abs(self.__position.x - other_enemy.__position.x) < 100:
                    distance = self.__position.distance_to(other_enemy.__position)
                    if distance < 50:
                        avoid_vector += (self.__position - other_enemy.__position).normalize()

        if avoid_vector.length() > 0:
            self.__direction += avoid_vector.normalize() * 0.5

    def get_damage(self, bullet, damage):
        enemy_hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)
        if enemy_hitbox.colliderect(bullet.rect):
            self.health -= damage
            if self.health <= 0 and not self.already_dead:
                SoundManager.get_instance().play_sound("Dead")
            return True

    def check_alive(self):
        if self.health > 0:
            return True
        return False

    def hit_player(self, player, bullets, camera):
        if self.check_alive():
            current_time = pg.time.get_ticks()
            if self.__player_in_range:
                self.__atk_state = True
                if current_time - self.last_attack_time > self.__atk_speed:
                    bullet = DemonBullet(self.rect.centerx, self.rect.centery, player, (20, 20), damage=self.__damage)
                    bullets.append(bullet)
                    camera.add(bullet)
                    SoundManager.get_instance().play_sound("DemonShoot")
                    self.last_attack_time = current_time
                    self.__move_state = False
                    return False
            self.__move_state = True
            return False

    def draw(self, screen, camera):
        if self.check_alive():
            bar_x = camera.apply(self).centerx - self.health_bar.width // 2
            bar_y = camera.apply(self).top-20
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


