import pygame
import pygame as pg
import visual
from block import *
from constants import *
from world import *
from hero import *
from buttons import *
from inventory import *
import time
import os
import pickle
from  world_cutted import *


class Game:
    def __init__(self):
        pg.init()
        self.finished = False
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.drawer = visual.Drawer(self.screen)
        self.world = World(-1)
        self.hero = Hero(screen_width//2, screen_height//2)
        self.world.move(-world_size_x//3*block_size, 0)
        self.clock = pg.time.Clock()
        self.inventory = Inventory(self.screen)
        self.background = pygame.transform.scale(LABaria_pict, (1200, 800))
        self.start_button = Button(350, 200, 1, 'Start')
        self.load_save_button = Button(350, 400, 1, 'Load save')
        self.exit_button = Button(350, 600, 1, 'Exit')
        self.game_status = GameStatus.in_main_menu
        self.back_button = Button(350, 200, 1, 'Back')
        self.save_game_button = Button(350, 400, 1, 'Save game')
        self.files = os.listdir('saves')
        self.saves = []
        self.need_to_blit = True

    def world_move_general(self, keys):
        """Функция, которая осуществляет движение мира с помощью других функций в world.py"""
        for chunk in range(len(self.world.map)):
            if self.world.map[chunk][0][0].x >= screen_width + 2*block_size:
                self.world.move_chunk_to_left(chunk)
            elif self.world.map[chunk][0][-1].x <= -2*block_size:
                self.world.move_chunk_to_right(chunk)
        if keys[pygame.K_a]:
            self.world.vx = hero_speed
        if keys[pygame.K_d]:
            self.world.vx = -hero_speed

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.world.vx = 0

        self.world.vy -= g
        if keys[pygame.K_SPACE] and not self.hero.falling:
            self.world.vy += hero_jump_power

        if self.world.will_collide_with_rect(self.world.vx, 0, self.hero.rect):
            self.world.vx = 0
        if self.world.will_collide_with_rect(0, self.world.vy, self.hero.rect):
            if self.world.will_collide_with_rect(0, -g, self.hero.rect):  # Проверяет можно ли еще чуть сместить героя
                self.hero.falling = False
            self.world.vy = 0
        else:
            self.hero.falling = True
        self.world.move(self.world.vx, self.world.vy)

    def break_block(self, chunk, block_x, block_y):
        block = self.world.map[chunk][block_y][block_x]
        if (block.x - self.hero.x) ** 2 + (block.y - self.hero.y) ** 2 <= hero_dig_range ** 2:
            s = time.time()
            if block.breaking_time is not None:
                if self.hero.breaking_block == block:
                    if s - self.hero.breaking_start_time >= block_breaking_time[block.type]:
                        self.world.remove_block(chunk, block_x, block_y)
                        self.stop_break_block()
                    else:
                        degree = (s - self.hero.breaking_start_time) / block_breaking_time[block.type]
                        block.set_transparency_level(degree * 0.4)
                else:
                    self.stop_break_block()
                    self.hero.breaking_block = block
                    self.hero.breaking_start_time = s
            else:
                self.stop_break_block()
        else:
            self.stop_break_block()

    def stop_break_block(self):
        if self.hero.breaking_block is not None:  # Останвливает ломание блока
            self.hero.breaking_block.set_transparency_level(0)
            self.hero.breaking_block = None
            self.hero.breaking_start_time = None

    def main_menu_activity(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
        self.screen.blit(self.background, (0, 0))
        self.start_button.draw_on(self.screen)
        self.exit_button.draw_on(self.screen)
        self.load_save_button.draw_on(self.screen)
        if self.start_button.collide(self.screen):
            self.game_status = GameStatus.in_game
        if self.exit_button.collide(self.screen):
            self.finished = True
        if self.load_save_button.collide(self.screen):
            self.game_status = GameStatus.in_saves
            self.load_save_button.clicked = False
#            print("Введите название сохранения:")
#            name = input()
#            files = os.listdir('saves')
#            if name in files:
#                self.download(name)
#                self.game_status = GameStatus.in_game
#            else:
#                print("Сохранение не найдено.")
#        else:
#            self.load_save_button.clicked = False
        pygame.display.update()

    def pause_activity(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game_status = GameStatus.in_game
        self.back_button.clicked = False
        if self.need_to_blit == True:
            back1 = self.background
            back1.set_alpha(50)
            self.screen.blit(back1, (0, 0))
            self.need_to_blit = False
        self.back_button.draw_on(self.screen)
        if self.back_button.collide(self.screen):
            self.game_status = GameStatus.in_game
        self.exit_button.draw_on(self.screen)
        if self.exit_button.collide(self.screen):
            self.finished = True
        self.save_game_button.draw_on(self.screen)
        if self.save_game_button.collide(self.screen):
            print("Введите название сохранения:")
            name = input()
            if name in self.files:
                print('Это название уже занято. Используйте другое название.')
            else:
                self.save_game(name)
                print('Файл сохранён.')
                self.files = os.listdir('saves')
        else:
            self.save_game_button.clicked = False
        pygame.display.update()

    def check_saves(self):
        """Добавляет массив кнопок в соответствии с файлами в 'saves'"""
        i = 200
        j = 0
        for file in self.files:
            self.saves.append(Button(350, i, 1, file))
            i += 200
            j += 1

    def in_saves_activity(self):
        f1 = pg.font.Font('DePixel/DePixelSchmal.ttf', 60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game_status = GameStatus.in_main_menu
        self.screen.blit(self.background, (0, 0))
        i = 220
        for k in range(len(self.saves)):
            self.saves[k].draw_on(self.screen)
            i += 200
            if self.saves[k].collide(self.screen):
                self.download_game(self.files[k])
                self.game_status = GameStatus.in_game
        pygame.display.update()

    def save_game(self, name):
        """Сохраняет мир в файл"""
        file = open(f'saves/{name}', 'wb')
        try:
#            for chunks in self.world.map:
#                for rows in chunks:
#                    for block in rows:
#                        file.write(f'{block.x}_{block.y}_{block.type} ')
#                    file.write('$')
#                file.write('%')
            pickled_map = []
            for i in range(len(self.world.map)):
                pickled_map.append([])
                for j in range(len(self.world.map[i])):
                    pickled_map[i].append([])
                    for k in range(len(self.world.map[i][j])):
                        pickled_block = PickledBlock(self.world.map[i][j][k].x, self.world.map[i][j][k].y, self.world.map[i][j][k].type)
                        pickled_map[i][j].append(pickled_block)
            pickle.dump(pickled_map, file)
        finally:
            file.close()

    def download_game(self, name):
        """Скачивает мир из файла"""
#        i = 0
#        j = 0
#        k = 0
        file = open(f'saves/{name}', 'rb')
        try:
#            text = file.read()
#            text = text.split('%')
#            for chunks in text:
#                chunks = chunks.split('$')
#                for string in chunks:
#                    string = string.split()
#                    for ministring in string:
#                       ministring = ministring.split('_')
 #                       self.world.map[k][i][j] = Block(float(ministring[0]), float(ministring[1]), int(float(ministring[2])))
 #                       j += 1
 #                   j = 0
  #                  i += 1
   #             i = 0
    #            k += 1
            map_converted = pickle.load(file)
            for i in range(len(map_converted)):
                for j in range(len(map_converted[i])):
                    for k in range(len(map_converted[i][j])):
                        self.world.map[i][j][k] = Block(map_converted[i][j][k].x, map_converted[i][j][k].y, map_converted[i][j][k].type)
        finally:
            file.close()

    def event_handler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.finished = True
            if event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT:
                self.stop_break_block()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game_status = GameStatus.in_pause

        if self.game_status == GameStatus.in_game and pg.mouse.get_pressed()[0]:
            chunk, destroy_x, destroy_y = self.world.get_block(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            self.break_block(chunk, destroy_x, destroy_y)
        self.world_move_general(pg.key.get_pressed())
        self.hero.set_animation(self.world.vx)

    def run(self):
        pg.font.init()
        self.check_saves()
        while not self.finished:
            if self.game_status == GameStatus.in_main_menu:
                self.main_menu_activity()
            if self.game_status == GameStatus.in_saves:
                self.in_saves_activity()
            if self.game_status == GameStatus.in_game:
                self.clock.tick(30)
                self.event_handler(pygame.event.get())
                self.drawer.update_screen(self.world.map, self.hero, self.inventory)
            if self.game_status == GameStatus.in_pause:
                self.pause_activity()


if __name__ == "__main__":
    Game().run()
