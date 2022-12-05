import pygame
from constants import *


class Button:
    """Класс для кнопок"""
    def __init__(self, x, y, image, scale):
        button_width = image.get_width()
        button_height = image.get_height()
        self.image = pygame.transform.scale(image, (int(button_width * scale), int(button_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """Рисует кнопку"""
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


def button_main():
    """Функция для тестирования"""
    start_button = Button(400, 300, start_img, 0.5)
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Buttons')
    run = True
    while run:
        screen.fill((0, 0, 0))
        if start_button.draw(screen):
            print("Hello")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


if __name__ == "__main__":
    button_main()





