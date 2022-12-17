import pygame

import visual
from constants import *


class Button(visual.DrawableObject):
    """Класс для кнопок"""
    def __init__(self, x, y, scale, text):
        self.button_width = button_img_on.get_width()
        self.button_height = button_img_on.get_height()
        self.image_off = pygame.transform.scale(button_img_off, (int(self.button_width * scale), int(self.button_height * scale)))
        self.image_on = pygame.transform.scale(button_img_on, (int(self.button_width * scale), int(self.button_height * scale)))
        self.rect = self.image_off.get_rect()
        self.rect.topleft = (x, y)
        self.collided = False
        self.clicked = False
        self.text = text
        self.f1 = pg.font.Font('DePixel/DePixelBreit.ttf', 60)

    def draw_on(self, surface):
        """Рисует кнопку"""
        if self.collided:
            surface.blit(self.image_on, (self.rect.x, self.rect.y))
            left_pos = 600-self.f1.render(self.text, False, (0, 0, 0)).get_width()/2
            y_pos = self.rect.y + (self.button_height - self.f1.render(self.text, False, (0, 0, 0)).get_height())/2
            surface.blit(self.f1.render(self.text, False, (0, 0, 0)), (left_pos, y_pos))
        else:
            surface.blit(self.image_off, (self.rect.x, self.rect.y))
            left_pos = 600-self.f1.render(self.text, False, (0, 0, 0)).get_width()/2
            y_pos = self.rect.y + (self.button_height - self.f1.render(self.text, False, (0, 0, 0)).get_height())/2
            surface.blit(self.f1.render(self.text, False, (0, 0, 0)), (left_pos, y_pos))

    def collide(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.collided = True
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if not self.rect.collidepoint(pos):
            self.collided = False
        return action


def button_main():
    """Функция для тестирования"""
    pg.font.init()
    font = pg.font.Font('DePixel/DePixelBreit.ttf', 60)
    f1 = font.render('Enter save name:', False, (0, 0, 0))
    x_pos = 600 - f1.get_width()/2
    y_pos = 400 + (100 - f1.get_height())/2
    enter_row = pygame.transform.scale(enter_row_img, (700, 100))
    LABaria = pygame.transform.scale(LABaria_pict, (1200, 800))
    start_button = Button(350, 200, 1, 'Start')
    load_save_button = Button(350, 400, 1, 'Load save')
    exit_button = Button(350, 600, 1, 'Exit')
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Buttons')
    txt_button = Button(350, 250, 1, '.txt')
    pickle_button = Button(350, 450, 1, 'Pickle')
    run = True
    test = 'menu'
    text = ''
    save_type = None
    while run:
        screen.blit(LABaria, (0, 0))
        if test == 'menu':
            start_button.draw_on(screen)
            exit_button.draw_on(screen)
            load_save_button.draw_on(screen)
            if start_button.collide(screen):
                print("Перерыв на обед.")
            if exit_button.collide(screen):
                run = False
            if load_save_button.collide(screen):
                test = 'test'
            if not pygame.mouse.get_pressed()[0]:
                start_button.clicked = False
                load_save_button.clicked = False
        if test == 'test':
            txt_button.draw_on(screen)
            pickle_button.draw_on(screen)
            for event in pygame.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    test = 'menu'
                if event.type == pygame.QUIT:
                    run = False
            if txt_button.collide(screen):
                save_type = '.txt'
                test = 'save'
            if pickle_button.collide(screen):
                save_type = 'pickle'
                test = 'save'
        if test == 'save':
            screen.blit(f1, (x_pos, 250))
            screen.blit(enter_row, (250, 400))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    test = 'test'
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE and len(text) > 0:
                        text = text[:-1]
                    else:
                        text += event.unicode
            screen.blit(font.render(text, False, (0, 0, 0)), (270, y_pos))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


if __name__ == "__main__":
    button_main()





