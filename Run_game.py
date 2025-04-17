import pygame as pg
import random
from Enemy import Enemy
from Player import Player
from background import Background as Bgd
from game_config import Config
from SoundManager import SoundManager
from bullet import Bullet, DemonBullet, CthuluBullet
from Effects import Explosion, DashEffect, FireBreatheEffect, CthuluExplosion
from UI import HealthBar, ManaBar, Inventory, InteractUI, Gold
from Shop import Shop
from Magic import FireBreath, ThunderStrike

from Slime import Slime
from Minotaur import Minotaur
from Cthulu import Cthulu
from Demon import Demon


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
        self.__game_state = "menu"
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

        self.health_bar = HealthBar(20, 20, 450, 35, self.player.health)
        self.mana_bar = ManaBar(20, 63, 450, 35, self.player.mana)
        self.inventory = Inventory(500, 580, self.player, self.FireBreath)
        self.shop = Shop(self.player)
        self.shop.on_next_level_clicked = self.go_to_next_level
        self.show_gold = Gold(70, 130, self.player)
        self.camera = Camera(Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT'))
        self.camera.add(self.player, *self.enemies, *self.bullets, *self.effects, self.FireBreath)
        self.player.draw(self.__screen, self.camera)
        self.__dash_time = 0
        self.__at_door = False
        self.__dash = False
        self.__before_dash_pos = self.player.rect
        # self.count = 0
        dash_effect = DashEffect(self.player.rect.centerx, self.player.rect.centery)
        self.effects.append(dash_effect)
        self.camera.add(dash_effect)
        self.__restart_button = pg.Rect(Config.get('WIN_WIDTH') // 2 - 125, Config.get('WIN_HEIGHT') // 2 + 40, 250, 80)
        SoundManager.get_instance().play_music("bgm")

        """settings attribute"""
        self.__effect_plus = pg.Rect(850, 250, 40, 40)
        self.__effect_minus = pg.Rect(800, 250, 40, 40)
        self.__music_plus = pg.Rect(850, 350, 40, 40)
        self.__music_minus = pg.Rect(800, 350, 40, 40)
        self.__gear_img = pg.transform.scale(pg.image.load("Game_Final_Project1/picture/gear.jpg"), (60, 60))
        self.__gear_button = self.__gear_img.get_rect(topleft=(Config.get('WIN_WIDTH') - 80, 20))
        self.__back_button = pg.Rect(500, 450, 150, 50)

    def settings_menu(self):
        self.__screen.fill((30, 30, 30))
        font = pg.font.SysFont("calibri", 40, bold=True)
        title = font.render("Settings", True, (255, 255, 255))
        self.__screen.blit(title, (Config.get('WIN_WIDTH') // 2 - 80, 100))

        effect_text = font.render(f"Effects Volume: {int(SoundManager.get_instance().effect_volume * 100)}", True,
                                  (255, 255, 255))
        music_text = font.render(f"Music Volume: {int(SoundManager.get_instance().music_volume * 100)}", True,
                                 (255, 255, 255))
        plus = font.render("+", True,(255, 255, 255))
        minus = font.render("-", True, (255, 255, 255))
        self.__screen.blit(effect_text, (400, 250))
        self.__screen.blit(music_text, (400, 350))

        pg.draw.rect(self.__screen, (100, 100, 255), self.__effect_plus)
        pg.draw.rect(self.__screen, (100, 100, 255), self.__effect_minus)
        pg.draw.rect(self.__screen, (100, 255, 100), self.__music_plus)
        pg.draw.rect(self.__screen, (100, 255, 100), self.__music_minus)
        pg.draw.rect(self.__screen, (180, 0, 0), self.__back_button)

        self.__screen.blit(plus, (self.__effect_plus.x + 5, self.__effect_plus.y + 5))
        self.__screen.blit(plus, (self.__effect_plus.x + 5, self.__music_plus.y + 5))
        self.__screen.blit(minus, (self.__effect_minus.x + 5, self.__effect_minus.y + 5))
        self.__screen.blit(minus, (self.__effect_minus.x + 5, self.__music_minus.y + 5))

        back_text = font.render("BACK", True, (255, 255, 255))
        self.__screen.blit(back_text, (self.__back_button.x + 10, self.__back_button.y + 5))

    def main_menu(self):
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.__background, (0, 0))
        text = pg.image.load("Game_Final_Project1/picture/background/start_game_text.png")
        text.set_colorkey((0, 0, 0))
        self.__screen.blit(text, (0, 0))
        self.__screen.blit(self.__gear_img, self.__gear_button)

    def game_over(self):
        self.__background = Bgd.load_menu('GameOver')
        self.__screen.blit(self.__background, (0, 0))
        pg.draw.rect(self.__screen, (44, 44, 44), self.__restart_button, border_radius=8)
        pg.draw.rect(self.__screen, (112, 112, 112), self.__restart_button, border_radius=8, width=5)

        subfont = pg.font.SysFont("calibri", 55, bold=True)
        restart_text = subfont.render("RESTART", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=self.__restart_button.center)
        self.__screen.blit(restart_text, restart_text_rect)

    def update_all(self):
        self.camera.update(self.player)
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background, (-self.camera.camera_rect.x, -self.camera.camera_rect.y))
        # self.player.draw(self.__screen, self.camera)

        finish_effect = []
        if self.level_name == 'shop':
            self.__screen.blit(self.__background, (0, 0))
            self.shop.draw(self.__screen)
            self.health_bar.draw(self.__screen, self.player.health)
            self.mana_bar.draw(self.__screen, self.player.mana)
            self.show_gold.draw(self.__screen, 160, 130)
            return None
        for bullet in self.bullets:
            bullet.draw(self.__screen, self.camera)
        self.player.draw(self.__screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.__screen, self.camera)
        self.FireBreath.draw(self.__screen, self.camera)
        # delete this loop if game is lag
        for effect in self.effects:
            if isinstance(effect, DashEffect):
                if self.__dash:
                    effect.rect = self.__before_dash_pos
                    effect.finish = False
                    self.__dash = False
            else:
                if effect.finish:
                    finish_effect.append(effect)
            effect.draw(self.__screen, self.camera)

        remove_set = set(finish_effect)
        self.enemies = [b for b in self.enemies if b not in remove_set]
        for effect in finish_effect:
            self.effects.remove(effect)
            self.camera.remove(effect)

        self.health_bar.draw(self.__screen, self.player.health)
        self.mana_bar.draw(self.__screen, self.player.mana)
        self.inventory.draw(self.__screen)
        self.show_gold.draw(self.__screen)

        if self.__complete_level and self.__at_door:
            InteractUI.draw_interact_door(self.__screen)
        # self.camera.draw(self.__screen)

    def entities_events(self):
        """players event"""
        self.__at_door = self.player.door_collision(Bgd.get(self.level_name, 'door'))
        if self.player.health <= 0:
            pg.mixer.music.stop()
            SoundManager.get_instance().play_music("game_over_music")
            SoundManager.get_instance().play_sound("game_over_sound")
            self.__game_state = "game_over"
        """"bullets event"""
        remove_bullets = []
        for bullet in self.bullets:
            # check that bullets not go out of border
            if (self.__border["RIGHT"] + self.bullet_size[0] * 2.5 > bullet.rect.centerx > self.__border["LEFT"] and
                    self.__border["DOWN"] + self.bullet_size[1] * 3.5 > bullet.rect.centery > self.__border["UP"]):
                bullet.update()
                if isinstance(bullet, DemonBullet):
                    if self.player.get_shoot(bullet):
                        SoundManager.get_instance().play_sound("DemonBulletHit")
                        explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                        self.effects.append(explosion)
                        self.camera.add(explosion)
                        remove_bullets.append(bullet)
                elif isinstance(bullet, CthuluBullet):
                    if self.player.get_shoot(bullet):
                        SoundManager.get_instance().play_sound("CthuluBulletHit")
                        explosion = CthuluExplosion(bullet.rect.centerx, bullet.rect.centery)
                        self.effects.append(explosion)
                        self.camera.add(explosion)
                        remove_bullets.append(bullet)
                else:
                    for enemy in self.enemies:
                        if enemy.check_alive() and enemy.get_damage(bullet, self.player.damage):
                            # if bullet in self.bullets:
                            SoundManager.get_instance().play_sound("PlayerBulletHit")
                            explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
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
        self.FireBreath.hit_enemy(self.enemies, self.player, self.effects, self.camera)

        dead_enemies = []
        for enemy in self.enemies:

            enemy.move(self.player, self.enemies)
            if isinstance(enemy, Demon) or isinstance(enemy, Cthulu):
                enemy.hit_player(self.player, bullets=self.bullets, camera=self.camera)
            elif enemy.hit_player(self.player):
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

    def restart_game(self):
        self.player.reset_game()
        self.shop.reset_game()
        # SoundManager.get_instance().play_music("bgm")
        SoundManager.get_instance().play_music("CthuluTheme")
        self.__level = 1
        self.load_level(self.__level)
        self.bullets.clear()
        self.effects.clear()
        dash_effect = DashEffect(self.player.rect.centerx, self.player.rect.centery)
        self.effects.append(dash_effect)
        self.camera.add(dash_effect)
        self.__complete_level = False
        self.__at_door = False
        self.__game_state = "playing"

    def set_level(self, name):
        self.__background = Bgd.load_bg(name)
        self.__border = Bgd.get(name, 'border')
        self.player.rect.center = Bgd.get(name, 'spawn')

    def go_to_next_level(self):
        self.__level += 1
        self.load_level(self.__level)
        self.shop.toggle_shop()
        SoundManager.get_instance().play_sound("DoorClose")

    def __level_generator(self, level):

        if level % 7 == 0:
            self.level_name = 4
            for i in range(1):
                # pg.mixer.music.stop()
                # SoundManager.get_instance().play_music("CthuluTheme")
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Cthulu(spawn_x, spawn_y, health=5*level)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif level % 5 == 0:
            self.level_name = 3
            for i in range(3):
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Demon(spawn_x, spawn_y, health=int(level*1.25), level=self.level_name)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        elif level % 3 == 0:
            self.level_name = 2
            for i in range(3):
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Minotaur(spawn_x, spawn_y, health=3*level)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

        else:
            self.level_name = 1
            for i in range(level):
                spawn_x, spawn_y = self.random_spawn()
                new_enemy = Slime(spawn_x, spawn_y, health=5+level)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.enemies.append(new_enemy)
            self.camera.add(*self.enemies)
            self.set_level(self.level_name)

    def load_level(self, level):
        self.enemies.clear()
        if level == 'shop':
            self.level_name = 'shop'
            self.set_level(self.level_name)
        else:
            self.__level_generator(level)

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
                    if event.key == pg.K_SPACE and self.player.use_skill('SPACE') and self.level_name != 'shop':
                        self.__before_dash_pos = self.player.rect.copy()
                        self.player.dash(self.__border)
                        self.__dash = True
                        self.__dash_time = now
                    if event.key == pg.K_e:
                        if self.level_name == 'shop':
                            SoundManager.get_instance().play_sound("DoorOpen")
                            self.__level += 1
                            self.load_level(self.__level)
                            self.shop.toggle_shop()
                        elif self.__complete_level and self.__at_door:
                            SoundManager.get_instance().play_sound("DoorClose")
                            self.load_level('shop')
                            self.shop.toggle_shop()
                    if event.key == pg.K_1 and self.player.use_skill('1'):
                        self.player.drink_potion('health_potion')
                    if event.key == pg.K_2 and self.player.use_skill('2'):
                        self.player.drink_potion('mana_potion')
                    if (event.key == pg.K_r and self.player.unlock_thunder_strike and self.player.use_skill("R")
                            and ThunderStrike.check_mana(self.player.mana)):
                        ThunderStrike.hit_enemy(self.enemies, self.player, self.effects, self.camera)

                if event.type == pg.MOUSEBUTTONDOWN:
                    """Shooting Bullet"""
                    if event.button == pg.BUTTON_LEFT and self.__game_state == "playing":
                        now = pg.time.get_ticks()
                        if self.player.use_skill("CLICK") and not self.player.drink_state and self.level_name != 'shop':
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
                    elif event.button == pg.BUTTON_LEFT and self.__game_state == "menu":
                        if self.__gear_button.collidepoint(event.pos):
                            self.__game_state = "settings"
                        else:
                            SoundManager.get_instance().play_sound("Hover")
                            self.restart_game()
                    elif event.button == pg.BUTTON_LEFT and self.__game_state == "game_over":
                        if self.__restart_button.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            self.restart_game()
                    elif self.__game_state == "settings":
                        if self.__effect_plus.collidepoint(event.pos):
                            SoundManager.get_instance().set_effect_volume(
                                min(1.0, SoundManager.get_instance().effect_volume + 0.1))
                        elif self.__effect_minus.collidepoint(event.pos):
                            SoundManager.get_instance().set_effect_volume(
                                max(0.0, SoundManager.get_instance().effect_volume - 0.1))
                        elif self.__music_plus.collidepoint(event.pos):
                            SoundManager.get_instance().set_music_volume(
                                min(1.0, SoundManager.get_instance().music_volume + 0.1))
                        elif self.__music_minus.collidepoint(event.pos):
                            SoundManager.get_instance().set_music_volume(
                                max(0.0, SoundManager.get_instance().music_volume - 0.1))
                        elif self.__back_button.collidepoint(event.pos):
                            self.__game_state = "menu"
                            self.__game_state = "menu"
                    if self.level_name == 'shop':
                        self.shop.handle_event(event)
            """game state"""
            if self.__game_state == "playing":
                self.update_all()
                self.entities_events()
                key = pg.key.get_pressed()
                # print(self.player.player_rect.y, self.player.player_rect.x)
                if self.level_name != 'shop' and not self.player.drink_state:
                    if key[pg.K_w] and self.player.wall_collision("UP", self.__border["UP"]):
                        self.player.move("UP")
                    if key[pg.K_s] and self.player.wall_collision("DOWN", self.__border["DOWN"]):
                        self.player.move("DOWN")
                    if key[pg.K_a] and self.player.wall_collision("LEFT", self.__border["LEFT"]):
                        self.player.move("LEFT")
                    if key[pg.K_d] and self.player.wall_collision("RIGHT", self.__border["RIGHT"]):
                        self.player.move("RIGHT")

                    if key[pg.K_q] and self.player.unlock_fire_breathe and self.FireBreath.check_mana(self.player.mana):
                        self.FireBreath.activate = True
                        self.FireBreath.set_position(self.player.rect, self.player.left_right)
                    else:
                        self.FireBreath.activate = False
            elif self.__game_state == "menu":
                self.main_menu()
            elif self.__game_state == "game_over":
                self.game_over()
            elif self.__game_state == "settings":
                self.settings_menu()

            pg.display.flip()
            clock.tick(Config.get('FPS'))
            fps = clock.get_fps()
            print(f"FPS: {fps:.2f}")

    pg.quit()


play = RunGame()
play.run_loop()
