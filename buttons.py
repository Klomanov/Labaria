import pygame

import visual
from constants import *


class Button(visual.DrawableObject):
    """Класс для кнопок"""
    def __init__(self, x, y, scale, text):
        self.button_width = save_img_off.get_width()
        self.button_height = save_img_on.get_height()
        self.image_off = pygame.transform.scale(save_img_off, (int(self.button_width * scale), int(self.button_height * scale)))
        self.image_on = pygame.transform.scale(save_img_on, (int(self.button_width * scale), int(self.button_height * scale)))
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
    LABaria = pygame.transform.scale(LABaria_pict, (1200, 800))
    start_button = Button(350, 200, 1, 'Start')
    load_save_button = Button(350, 400, 1, 'Load save')
    exit_button = Button(350, 600, 1, 'Exit')
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Buttons')
    run = True
    while run:
        screen.blit(LABaria, (0, 0))
        start_button.draw_on(screen)
        exit_button.draw_on(screen)
        load_save_button.draw_on(screen)
        if start_button.collide(screen):
            print("Hello")
        if exit_button.collide(screen):
            run = False
        if load_save_button.collide(screen):
            print("Привет")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if not pygame.mouse.get_pressed()[0]:
                start_button.clicked = False
                load_save_button.clicked = False
        pygame.display.update()


if __name__ == "__main__":
    button_main()





