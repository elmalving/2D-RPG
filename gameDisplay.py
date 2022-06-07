import time

import pygame
import sqlite3
import random
import Mob
from button import Button
from Items import Item


class gameDisplay:
    def __init__(self, player):
        pygame.init()
        pygame.display.set_icon(pygame.image.load('icon.png'))
        pygame.display.set_caption("Project RPG")
        self.player = player
        self.db = sqlite3.connect('info.db')
        self.cursor = self.db.cursor()
        self.screen = pygame.display.set_mode((1280, 720))
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.first_row = self.width // 6
        self.first_col = self.height // 8
        self.second_row = self.width // 1.7
        self.second_col = self.height // 2
        self.running = True

    @property
    def mouse(self):
        return pygame.mouse.get_pos()

    def showMenu(self):
        self.screen.blit(pygame.image.load('menu_bg.png'), (0, 0))
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('menu_bg_music.mp3')
            pygame.mixer.music.play(-1)
        inv_button = Button(self.screen, self.first_row, self.first_col, self.width // 4, self.height // 4,
                            image=pygame.image.load('inv_button.png'))
        battle_button = Button(self.screen, self.second_row, self.first_col, self.width // 4, self.height // 4,
                               image=pygame.image.load('battle_button.png'))
        inv_button.create_rect()
        battle_button.create_rect()

        pygame.display.update()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if inv_button.touched(self.mouse):
                        self.showInventory()
                    if battle_button.touched(self.mouse):
                        pygame.mixer.music.stop()
                        self.screen.fill('black')
                        pygame.display.update()
                        self.zombieFight()
                if event.type == pygame.MOUSEMOTION:
                    if inv_button.touched(self.mouse):
                        if not inv_button.colored:
                            inv_button.image = pygame.image.load('inv_button_hover.png')
                            inv_button.create_rect()
                            inv_button.colored = True
                    elif inv_button.colored:
                        inv_button.image = pygame.image.load('inv_button.png')
                        inv_button.create_rect()
                        inv_button.colored = False
                    if battle_button.touched(self.mouse):
                        if not battle_button.colored:
                            battle_button.image = pygame.image.load('battle_button_hover.png')
                            battle_button.create_rect()
                            battle_button.colored = True
                    elif battle_button.colored:
                        battle_button.image = pygame.image.load('battle_button.png')
                        battle_button.create_rect()
                        battle_button.colored = False

            pygame.display.update()
            pygame.time.Clock().tick(30)

    def showInventory(self):
        self.screen.blit(pygame.image.load('inv_bg.png'), (0, 0))
        if self.player.weapon:
            Button(screen=self.screen, x=self.width // 4.28, y=self.height // 1.95, width=self.height // 9.6,
                   height=self.height // 9.6, text=f'{self.player.weapon.name}',
                   text_color=f'{self.player.weapon.rarityColor}', font_size=11).create_rect()
        if self.player.armor:
            Button(screen=self.screen, x=self.width // 3.325, y=self.height // 3.1, width=self.height // 7.3,
                   height=self.height // 7.3, text=f'{self.player.armor.name}',
                   text_color=f'{self.player.armor.rarityColor}', font_size=15).create_rect()
        if self.player.money:
            Button(screen=self.screen, x=self.width // 2.505, y=self.height // 6.755, width=self.height // 9.6,
                   height=self.height // 9.6, text=f'{self.player.money}', text_color='yellow', only_text=True,
                   font_size=20).create_rect()
        self.cursor.execute(f"SELECT inventory FROM {self.player.name}")
        inventory = self.cursor.fetchall()[1:]
        self.db.commit()
        cell_coord = [(self.width // 1.6525 + self.width // 11.1 * j, self.height // 45.2 + self.height // 12.6 * i)
                      for i in range(12) for j in range(4)]

        items = []
        item_buttons = []

        for i in range(len(inventory)):
            item = Item.from_id(inventory[i][0])
            button = Button(self.screen, cell_coord[i][0], cell_coord[i][1], width=self.width // 11.7,
                            height=self.height // 13.75, text=item.name, text_color=item.rarityColor, font_size=15)
            button.create_rect()
            item_buttons.append(button)
            items.append(item)

        pygame.display.update()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.showMenu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for cell in range(len(item_buttons)):
                        if item_buttons[cell].touched(self.mouse):
                            if event.button == 3:
                                self.cursor.execute(f"""UPDATE {self.player.name} 
                                            SET money = {self.player.money + items[cell].price} WHERE rowid = 1""")
                                self.db.commit()
                                self.player.money += items[cell].price
                            elif event.button == 1:
                                if items[cell].type != 'armor':
                                    if self.player.weapon:
                                        self.cursor.execute(f'INSERT INTO {self.player.name} (inventory) VALUES (?)',
                                                            (self.player.weapon.id,))
                                        self.db.commit()
                                    self.player.weapon = Item.from_id(items[cell].id)
                                    self.cursor.execute(f"""UPDATE {self.player.name} SET weapon = {items[cell].id}
                                                        WHERE rowid = 1""")
                                    self.db.commit()
                                else:
                                    if self.player.armor:
                                        self.cursor.execute(f'INSERT INTO {self.player.name} (inventory) VALUES (?)',
                                                            (self.player.armor.id,))
                                        self.db.commit()
                                    self.player.armor = Item.from_id(items[cell].id)
                                    self.cursor.execute(f"""UPDATE {self.player.name} SET armor = {items[cell].id}
                                                        WHERE rowid = 1;""")
                                    self.db.commit()
                            self.cursor.execute(f"""SELECT rowid FROM {self.player.name} 
                                            WHERE inventory = {items[cell].id}""")
                            self.db.commit()
                            self.cursor.execute(f"""DELETE FROM {self.player.name}
                                            WHERE rowid = {self.cursor.fetchone()[0]}""")
                            self.db.commit()
                            self.showInventory()

                if event.type == pygame.MOUSEMOTION:
                    for cell in range(len(item_buttons)):
                        if item_buttons[cell].touched(self.mouse):
                            if not item_buttons[cell].colored:
                                gui_itemName = Button(screen=self.screen,
                                                      x=item_buttons[cell].x - self.width // 11.7 - self.width // 80,
                                                      y=item_buttons[cell].y,
                                                      width=self.width // 10, height=self.height // 48,
                                                      text=items[cell].name,
                                                      font_size=12)
                                gui_damage = Button(screen=self.screen,
                                                    x=item_buttons[cell].x - item_buttons[cell].width,
                                                    y=item_buttons[cell].y + self.height // 36,
                                                    width=self.width // 12.8, height=self.height // 60,
                                                    text=f'Damage: {items[cell].damage}' if items[cell].type != 'armor'
                                                    else f'Armor: {items[cell].armor}',
                                                    font_size=10)
                                gui_item_type = Button(screen=self.screen,
                                                       x=item_buttons[cell].x - item_buttons[cell].width,
                                                       y=item_buttons[cell].y + self.height // 20.57,
                                                       width=self.width // 12.8, height=self.height // 60,
                                                       text=f'Range: {items[cell].type}' if items[cell].type != 'armor'
                                                       else f'Type: {items[cell].type}',
                                                       font_size=10)
                                gui_price = Button(screen=self.screen,
                                                   x=item_buttons[cell].x - item_buttons[cell].width,
                                                   y=item_buttons[cell].y + self.height // 14.4,
                                                   width=self.width // 12.8, height=self.height // 60,
                                                   text=f'Price: {items[cell].price}',
                                                   font_size=10)
                                gui_itemName.create_rect(outline=items[cell].rarityColor)
                                gui_damage.create_rect(outline=items[cell].rarityColor)
                                gui_item_type.create_rect(outline=items[cell].rarityColor)
                                gui_price.create_rect(outline=items[cell].rarityColor)
                                item_buttons[cell].colored = True
                                pygame.display.update()
                        elif item_buttons[cell].colored:
                            item_buttons[cell].colored = False
                            self.showInventory()

            pygame.time.Clock().tick(30)

    def zombieFight(self):
        zombie = Mob.Zombie()
        zombie_img = Button(screen=self.screen, x=self.second_row - self.first_row, y=self.second_col,
                            text=str(zombie.health), width=self.width // 8, height=self.height // 5, color='green')
        zombie_img.create_rect()
        damageTexts = []
        zombie_img_reached_left = False
        zombie_img_reached_right = True
        pygame.display.update()

        while self.running:

            zombie_img.color = 'black'
            zombie_img.create_rect()

            if zombie_img_reached_left:
                zombie_img.x += 3
            elif zombie_img_reached_right:
                zombie_img.x -= 3

            if zombie_img.x <= 0:
                zombie_img.x = 0
                zombie_img_reached_left = True
                zombie_img_reached_right = False

            elif zombie_img.x >= self.width - self.width // 8:
                zombie_img.x = self.width - self.width // 8
                zombie_img_reached_right = True
                zombie_img_reached_left = False

            zombie_img.color = 'green'
            zombie_img.create_rect()

            for damage in damageTexts:
                damage.text_color = (damage.text_color[0] - 5, 0, 0)
                damage.create_rect()
                if damage.text_color[0] == 0:
                    damageTexts.remove(damage)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.showMenu()

                # Battle logic
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player.weapon.type == 'long-range' and event.button == 3:
                        clicked = time.time()
                        continue
                    # Close-range weapon
                    if zombie_img.touched(self.mouse):
                        pygame.mixer.Sound('zombie_attacked_sound.mp3').play()

                        damageCoord = self.get_above_coord(zombie_img.x, zombie_img.y, zombie_img.width,
                                                           zombie_img.height)
                        currentDamage = Button(screen=self.screen, x=damageCoord[0], y=damageCoord[1],
                                               width=self.width // 16, height=self.height // 22,
                                               text=str(self.player.attack(zombie)), text_color=(255, 0, 0),
                                               font_size=20, only_text=True)
                        currentDamage.create_rect()
                        damageTexts.append(currentDamage)
                        zombie_img.text = str(zombie.health)
                        zombie_img.create_rect()
                        if zombie.health < 1:
                            pygame.mixer.Sound('zombie_die_sound.mp3').play()
                            self.screen.fill('black')
                            pygame.display.update()
                            self.win(zombie)

                if event.type == pygame.MOUSEBUTTONUP and zombie_img.touched(self.mouse) \
                        and self.player.weapon.type == 'long-range' and event.button == 3:
                    # Bow
                    released = time.time()
                    pygame.mixer.Sound('zombie_attacked_sound.mp3').play()

                    damageCoord = self.get_above_coord(zombie_img.x, zombie_img.y, zombie_img.width,
                                                       zombie_img.height)
                    currentDamage = Button(screen=self.screen, x=damageCoord[0], y=damageCoord[1],
                                           width=self.width // 16, height=self.height // 22,
                                           text=str(self.player.attack(target=zombie, stretch=released - clicked)),  # noqa, 'clicked' always exists
                                           text_color=(255, 0, 0), font_size=20, only_text=True)
                    currentDamage.create_rect()
                    damageTexts.append(currentDamage)
                    zombie_img.text = str(zombie.health)
                    zombie_img.create_rect()
                    if zombie.health < 1:
                        pygame.mixer.Sound('zombie_die_sound.mp3').play()
                        self.screen.fill('black')
                        pygame.display.update()
                        self.win(zombie)

            pygame.time.Clock().tick(30)
            pygame.display.update()

    def win(self, mob):
        drop = list(mob.die())
        items_coord = self.get_rand_coord(len(drop))
        items_buttons = []
        for i in range(len(drop)):
            items_buttons.append(Button(screen=self.screen, x=items_coord[i][0], y=items_coord[i][1],
                                        width=self.width // 12, height=self.height // 22, text=drop[i].name,
                                        text_color=drop[i].rarityColor, color='grey', font_size=15))
            items_buttons[i].create_rect(outline=drop[i].rarityColor)

        pygame.display.update()

        fullButton = []

        while self.running:
            if fullButton:
                if fullButton[0][2] <= 0:
                    fullButton[0][0].color = 'grey'
                    fullButton[0][0].text = f'{fullButton[0][1].name}'
                    fullButton[0][0].create_rect(outline=fullButton[0][1].rarityColor)
                    pygame.display.update()
                    fullButton.remove(fullButton[0])
                else:
                    fullButton[0][2] -= 100
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.showMenu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(items_buttons)):
                        if items_buttons[i].touched(self.mouse):
                            self.cursor.execute(f'SELECT COUNT(inventory) FROM {self.player.name};')
                            self.db.commit()
                            if self.cursor.fetchone()[0] < 48:
                                pygame.mixer.Sound('item_pick_sound.mp3').play()
                                items_buttons[i].color = 'black'
                                items_buttons[i].x -= items_buttons[i].width // 2
                                items_buttons[i].width += items_buttons[i].width * 2
                                items_buttons[i].text = f'{drop[i].name} collected!'
                                items_buttons[i].create_rect(outline=drop[i].rarityColor)
                                self.cursor.execute(f'INSERT INTO {self.player.name} (inventory) VALUES (?);',
                                                    (drop[i].id,))
                                self.db.commit()
                                items_buttons.remove(items_buttons[i])
                                drop.remove(drop[i])
                            else:
                                # pygame.mixer.Sound('full_inv_warn.mp3').play()
                                items_buttons[i].color = 'red'
                                items_buttons[i].text = f'Inventory is full!'
                                items_buttons[i].create_rect(outline=drop[i].rarityColor)
                                fullButton.append([items_buttons[i], drop[i], 1000])

                            pygame.display.update()
                            break

            pygame.time.Clock().tick(30)

    def get_rand_coord(self, length):
        items_coord = [(random.randint(self.first_row, self.second_row),
                        random.randint(self.first_col, self.second_col))]
        while len(items_coord) < length:
            same = False
            rect = pygame.Rect(random.randint(self.first_row, self.second_row),
                               random.randint(self.first_col, self.second_col), self.width // 12, self.height // 22)
            for x1, y1 in items_coord:
                if rect.colliderect((x1, y1, self.width // 12, self.height // 22)):
                    same = True
                    break
            if not same:
                items_coord.append((rect.x, rect.y))
        return items_coord

    @staticmethod
    def get_above_coord(x, y, width, height):
        return random.randint(x - width * 2, x + width * 2), random.randint(y - height * 2, y - height / 3)
