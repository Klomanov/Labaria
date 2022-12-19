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
from world_cutted import *


class Game:
    def __init__(self):
        pg.init()
        self.finished = False
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.drawer = visual.Drawer(self.screen)
        self.clock = pg.time.Clock()
        self.world = None
        self.hero = None
        self.inventory = None
        self.background = pygame.transform.scale(LABaria_pict, (1200, 800))
        self.start_button = Button(350, 200, 1, 'Start')
        self.load_save_button = Button(350, 400, 1, 'Load save')
        self.exit_button = Button(350, 600, 1, 'Exit')
        self.game_status = GameStatus.in_main_menu
        self.back_button = Button(350, 200, 1, 'Back')
        self.save_game_button = Button(350, 400, 1, 'Save game')
        self.back_to_main_menu_button = Button(350, 600, 1, 'To menu')
        self.enter_row = pygame.transform.scale(enter_row_img, (700, 100))
        self.files = os.listdir('saves')
        self.saves = []
        self.need_to_blit = True
        self.text = ''

    def world_move_general(self, keys):
        """Функция, которая осуществляет движение мира с помощью других функций в world.py"""
        for chunk in range(len(self.world.map)):
            if visual.is_chunk_on_screen(self.world.map[chunk]):
                if chunk == chunk_num - 1:
                    self.world.move_left_chunk_to_right()
                if chunk == 0:
                    self.world.move_right_chunk_to_left()
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
                        if block.type in block_resource:
                            self.inventory.increase(block_resource[block.type])
                            self.hero.selected_item_type = block_resource[block.type]
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

    def build_block(self, chunk, x, y):
        block = self.world.map[chunk][y][x]
        if block.type == BlockType.sky or block.type == BlockType.bg_stone or block.type == BlockType.bg_dirt:
             if (block.x >= self.hero.x + 0.75*hero_width or self.hero.x - 0.75*hero_width >= block.x)\
                    or (block.y >= self.hero.y + 0.75*hero_height or self.hero.y - 0.75*hero_height >= block.y):
                if self.hero.selected_item_type is not None and self.hero.selected_item_type in self.inventory.resources:
                    if (block.x - self.hero.x) ** 2 + (block.y - self.hero.y) ** 2 <= hero_dig_range ** 2:
                        self.world.place_block(chunk, x, y, resource_block[self.hero.selected_item_type])
                        self.inventory.decrease(self.hero.selected_item_type)

    def main_menu_activity(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
            if not pg.mouse.get_pressed()[0] and self.exit_button.clicked:
                self.exit_button.clicked = False
                self.start_button.clicked = False
                self.load_save_button.clicked = False
        self.back_to_main_menu_button.clicked = False
        self.screen.blit(self.background, (0, 0))
        self.start_button.draw_on(self.screen)
        self.exit_button.draw_on(self.screen)
        self.load_save_button.draw_on(self.screen)
        if self.start_button.collide():
            self.game_status = GameStatus.in_game
            self.world = World(seed=-1)
            self.hero = Hero(screen_width//2, screen_height//2)
            self.world.move(-world_size_x//3*block_size, 0)
            self.inventory = Inventory(self.screen)
        if self.exit_button.collide():
            self.finished = True
        if self.load_save_button.collide():
            self.game_status = GameStatus.in_saves
            for save in self.saves:
                save.clicked = True
            self.load_save_button.clicked = False
        pygame.display.update()

    def pause_activity(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game_status = GameStatus.in_game
        self.back_button.clicked = False
        self.start_button.clicked = False
        if self.need_to_blit:
            back1 = self.background
            back1.set_alpha(50)
            self.screen.blit(back1, (0, 0))
            self.need_to_blit = False
        self.back_button.draw_on(self.screen)
        if self.back_button.collide():
            self.game_status = GameStatus.in_game
        self.back_to_main_menu_button.draw_on(self.screen)
        if self.back_to_main_menu_button.collide():
            self.game_status = GameStatus.in_main_menu
            self.exit_button.clicked = True
            self.load_save_button.clicked = True
            self.start_button.clicked = True
        self.save_game_button.draw_on(self.screen)
        if self.save_game_button.collide():
            self.need_to_blit = True
            self.drawer.update_screen(self.world.map, self.hero, self.inventory)
            self.game_status = GameStatus.in_enter_save

        pygame.display.update()

    def enter_save(self, text):
        self.save_game_button.clicked = False
        font = pg.font.Font('DePixel/DePixelBreit.ttf', 60)
        f1 = font.render('Enter save name:', False, (0, 0, 0))
        x_pos = 600 - f1.get_width() / 2
        y_pos = 400 + (100 - f1.get_height()) / 2
        if self.need_to_blit:
            back1 = self.background
            back1.set_alpha(50)
            self.screen.blit(back1, (0, 0))
            self.need_to_blit = False
        self.screen.blit(f1, (x_pos, 250))
        self.screen.blit(self.enter_row, (250, 400))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finished = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game_status = GameStatus.in_pause
                self.drawer.update_screen(self.world.map, self.hero, self.inventory)
                self.need_to_blit = True
                text = ''
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE and len(text) > 0:
                    text = text[:-1]
                elif event.key == pg.K_RETURN:
                    if text in self.files and (text != self.search_oldest_file() or len(self.files) < 3):
                        text += '(1)'
                        if text in self.files:
                            text = text[:-3]
                            text += '(2)'
                            if text in self.files:
                                text = text[:-3]
                    self.save_game(text)
                    self.game_status = GameStatus.in_pause
                    self.drawer.update_screen(self.world.map, self.hero, self.inventory)
                    self.need_to_blit = True
                    text = ''
                else:
                    text += event.unicode
        self.text = text
        self.screen.blit(font.render(self.text, False, (0, 0, 0)), (270, y_pos))
        pygame.display.update()

    def check_saves(self):
        """Добавляет массив кнопок в соответствии с файлами в 'saves'"""
        self.saves = []
        i = 200
        j = 0
        for file in self.files:
            self.saves.append(Button(350, i, 1, file))
            i += 200
            j += 1
        if len(os.listdir('saves')) > 3: #удаляет самый старый файл
            oldest_file_path = self.search_oldest_file()
            if os.path.isfile(f'saves/{oldest_file_path}'):
                os.remove(f'saves/{oldest_file_path}')

    def search_oldest_file(self):
        min_time = None
        min_time_path = ''
        for file in self.files:
            if min_time is None:
                min_time = os.path.getmtime(f'saves/{file}')
                min_time_path = file
            elif os.path.getmtime(f'saves/{file}') < min_time:
                min_time = os.path.getmtime(f'saves/{file}')
                min_time_path = file
        return min_time_path

    def in_saves_activity(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.game_status = GameStatus.in_main_menu
            if not pg.mouse.get_pressed()[0]:
                for save in self.saves:
                    save.clicked = False
        self.save_game_button.clicked = False
        self.back_to_main_menu_button.clicked = False
        self.screen.blit(self.background, (0, 0))
        i = 220
        for k in range(len(self.saves)):
            self.saves[k].draw_on(self.screen)
            i += 200
            if self.saves[k].collide():
                self.download_game(self.files[k])
                self.game_status = GameStatus.in_game
        pygame.display.update()

    def save_game(self, name):
        """Сохраняет мир в файл"""
        file = open(f'saves/{name}', 'wb')
        try:
            pickled_file = []
            pickled_map = PickledWorld(self.world.map)
            pickled_file.append(pickled_map)
            pickled_inventory = PickledInventory(self.inventory.resources)
            pickled_file.append(pickled_inventory.resources)
            pickle.dump(pickled_file, file)

        finally:
            file.close()

    def download_game(self, name):
        """Скачивает мир из файла"""
        self.world = World(file_name=name)
        self.inventory = Inventory(self.screen, name)
        self.hero = Hero(screen_width // 2, screen_height // 2)

    def event_handler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.finished = True
            if event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT:
                self.stop_break_block()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_RIGHT:
                chunk, place_x, place_y = self.world.get_block(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                if chunk is not None:
                    self.build_block(chunk, place_x, place_y)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and not self.inventory.flag:
                    self.game_status = GameStatus.in_pause
                elif event.key == pg.K_ESCAPE and self.inventory.flag:
                    self.inventory.flag = False

        for i in range(len(keys)):
            if pg.key.get_pressed()[keys[i]]:
                if len(self.inventory.resources) >= i + 1:
                    self.hero.selected_item_type = list(self.inventory.resources.keys())[i]

        if self.game_status == GameStatus.in_game and pg.mouse.get_pressed()[0]:
            chunk, destroy_x, destroy_y = self.world.get_block(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            if chunk is not None:
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
                self.clock.tick(60)
                self.need_to_blit = True
                self.event_handler(pygame.event.get())
                self.drawer.update_screen(self.world.map, self.hero, self.inventory)
            if self.game_status == GameStatus.in_pause:
                self.files = os.listdir('saves')
                self.check_saves()
                self.pause_activity()
            if self.game_status == GameStatus.in_enter_save:
                self.enter_save(self.text)


if __name__ == "__main__":
    Game().run()
