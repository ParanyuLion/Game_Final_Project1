import pygame as pg


class Shop:
    def __init__(self, player):
        self.player = player
        self.items = [
            {"name": "Health Potion", "price": 100, "effect": self.increase_health,
             "image": pg.image.load("Game_Final_Project1/picture/Potion/HealPotion.png")},
            {"name": "Speed Potion", "price": 200, "effect": self.increase_speed,
             "image": pg.image.load("Game_Final_Project1/picture/Potion/SpeedPotion.png")},
            {"name": "Mana Potion", "price": 100, "effect": self.increase_attack,
             "image": pg.image.load("Game_Final_Project1/picture/Potion/ManaPotion.png")},
            {"name": "Health Potion", "price": 100, "effect": self.increase_health,
             "image": pg.image.load("Game_Final_Project1/picture/Potion/AttackPotion.png")},
            {"name": "Speed Potion", "price": 200, "effect": self.increase_speed,
             "image": pg.image.load("Game_Final_Project1/picture/Potion/SpeedPotion.png")},
            {"name": "Attack Potion", "price": 300, "effect": self.increase_attack,
             "image": pg.image.load("Game_Final_Project1/picture/Potion/ManaPotion.png")}
        ]
        self.font = pg.font.Font(None, 36)
        self.shop_open = False
        self.buttons = []
        for i in range(len(self.items)):
            if i < len(self.items)//2:
                self.buttons.append(pg.Rect(320, 200 + i * 150, 100, 40))
            else:
                self.buttons.append(pg.Rect(320 + 500, 200 + (i-len(self.items)//2) * 150, 100, 40))


    def increase_health(self):
        self.player.health += 20

    def increase_speed(self):
        self.player.speed += 1

    def increase_attack(self):
        self.player.attack_power += 5

    def buy_item(self, index):
        item = self.items[index]
        if self.player.gold >= item["price"]:
            self.player.gold -= item["price"]
            item["effect"]()
            print(f"Bought {item['name']}!")
        else:
            print("Not enough gold!")

    def draw(self, screen):
        if self.shop_open:
            pg.draw.rect(screen, (50, 50, 50), (100, 100, 1080, 520))

            gold_text = self.font.render(f"Gold: {self.player.gold}", True, (255, 255, 0))
            screen.blit(gold_text, (120, 110))
            for i, item in enumerate(self.items):
                if i < len(self.items) // 2:
                    screen.blit(item["image"], (120, 150 + i * 150))

                    text = self.font.render(f"{item['name']} - {item['price']} Gold", True, (255, 255, 255))
                    screen.blit(text, (180, 150 + i * 150))

                    pg.draw.rect(screen, (0, 200, 0), self.buttons[i])
                    buy_text = self.font.render("Buy", True, (255, 255, 255))
                    screen.blit(buy_text, (self.buttons[i].x + 25, self.buttons[i].y + 5))
                else:
                    screen.blit(item["image"], (120 + 500, 150 + (i-len(self.items)//2) * 150))

                    text = self.font.render(f"{item['name']} - {item['price']} Gold", True, (255, 255, 255))
                    screen.blit(text, (180 + 500, 150 + (i-len(self.items)//2) * 150))

                    pg.draw.rect(screen, (0, 200, 0), self.buttons[i])
                    buy_text = self.font.render("Buy", True, (255, 255, 255))
                    screen.blit(buy_text, (self.buttons[i].x + 25, self.buttons[i].y + 5))

    def toggle_shop(self):
        self.shop_open = not self.shop_open

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.shop_open:
            for i, button in enumerate(self.buttons):
                if button.collidepoint(event.pos):
                    self.buy_item(i)