import pygame as pg
import colors

class Bullet(object):

    def __init__(self):
        self.image = pg.Surface([4,10])
        self.image.fill(colors.Black)

        self.rect = self.image.get_rect()

    def update(self):

        if
        self.rect.y