import os
import pygame as pg
import glob

import constants

pg.display.init()
video = pg.display
screen = video.set_mode(constants.display_size)

""" Preloads images and parameters """
images = glob.glob('*.png')
image_cache = {}


def get_image(path):
    img = image_cache.get(path)
    path = os.path.join('resources', 'img', img)
    if img not in image_cache:
        image_cache[path] = pg.image.load(path)
    rect = img.get_rect()
    size = img.get_size()
    return img, rect, size


for pic in images:
    get_image(pic)

# Use these manually until I figure out a better solution
img_background = pg.image.load(os.path.join('resources', 'img', 'background.png')).convert()
level_size = img_background.get_size()
level_rect = img_background.get_rect()
img_title_screen = pg.image.load(os.path.join('resources', 'img', 'title.png')).convert()
img_bomb = pg.image.load(os.path.join('resources', 'img', 'bomb.png')).convert_alpha()
bomb_size = img_bomb.get_size()
img_apple = pg.image.load(os.path.join('resources', 'img', 'apple.png')).convert_alpha()
apple_size = img_apple.get_size()
img_head = pg.image.load(os.path.join('resources', 'img', 'snakehead.png')).convert_alpha()
img_body = pg.image.load(os.path.join('resources', 'img', 'snakebody.png')).convert()
img_heart = pg.image.load(os.path.join('resources', 'img', 'heart.png')).convert_alpha()
img_heart = pg.transform.scale(img_heart, (20, 20))
img_dog = pg.image.load(os.path.join('resources', 'img', 'bruh.png')).convert()
img_dog = pg.transform.scale(img_dog, (480, 440))
img_dog_neg = pg.image.load(os.path.join('resources', 'img', 'bruh_neg.png')).convert()
img_dog_neg = pg.transform.scale(img_dog_neg, (480, 440))
img_explosion = pg.image.load(os.path.join('resources', 'img', 'explosion.png')).convert_alpha()
img_explosion = pg.transform.scale2x(img_explosion)
explosion_size = img_explosion.get_size()
img_bullet = pg.image.load(os.path.join('resources', 'img', 'bullet.png')).convert_alpha()
img_time_up = pg.image.load(os.path.join('resources', 'img', 'time_up.png')).convert()
