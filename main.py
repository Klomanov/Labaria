import pygame as pg
import visual


def main():

    pg.init()
    finished = False

    width = 1200
    height = 800
    screen = pg.display.set_mode((width, height))
    drawer = visual.Drawer(screen)
    clock = pg.time.Clock()

    while not finished:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
        drawer.update([], None)


if __name__ == "__main__":
    main()
