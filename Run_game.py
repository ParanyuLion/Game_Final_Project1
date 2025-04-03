import pygame as pg
from Enemy import Enemy
from Player import Player
from background import Background as Bgd
from game_config import Config
from bullet import Bullet
from Effects import Explosion, DashEffect, FireBreatheEffect
from UI import HealthBar
from Slime import Slime
from Minotaur import Minotaur
from Cthulu import Cthulu
from Magic import FireBreath
from Shop import Shop
import random


class Camera(pg.sprite.Group):
    def __init__(self, width, height):
        super().__init__()
        self.camera_rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target):
        x = target.rect.centerx - Config.get('WIN_WIDTH') // 2
        y = target.rect.centery - Config.get('WIN_HEIGHT') // 2
        self.camera_rect.topleft = (x, y)


class RunGame:
    def __init__(self):
        """set up game"""
        pg.init()
        pg.display.set_caption('Game')
        self.__screen = pg.display.set_mode((Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT')))
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__start_game = False
        self.__running = True

        """background attribute"""
        self.level_name = 'MainMenu'
        self.__background = Bgd.load_menu(self.level_name)
        self.bg_width, self.bg_height = self.__background.get_size()
        self.__border = Bgd.get(self.level_name, 'border')
        self.__level = 0
        self.__complete_level = False
        """entities attribute"""
        spawn_point = Bgd.get(1, 'spawn')

        self.player = Player(spawn_point[0], spawn_point[1])
        self.FireBreath = FireBreath(self.player.rect.x, self.player.rect.y)
        self.bullets = []
        self.bullet_size = (20, 20)
        self.enemies = []
        self.effects = []
        self.health_bar = HealthBar(20, 20, 300, 35, self.player.health)
        self.camera = Camera(Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT'))
        self.camera.add(self.player, *self.enemies, *self.bullets, *self.effects, self.FireBreath)
        self.player.draw(self.__screen, self.camera)
        self.__last_shot_time = 0
        self.__dash_time = 0
        self.__at_door = False
        self.__dash = False
        self.__before_dash_pos = self.player.rect
        # self.count = 0
        dash_effect = DashEffect(self.player.rect.centerx, self.player.rect.centery)
        self.effects.append(dash_effect)
        self.camera.add(dash_effect)
        self.shop = Shop(self.player)

    def main_menu(self):
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.__background, (0, 0))
        text = pg.image.load("Game_Final_Project1/picture/background/start_game_text.png")
        text.set_colorkey((0, 0, 0))
        self.__screen.blit(text, (0, 0))
        # font_size = 50
        # font = pg.font.SysFont('comicsansms', font_size, bold=True)
        # text = font.render(f"Press to Start", True, (255, 255, 255))
        # text_rect = text.get_rect(center=(Config.get('WIN_WIDTH') // 2, Config.get('WIN_HEIGHT') // 2))
        # self.__screen.blit(text, text_rect)

    def update_all(self):
        self.camera.update(self.player)
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background, (-self.camera.camera_rect.x, -self.camera.camera_rect.y))
        # self.player.draw(self.__screen, self.camera)
        finish_effect = []
        if self.level_name == 'shop':
            self.__screen.blit(self.__background, (0,0))
            self.shop.draw(self.__screen)
            self.health_bar.draw(self.__screen, self.player.health)
            return None
        for entity in self.camera:
            if isinstance(entity, DashEffect):
                if self.__dash:
                    entity.rect = self.__before_dash_pos
                    entity.finish = False
                    self.__dash = False
            elif isinstance(entity, Explosion) or isinstance(entity, FireBreatheEffect):
                if entity.finish:
                    finish_effect.append(entity)
            entity.draw(self.__screen, self.camera)
        self.FireBreath.draw(self.__screen, self.camera)
        # delete this loop if game is lag
        for entity in self.camera:
            if isinstance(entity, (Explosion, DashEffect, FireBreatheEffect)):
                entity.draw(self.__screen, self.camera)

        remove_set = set(finish_effect)
        self.enemies = [b for b in self.enemies if b not in remove_set]
        for effect in finish_effect:
            self.effects.remove(effect)
            self.camera.remove(effect)

        self.health_bar.draw(self.__screen, self.player.health)
        # self.camera.draw(self.__screen)


    def entities_events(self):
        """players event"""
        self.__at_door = self.player.door_collision(Bgd.get(self.level_name, 'door'))

        """"bullets event"""
        remove_bullets = []
        for bullet in self.bullets:
            # check that bullets not go out of border
            if (self.__border["RIGHT"] + self.bullet_size[0] * 2.5 > bullet.rect.centerx > self.__border["LEFT"] and
                    self.__border["DOWN"] + self.bullet_size[1] * 3.5 > bullet.rect.centery > self.__border["UP"]):
                bullet.update()
                for enemy in self.enemies:
                    if enemy.check_alive() and enemy.get_damage(bullet, self.player.damage):
                        # if bullet in self.bullets:
                        explosion = Explosion(bullet.rect.x, bullet.rect.y)
                        self.effects.append(explosion)
                        self.camera.add(explosion)
                        remove_bullets.append(bullet)
            else:
                remove_bullets.append(bullet)
        remove_set = set(remove_bullets)
        self.bullets = [b for b in self.bullets if b not in remove_set]
        for bullet in remove_bullets:
            self.camera.remove(bullet)

        """enemies event"""
        self.FireBreath.hit_enemy(self.enemies, self.effects, self.camera)
        dead_enemies = []
        for enemy in self.enemies:
            enemy.move(self.player, self.enemies)
            if enemy.hit_player(self.player):
                pass
            if enemy.already_dead:
                dead_enemies.append(enemy)
        remove_set = set(dead_enemies)
        self.enemies = [b for b in self.enemies if b not in remove_set]
        for enemy in dead_enemies:
            self.player.gold += enemy.gold_drop
            self.camera.remove(enemy)
            enemy.kill()
        if len(self.enemies) == 0:
            self.__complete_level = True
        else:
            self.__complete_level = False

    def random_spawn(self):
        spawn = Bgd.get(self.level_name, 'enemy_spawn')
        spawn_x = spawn['x']
        spawn_y = spawn['y']
        return random.randint(spawn_x[0], spawn_x[1]), random.randint(spawn_y[0], spawn_y[1])

    def set_level(self, name):
        self.__background = Bgd.load_bg(name)
        self.__border = Bgd.get(name, 'border')
        self.player.rect.center = Bgd.get(name, 'spawn')

    def load_level(self, level):
        self.enemies.clear()
        if level == 'shop':
            self.level_name = 'shop'
            self.set_level(self.level_name)
        elif level == 1:
            self.level_name = 1
            for i in range(1):
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Cthulu(spawn_x, spawn_y, health=30)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif level == 2:
            self.level_name = 2
            for i in range(2):
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Minotaur(spawn_x, spawn_y, health=5)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif level == 3:
            self.level_name = 3
            for i in range(3):
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Minotaur(spawn_x, spawn_y, health=5)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif level == 4:
            self.level_name = 4
            for i in range(4):
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Slime(spawn_x, spawn_y, health=5)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        else:
            self.level_name = 2
            for i in range(self.__level):
                self.enemies.append(Slime(x=random.randint(0, 1000), y=random.randint(0, 620), health=5))
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

    def run_loop(self):
        clock = pg.time.Clock()
        while self.__running:
            start_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                if event.type == pg.KEYDOWN:
                    # pause game
                    # if event.key == pg.K_ESCAPE:
                    #     self.__start_game = False
                    now = pg.time.get_ticks()
                    if event.key == pg.K_SPACE and now - self.__dash_time > self.player.dash_cooldown and self.level_name != 'shop':
                        self.__before_dash_pos = self.player.rect.copy()
                        self.player.dash(self.__border)
                        self.__dash = True
                        self.__dash_time = now
                    if event.key == pg.K_e:
                        if self.level_name == 'shop':
                            self.__level += 1
                            self.load_level(self.__level)
                            self.shop.toggle_shop()
                        elif self.__complete_level and self.__at_door:
                            self.load_level('shop')
                            self.shop.toggle_shop()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT and self.__start_game:
                        now = pg.time.get_ticks()
                        if now - self.__last_shot_time > self.player.atk_speed * 4:
                            mouse_pos = pg.mouse.get_pos()
                            mouse_pos_world = (mouse_pos[0] + self.camera.camera_rect.x,
                                               mouse_pos[1] + self.camera.camera_rect.y)
                            if mouse_pos_world[0] < self.player.rect.x:
                                self.player.set_left_right("LEFT")
                            else:
                                self.player.set_left_right("RIGHT")
                            self.player.attack()
                            new_bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, mouse_pos_world,
                                                self.bullet_size)
                            self.bullets.append(new_bullet)
                            self.__last_shot_time = now
                            self.camera.add(new_bullet, *self.bullets)
                    elif event.button == pg.BUTTON_LEFT and not self.__start_game:
                        self.__level += 1
                        self.__start_game = True
                        self.load_level(self.__level)
                    if self.level_name == 'shop':
                        self.shop.handle_event(event)
            if self.__start_game:
                self.update_all()
                self.entities_events()
                key = pg.key.get_pressed()
                # print(self.player.player_rect.y, self.player.player_rect.x)
                if self.level_name != 'shop':
                    if key[pg.K_w] and self.player.wall_collision("UP", self.__border["UP"]):
                        self.player.move("UP")
                    if key[pg.K_s] and self.player.wall_collision("DOWN", self.__border["DOWN"]):
                        self.player.move("DOWN")
                    if key[pg.K_a] and self.player.wall_collision("LEFT", self.__border["LEFT"]):
                        self.player.move("LEFT")
                    if key[pg.K_d] and self.player.wall_collision("RIGHT", self.__border["RIGHT"]):
                        self.player.move("RIGHT")
                    if key[pg.K_q] and self.player.unlock_fire_breathe:
                        self.FireBreath.activate = True
                        self.FireBreath.set_position(self.player.rect, self.player.left_right)
                    else:
                        self.FireBreath.activate = False
            else:
                self.main_menu()

            pg.display.flip()
            clock.tick(Config.get('FPS'))
            end_time = pg.time.get_ticks()
            if end_time - start_time > 17:
                print(f"Frame time: {end_time - start_time} ms")

    pg.quit()


play = RunGame()
play.run_loop()
