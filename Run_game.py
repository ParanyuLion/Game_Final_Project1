import pygame as pg
import random
from Player import Player
from Camera import Camera
from background import Background as Bgd
from game_config import Config
from SoundManager import SoundManager
from bullet import Bullet, DemonBullet, CthuluBullet
from Effects import Explosion, DashEffect, CthuluExplosion
from UI import HealthBar, ManaBar, Inventory, InteractUI, Gold, Score
from Shop import Shop
from Magic import FireBreath, ThunderStrike
from StatTracker import StatTracker
from Slime import Slime
from Minotaur import Minotaur
from Cthulu import Cthulu
from Demon import Demon
from tk_show_graph import run_graph_window


class RunGame:
    def __init__(self):
        """set up game attributes"""
        pg.init()
        pg.display.set_caption('Dungeon Hunter')
        self.__screen = pg.display.set_mode((Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT')))
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__game_state = "menu"
        self.__previous_game_state = self.__game_state
        self.__running = True

        """background attribute"""
        self.__level_name = 'MainMenu'
        self.__background = Bgd.load_menu(self.__level_name)
        self.__bg_width, self.bg_height = self.__background.get_size()
        self.__border = Bgd.get(self.__level_name, 'border')
        self.__level = 0
        self.__complete_level = False
        self.__start_level_time = 0

        """entities attribute"""
        spawn_point = Bgd.get(1, 'spawn')
        self.__player = Player(spawn_point[0], spawn_point[1])
        self.__FireBreath = FireBreath(self.__player.rect.x, self.__player.rect.y)
        self.__bullets = []
        self.__bullet_size = (20, 20)
        self.__enemies = []
        self.__effects = []

        """UI attributes"""
        self.__health_bar = HealthBar(20, 20, 450, 35, self.__player.health)
        self.__mana_bar = ManaBar(20, 63, 450, 35, self.__player.mana)
        self.__inventory = Inventory(500, 580, self.__player, self.__FireBreath)
        self.score = Score(37, 150, self.__player)
        self.__shop = Shop(self.__player)
        self.__shop.on_next_level_clicked = self.__go_to_next_level
        self.__show_gold = Gold(70, 130, self.__player)
        self.__restart_button = pg.Rect(Config.get('WIN_WIDTH') // 2 - 125, Config.get('WIN_HEIGHT') // 2 + 40, 250, 80)
        self.__stat_button = pg.Rect(Config.get('WIN_WIDTH') // 2 - 100, Config.get('WIN_HEIGHT') // 2 + 140, 200, 50)

        """stats display attribute"""
        button_x = 30
        self.__stat_back_button = pg.Rect(button_x, 590, 270, 60)


        """settings attributes"""
        self.__effect_plus = pg.Rect(880, 220, 40, 40)
        self.__effect_minus = pg.Rect(830, 220, 40, 40)
        self.__music_plus = pg.Rect(880, 375, 40, 40)
        self.__music_minus = pg.Rect(830, 375, 40, 40)
        self.__gear_img = pg.transform.scale(pg.image.load("picture/gear.png").convert_alpha(),
                                             (60, 60))
        self.__gear_button = self.__gear_img.get_rect(topleft=(Config.get('WIN_WIDTH') - 100, 20))
        self.__back_button = pg.Rect(Config.get('WIN_WIDTH') // 2 - 75, Config.get('WIN_HEIGHT') // 2 + 140, 150, 50)

        """other attributes"""
        self.__camera = Camera(Config.get('WIN_WIDTH'), Config.get('WIN_HEIGHT'))
        self.__camera.add(self.__player, *self.__enemies, *self.__bullets, *self.__effects, self.__FireBreath)
        self.__dash_time = 0
        self.__at_door = False
        self.__dash = False
        self.__before_dash_pos = self.__player.rect
        dash_effect = DashEffect(self.__player.rect.centerx, self.__player.rect.centery)
        self.__effects.append(dash_effect)
        self.__camera.add(dash_effect)
        self.__last_shot_time = 0
        self.__last_update_data = 0
        self.__minutes = 1
        self.__score_per_min = 0
        self.__enemy_dead_per_min = 0
        SoundManager.get_instance().play_music("bgm")

    def __settings_menu(self):
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(Bgd.load_menu('setting'), (0, 0))
        font = pg.font.SysFont("calibri", 40, bold=True)

        effect_text = font.render(f"Effects Volume: {int(SoundManager.get_instance().effect_volume * 100)}", True,
                                  (255, 255, 255))
        music_text = font.render(f"Music Volume: {int(SoundManager.get_instance().music_volume * 100)}", True,
                                 (255, 255, 255))
        plus = font.render("+", True, (255, 255, 255))
        minus = font.render("-", True, (255, 255, 255))
        self.__screen.blit(effect_text, (450, 220))
        self.__screen.blit(music_text, (450, 375))
        """draw button"""
        pg.draw.rect(self.__screen, (15, 87, 13), self.__effect_plus, border_radius=7)
        pg.draw.rect(self.__screen, (128, 25, 18), self.__effect_minus, border_radius=7)
        pg.draw.rect(self.__screen, (15, 87, 13), self.__music_plus, border_radius=7)
        pg.draw.rect(self.__screen, (128, 25, 18), self.__music_minus, border_radius=7)
        pg.draw.rect(self.__screen, (180, 0, 0), self.__back_button, border_radius=7)
        """draw button border"""
        pg.draw.rect(self.__screen, (0, 0, 0), self.__effect_plus, border_radius=7, width=4)
        pg.draw.rect(self.__screen, (0, 0, 0), self.__effect_minus, border_radius=7, width=4)
        pg.draw.rect(self.__screen, (0, 0, 0), self.__music_plus, border_radius=7, width=4)
        pg.draw.rect(self.__screen, (0, 0, 0), self.__music_minus, border_radius=7, width=4)
        pg.draw.rect(self.__screen, (0, 0, 0), self.__back_button, border_radius=7, width=4)
        """plus and minus and text in button"""
        self.__screen.blit(plus, (self.__effect_plus.x + 10, self.__effect_plus.y + 1))
        self.__screen.blit(plus, (self.__effect_plus.x + 10, self.__music_plus.y + 1))
        self.__screen.blit(minus, (self.__effect_minus.x + 14, self.__effect_minus.y + 2))
        self.__screen.blit(minus, (self.__effect_minus.x + 14, self.__music_minus.y + 2))

        back_text = font.render("BACK", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.__back_button.center)
        self.__screen.blit(back_text, back_text_rect)

    def __main_menu(self):
        self.__screen.fill((0, 0, 0))
        self.__screen.blit(self.__background, (0, 0))
        text = pg.image.load("picture/background/start_game_text.png")
        text.set_colorkey((0, 0, 0))
        self.__screen.blit(text, (0, 0))
        self.__screen.blit(self.__gear_img, self.__gear_button)

        """make stat button"""
        pg.draw.rect(self.__screen, (44, 44, 44), self.__stat_button, border_radius=8)
        pg.draw.rect(self.__screen, (112, 112, 112), self.__stat_button, border_radius=8, width=5)
        subfont = pg.font.SysFont("calibri", 35, bold=True)
        stat_text = subfont.render("STATISTICS", True, (255, 255, 255))
        stat_text_rect = stat_text.get_rect(center=self.__stat_button.center)
        self.__screen.blit(stat_text, stat_text_rect)

    def __game_over(self):
        self.__background = Bgd.load_menu('GameOver')
        self.__screen.blit(self.__background, (0, 0))
        pg.draw.rect(self.__screen, (44, 44, 44), self.__restart_button, border_radius=8)
        pg.draw.rect(self.__screen, (112, 112, 112), self.__restart_button, border_radius=8, width=5)

        subfont = pg.font.SysFont("calibri", 55, bold=True)
        restart_text = subfont.render("RESTART", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=self.__restart_button.center)
        score_text = subfont.render(f"SCORE: {self.__player.score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(Config.get('WIN_WIDTH') // 2, Config.get('WIN_HEIGHT') // 2))

        self.__screen.blit(score_text, score_text_rect)
        self.__screen.blit(restart_text, restart_text_rect)
        self.__screen.blit(self.__gear_img, self.__gear_button)

        """make stat button"""
        pg.draw.rect(self.__screen, (44, 44, 44), self.__stat_button, border_radius=8)
        pg.draw.rect(self.__screen, (112, 112, 112), self.__stat_button, border_radius=8, width=5)
        subfont = pg.font.SysFont("calibri", 35, bold=True)
        stat_text = subfont.render("STATISTICS", True, (255, 255, 255))
        stat_text_rect = stat_text.get_rect(center=self.__stat_button.center)
        self.__screen.blit(stat_text, stat_text_rect)

    def __update_all(self):
        self.__camera.update(self.__player)
        self.__screen.fill(Config.get('BG_COLOR'))
        self.__screen.blit(self.__background, (-self.__camera.camera_rect.x, -self.__camera.camera_rect.y))
        # self.player.draw(self.__screen, self.camera)

        finish_effect = []
        if self.__level_name == 'shop':
            self.__screen.blit(self.__background, (0, 0))
            self.__shop.draw(self.__screen)
            self.__health_bar.draw(self.__screen, self.__player.health)
            self.__mana_bar.draw(self.__screen, self.__player.mana)
            self.__show_gold.draw(self.__screen, 160, 130)
            return None
        for bullet in self.__bullets:
            bullet.draw(self.__screen, self.__camera)
        self.__player.draw(self.__screen, self.__camera)
        for enemy in self.__enemies:
            enemy.draw(self.__screen, self.__camera)
        self.__FireBreath.draw(self.__screen, self.__camera)
        # delete this loop if game is lag
        for effect in self.__effects:
            if isinstance(effect, DashEffect):
                if self.__dash:
                    effect.rect = self.__before_dash_pos
                    effect.finish = False
                    self.__dash = False
            else:
                if effect.finish:
                    finish_effect.append(effect)
            effect.draw(self.__screen, self.__camera)

        remove_set = set(finish_effect)
        self.__enemies = [b for b in self.__enemies if b not in remove_set]
        for effect in finish_effect:
            self.__effects.remove(effect)
            self.__camera.remove(effect)

        self.__health_bar.draw(self.__screen, self.__player.health)
        self.__mana_bar.draw(self.__screen, self.__player.mana)
        self.__inventory.draw(self.__screen)
        self.__show_gold.draw(self.__screen)
        self.score.draw(self.__screen)

        if self.__complete_level and self.__at_door:
            InteractUI.draw_interact_door(self.__screen)
        # self.camera.draw(self.__screen)

        self.__screen.blit(self.__gear_img, self.__gear_button)

    def __entities_events(self):
        """players event"""
        self.__at_door = self.__player.door_collision(Bgd.get(self.__level_name, 'door'))
        if self.__player.health <= 0:
            pg.mixer.music.stop()
            SoundManager.get_instance().play_music("game_over_music")
            SoundManager.get_instance().play_sound("game_over_sound")
            self.__game_state = "game_over"
        """"bullets event"""
        remove_bullets = []
        for bullet in self.__bullets:
            # check that bullets not go out of border
            if (self.__border["RIGHT"] + self.__bullet_size[0] * 2.5 > bullet.rect.centerx > self.__border["LEFT"] and
                    self.__border["DOWN"] + self.__bullet_size[1] * 3.5 > bullet.rect.centery > self.__border["UP"]):
                bullet.update()
                if isinstance(bullet, DemonBullet):
                    if self.__player.get_shoot(bullet):
                        SoundManager.get_instance().play_sound("DemonBulletHit")
                        explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                        self.__effects.append(explosion)
                        self.__camera.add(explosion)
                        remove_bullets.append(bullet)
                elif isinstance(bullet, CthuluBullet):
                    if self.__player.get_shoot(bullet):
                        SoundManager.get_instance().play_sound("CthuluBulletHit")
                        explosion = CthuluExplosion(bullet.rect.centerx, bullet.rect.centery)
                        self.__effects.append(explosion)
                        self.__camera.add(explosion)
                        remove_bullets.append(bullet)
                else:
                    for enemy in self.__enemies:
                        if enemy.check_alive() and enemy.get_damage(bullet, self.__player.damage):
                            # if bullet in self.bullets:
                            SoundManager.get_instance().play_sound("PlayerBulletHit")
                            explosion = Explosion(bullet.rect.centerx, bullet.rect.centery)
                            self.__effects.append(explosion)
                            self.__camera.add(explosion)
                            remove_bullets.append(bullet)

            else:
                remove_bullets.append(bullet)
        remove_set = set(remove_bullets)
        self.__bullets = [b for b in self.__bullets if b not in remove_set]
        for bullet in remove_bullets:
            self.__camera.remove(bullet)

        """enemies event"""
        self.__FireBreath.hit_enemy(self.__enemies, self.__player, self.__effects, self.__camera)

        dead_enemies = []
        for enemy in self.__enemies:

            enemy.move(self.__player, self.__enemies)
            if isinstance(enemy, Demon) or isinstance(enemy, Cthulu):
                enemy.hit_player(self.__player, bullets=self.__bullets, camera=self.__camera)
            elif enemy.hit_player(self.__player):
                pass

            if enemy.already_dead:
                StatTracker.get_instance().log("enemy_defeated", value=f"{enemy.__class__.__name__}")
                dead_enemies.append(enemy)
        remove_set = set(dead_enemies)
        self.__enemies = [b for b in self.__enemies if b not in remove_set]
        for enemy in dead_enemies:
            self.__player.gold += enemy.gold_drop
            self.__player.score += enemy.score
            self.__enemy_dead_per_min += 1
            self.__score_per_min += enemy.score
            self.__camera.remove(enemy)
            enemy.kill()
        if len(self.__enemies) == 0:
            self.__complete_level = True
        else:
            self.__complete_level = False

    def __random_spawn(self):
        spawn = Bgd.get(self.__level_name, 'enemy_spawn')
        spawn_x = spawn['x']
        spawn_y = spawn['y']
        return random.randint(spawn_x[0], spawn_x[1]), random.randint(spawn_y[0], spawn_y[1])

    def __restart_game(self):
        self.__update_data_per_minute()
        self.__score_per_min = 0
        self.__enemy_dead_per_min = 0
        self.__minutes = 1
        self.__player.reset_game()
        self.__shop.reset_game()
        # SoundManager.get_instance().play_music("bgm")
        SoundManager.get_instance().play_music("CthuluTheme")
        self.__level = 1
        self.__load_level(self.__level)
        self.__bullets.clear()
        self.__effects.clear()
        dash_effect = DashEffect(self.__player.rect.centerx, self.__player.rect.centery)
        self.__effects.append(dash_effect)
        self.__camera.add(dash_effect)
        self.__complete_level = False
        self.__at_door = False
        self.__previous_game_state = "playing"
        self.__game_state = "playing"

    def __set_level(self, name):
        self.__background = Bgd.load_bg(name)
        self.__border = Bgd.get(name, 'border')
        self.__player.rect.center = Bgd.get(name, 'spawn')

    def __go_to_next_level(self):
        self.__level += 1
        self.__load_level(self.__level)
        self.__shop.toggle_shop()
        SoundManager.get_instance().play_sound("DoorClose")

    def __level_generator(self, level):

        if level % 7 == 0:
            self.__level_name = 4
            for i in range(1):
                # pg.mixer.music.stop()
                # SoundManager.get_instance().play_music("CthuluTheme")
                spawn_x, spawn_y = self.__random_spawn()
                new_enemy = Cthulu(spawn_x, spawn_y, health=7 * level)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.__enemies.append(new_enemy)
            self.__camera.add(*self.__enemies)
            self.__set_level(self.__level_name)

        elif level % 5 == 0:
            self.__level_name = 3
            spawn_num = level // 5
            if spawn_num > 5:
                spawn_num = 5
            for i in range(spawn_num):
                spawn_x, spawn_y = self.__random_spawn()
                new_enemy = Demon(spawn_x, spawn_y, health=int(level * 1.25), level=self.__level_name)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.__enemies.append(new_enemy)
            self.__camera.add(*self.__enemies)
            self.__set_level(self.__level_name)

        elif level % 3 == 0:
            self.__level_name = 2
            for i in range(level // 3):
                spawn_x, spawn_y = self.__random_spawn()
                new_enemy = Minotaur(spawn_x, spawn_y, health=3 * level)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.__enemies.append(new_enemy)
            self.__camera.add(*self.__enemies)
            self.__set_level(self.__level_name)

        else:
            self.__level_name = 1
            for i in range(level):
                spawn_x, spawn_y = self.__random_spawn()
                new_enemy = Slime(spawn_x, spawn_y, health=5 + level)
                new_enemy.rect.topleft = (spawn_x, spawn_y)
                self.__enemies.append(new_enemy)
            self.__camera.add(*self.__enemies)
            self.__set_level(self.__level_name)

    def __load_level(self, level):
        self.__enemies.clear()
        if level == 'shop':
            self.__level_name = 'shop'
            self.__set_level(self.__level_name)
        else:
            self.__start_level_time = pg.time.get_ticks()
            self.__level_generator(level)

    def __update_data_per_minute(self):
        if self.__level != 0:
            StatTracker.get_instance().log(event_type="game_stats_per_min", minutes=self.__minutes, level=self.__level,
                                           enemy_dead=self.__enemy_dead_per_min,
                                           score=self.__score_per_min, distance=self.__player.distance_per_min / 10)
            self.__score_per_min = 0
            self.__enemy_dead_per_min = 0
            self.__player.distance_per_min = 0
            self.__minutes += 1

    def run_loop(self):
        clock = pg.time.Clock()
        while self.__running:
            if self.__game_state == 'playing':
                now = pg.time.get_ticks()
                if now - self.__last_update_data >= 60000:
                    self.__update_data_per_minute()
                    self.__last_update_data = now
            if self.__game_state == 'playing' and self.__level_name != 'shop':
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

            # start_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.__game_state != 'main_menu':
                        self.__update_data_per_minute()
                    self.__running = False
                if event.type == pg.KEYDOWN and self.__game_state == 'playing':
                    now = pg.time.get_ticks()

                    if event.key == pg.K_SPACE and self.__player.use_skill('SPACE') and self.__level_name != 'shop':
                        self.__before_dash_pos = self.__player.rect.copy()
                        self.__player.dash(self.__border)
                        self.__dash = True
                        self.__dash_time = now

                    if event.key == pg.K_e:
                        if self.__level_name == 'shop':
                            StatTracker.get_instance().log("level_complete", value=self.__level,
                                                           time_used=(now - self.__start_level_time) / 1000)
                            SoundManager.get_instance().play_sound("DoorOpen")
                            self.__level += 1
                            self.__load_level(self.__level)
                            self.__shop.toggle_shop()
                        elif self.__complete_level and self.__at_door:
                            SoundManager.get_instance().play_sound("DoorClose")
                            self.__load_level('shop')
                            self.__shop.toggle_shop()
                    if event.key == pg.K_1 and self.__player.use_skill('1'):
                        self.__player.drink_potion('health_potion')
                    if event.key == pg.K_2 and self.__player.use_skill('2'):
                        self.__player.drink_potion('mana_potion')
                    if (event.key == pg.K_r and self.__player.unlock_thunder_strike and self.__player.use_skill("R")
                            and ThunderStrike.check_mana(self.__player.mana)):
                        ThunderStrike.hit_enemy(self.__enemies, self.__player, self.__effects, self.__camera)

                if event.type == pg.MOUSEBUTTONDOWN:
                    """Click Event"""
                    if event.button == pg.BUTTON_LEFT:
                        now = pg.time.get_ticks()
                        if self.__gear_button.collidepoint(event.pos) and self.__game_state != "settings":
                            SoundManager.get_instance().play_sound("Hover")
                            self.__previous_game_state = self.__game_state
                            self.__game_state = "settings"
                        # """Shooting Event"""
                        elif (self.__player.use_skill("CLICK") and not self.__player.drink_state
                              and self.__level_name != 'shop' and self.__game_state == 'playing'):
                            mouse_pos = pg.mouse.get_pos()
                            mouse_pos_world = (mouse_pos[0] + self.__camera.camera_rect.x,
                                               mouse_pos[1] + self.__camera.camera_rect.y)
                            if mouse_pos_world[0] < self.__player.rect.x:
                                self.__player.set_left_right("LEFT")
                            else:
                                self.__player.set_left_right("RIGHT")
                            self.__player.attack()

                            new_bullet = Bullet(self.__player.rect.centerx, self.__player.rect.centery, mouse_pos_world,
                                                self.__bullet_size)
                            self.__bullets.append(new_bullet)
                            self.__last_shot_time = now
                            self.__camera.add(new_bullet, *self.__bullets)
                    # """setting state"""
                    if self.__game_state == "settings":
                        if self.__effect_plus.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            SoundManager.get_instance().set_effect_volume(
                                min(1.0, SoundManager.get_instance().effect_volume + 0.1))
                        elif self.__effect_minus.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            SoundManager.get_instance().set_effect_volume(
                                max(0.0, SoundManager.get_instance().effect_volume - 0.1))
                        elif self.__music_plus.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            SoundManager.get_instance().set_music_volume(
                                min(1.0, SoundManager.get_instance().music_volume + 0.1))
                        elif self.__music_minus.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            SoundManager.get_instance().set_music_volume(
                                max(0.0, SoundManager.get_instance().music_volume - 0.1))
                        elif self.__back_button.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            self.__game_state = self.__previous_game_state
                    # """menu state"""
                    elif event.button == pg.BUTTON_LEFT and self.__game_state == "menu":
                        if self.__stat_button.collidepoint(event.pos):
                            run_graph_window()
                        elif self.__gear_button.collidepoint(event.pos):
                            self.__previous_game_state = self.__game_state
                            self.__game_state = "settings"
                        else:
                            SoundManager.get_instance().play_sound("Hover")
                            self.__restart_game()
                    # """game over state"""
                    elif event.button == pg.BUTTON_LEFT and self.__game_state == "game_over":
                        if self.__stat_button.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            run_graph_window()
                        elif self.__restart_button.collidepoint(event.pos):
                            SoundManager.get_instance().play_sound("Hover")
                            self.__restart_game()
                    if self.__level_name == 'shop':
                        self.__shop.handle_event(event)
            """game state"""
            if self.__game_state == "playing":
                self.__update_all()
                self.__entities_events()
                key = pg.key.get_pressed()
                # print(self.player.player_rect.y, self.player.player_rect.x)
                if self.__level_name != 'shop' and not self.__player.drink_state:
                    if key[pg.K_w] and self.__player.wall_collision("UP", self.__border["UP"]):
                        self.__player.move("UP")
                    if key[pg.K_s] and self.__player.wall_collision("DOWN", self.__border["DOWN"]):
                        self.__player.move("DOWN")
                    if key[pg.K_a] and self.__player.wall_collision("LEFT", self.__border["LEFT"]):
                        self.__player.move("LEFT")
                    if key[pg.K_d] and self.__player.wall_collision("RIGHT", self.__border["RIGHT"]):
                        self.__player.move("RIGHT")

                    if key[pg.K_q] and self.__player.unlock_fire_breathe and self.__FireBreath.check_mana(
                            self.__player.mana):
                        self.__FireBreath.activate = True
                        self.__FireBreath.set_position(self.__player.rect, self.__player.left_right)
                    else:
                        self.__FireBreath.activate = False
            elif self.__game_state == "menu":
                self.__main_menu()
            elif self.__game_state == "game_over":
                self.__game_over()
            elif self.__game_state == "settings":
                self.__settings_menu()


            pg.display.flip()
            clock.tick(Config.get('FPS'))
            fps = clock.get_fps()
            # print(f"FPS: {fps:.2f}")

    pg.quit()


if __name__ == "__main__":
    play = RunGame()
    play.run_loop()
