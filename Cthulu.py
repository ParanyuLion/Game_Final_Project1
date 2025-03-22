import pygame as pg
from UI import HealthBar
from entity import Entity


class Boss(Entity):
    def __init__(self, x, y, health=100, damage=20, img="Game_Final_Project1/picture/cthulu_SpriteSheet.png"):
        super().__init__(img,x,y)
        self.__atk_frames = []
        self.__atk_frames_index = 0
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

        self.__atk_speed = 500
        self.__atk_frame_speed = self.__atk_speed // 8
        self.__health = health

        self.__speed = 2
        self.__damage = damage
        self.__direction = pg.math.Vector2()
        self.__velocity = pg.math.Vector2()
        self.health_bar = HealthBar(self.rect.x, self.rect.y, 100, 15, self.__health)
        # self.last_move_rect = self.rect.copy()
        self.last_attack_time = 0
        self.__position = pg.math.Vector2(x, y)

    def __load_frames(self, num_frames, num_movement):
        sheet_width, sheet_height = self.image.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height // num_movement
        w,h = frame_width*3, frame_height*3

        frames = []
        """load walk animation"""
        for i in range(6):
            frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 2 * frame_height, frame_width, frame_height)), (w,h))
            frames.append(frame)
        """load attack animation"""
        for i in range(9):
            atk_frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 4 * frame_height, frame_width, frame_height)), (w,h))
            self.__atk_frames.append(atk_frame)
        """load dead animation"""
        for i in range(6):
            dead_frame = pg.transform.scale(
                self.image.subsurface(pg.Rect(i * frame_width, 1 * frame_height, frame_width, frame_height)), (w,h))
            self.__dead_frames.append(dead_frame)
        return frames

    def __dead_animation(self,screen, camera):
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__dead_frames_speed:
            if self.__dead_frames_index == 4:
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
        now = pg.time.get_ticks()
        if now - self.__last_update > self.__atk_frame_speed:
            self.__last_update = now
            self.__atk_frames_index = (self.__atk_frames_index + 1) % len(self.__atk_frames)

            if self.__atk_state:
                if self.__left_right == "LEFT":
                    self.image = self.__atk_frames[self.__atk_frames_index]
                else:
                    self.image = pg.transform.flip(self.__atk_frames[self.__atk_frames_index], True, False)
                # print("atk", self.__atk_frames_index)
        screen.blit(self.image, camera.apply(self))

    def move(self, player, enemies):
        if self.check_alive():
            player_hitbox = player.rect.inflate(-player.rect.width * 1, -player.rect.height * 1)
            if not self.rect.colliderect(player_hitbox):
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
        if self.rect.colliderect(bullet.rect):
            self.__health -= 1
            return True

    def check_alive(self):
        if self.__health > 0:
            return True
        return False

    def hit_player(self, player):
        if self.check_alive():
            current_time = pg.time.get_ticks()
            player_hitbox = player.rect.inflate(-player.rect.width * 0.7, -player.rect.height * 0.7)
            if self.rect.colliderect(player_hitbox):
                self.__atk_state = True

                if current_time - self.last_attack_time > self.__atk_speed:
                    player.health -= self.__damage
                    self.last_attack_time = current_time
                    self.__move_state = False
                    return True
            self.__move_state = True
            return False

    def draw(self, screen, camera):
        if self.check_alive():
            bar_x, bar_y = camera.apply(self).topleft
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

