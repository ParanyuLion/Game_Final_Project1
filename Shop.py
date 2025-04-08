import pygame as pg


class Shop:
    def __init__(self, player):
        self.player = player
        self.size = (70,70)
        self.items = [
            {"name": "Health Potion", "price": 10, "effect": self.increase_health_potion,
             "image": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/HealPotion.png"), self.size),
             "amount": 10},
            {"name": "Speed Potion", "price": 200, "effect": self.increase_speed,
             "image": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/SpeedPotion.png"), self.size),
             "amount": 2},
            {"name": "Mana Potion", "price": 100, "effect": self.increase_mana_potion,
             "image": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/ManaPotion.png"), self.size),
             "amount": 10},
            {"name": "Thunder Strike", "price": 250, "effect": self.unlock_thunder_strike,
             "image": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/MagicIcon/ThunderStrikeIcon.png"), self.size),
             "amount": 1},
            {"name": "Fire Breath", "price": 200, "effect": self.unlock_fire_breathe,
             "image": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/MagicIcon/FireBreathIcon.png"), self.size),
             "amount": 1},
            {"name": "Attack Potion", "price": 300, "effect": self.increase_damage,
             "image": pg.transform.scale(pg.image.load("Game_Final_Project1/picture/Potion/AttackPotion.png"), self.size),
             "amount": 2},
        ]
        self.font = pg.font.Font(None, 36)
        self.shop_open = False
        self.buttons = []
        for i in range(len(self.items)):
            if i < len(self.items)//2:
                self.buttons.append(pg.Rect(370, 200 + i * 150, 100, 40))
            else:
                self.buttons.append(pg.Rect(370 + 500, 200 + (i-len(self.items)//2) * 150, 100, 40))

    def increase_health_potion(self):
        self.player.health_potion += 1

    def increase_speed(self):
        self.player.speed += 1

    def increase_mana_potion(self):
        self.player.mana_potion += 1

    def increase_damage(self):
        self.player.damage += 5

    def unlock_fire_breathe(self):
        self.player.unlock_fire_breathe = True

    def unlock_thunder_strike(self):
        self.player.unlock_thunder_strike = True

    def buy_item(self, index):
        item = self.items[index]
        if self.player.gold >= item["price"] and item["amount"] > 0:
            self.player.gold -= item["price"]
            item["effect"]()
            print(f"Bought {item['name']}!")
            item["amount"] -= 1

        else:
            print("Not enough gold!")

    def draw(self, screen):
        if self.shop_open:
            shop_bg = pg.Surface((1080, 520))
            shop_bg.set_alpha(200)
            shop_bg.fill((50, 50, 50))
            screen.blit(shop_bg, (100, 100))
            # pg.draw.rect(screen, (50, 50, 50), (100, 100, 1080, 520))

            gold_text = self.font.render(f"Gold: {self.player.gold}", True, (255, 255, 0))
            screen.blit(gold_text, (120, 110))
            for i, item in enumerate(self.items):
                if i < len(self.items) // 2:
                    screen.blit(item["image"], (170, 150 + i * 150))

                    text = self.font.render(f"{item['name']} - {item['price']} Gold", True, (255, 255, 255))
                    screen.blit(text, (260, 150 + i * 150))

                    if item["amount"] > 0:
                        pg.draw.rect(screen, (0, 200, 0), self.buttons[i])
                        buy_text = self.font.render("Buy", True, (255, 255, 255))
                        screen.blit(buy_text, (self.buttons[i].x + 25, self.buttons[i].y + 5))
                    else:
                        pg.draw.rect(screen, (200, 0, 0), self.buttons[i])
                        buy_text = self.font.render("Sold", True, (255, 255, 255))
                        screen.blit(buy_text, (self.buttons[i].x + 25, self.buttons[i].y + 5))
                else:
                    screen.blit(item["image"], (170 + 500, 150 + (i-len(self.items)//2) * 150))

                    text = self.font.render(f"{item['name']} - {item['price']} Gold", True, (255, 255, 255))
                    screen.blit(text, (260 + 500, 150 + (i-len(self.items)//2) * 150))

                    if item["amount"] > 0:
                        pg.draw.rect(screen, (0, 200, 0), self.buttons[i])
                        buy_text = self.font.render("Buy", True, (255, 255, 255))
                        screen.blit(buy_text, (self.buttons[i].x + 25, self.buttons[i].y + 5))
                    else:
                        pg.draw.rect(screen, (200, 0, 0), self.buttons[i])
                        buy_text = self.font.render("Sold", True, (255, 255, 255))
                        screen.blit(buy_text, (self.buttons[i].x + 25, self.buttons[i].y + 5))

    def toggle_shop(self):
        self.shop_open = not self.shop_open

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.shop_open:
            for i, button in enumerate(self.buttons):
                if button.collidepoint(event.pos):
                    self.buy_item(i)
