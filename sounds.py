import pygame as pg

pg.mixer.init()


def load_music():
    pg.mixer.music.load('the_reckoning.ogg')


def music_play():
    load_music()
    pg.mixer.music.play(-1)


def music_stop():
    pg.mixer.music.stop()


def eat_apple():
    sound = pg.mixer.Sound('eatapple.ogg')
    sound.play()


def begin():
    sound = pg.mixer.Sound('beginning.ogg')
    sound.play()


def game_over():
    sound = pg.mixer.Sound('gameover.ogg')
    sound.play()


def xplode():
    sound = pg.mixer.Sound('explode.ogg')
    sound.play()


def bomb():
    sound = pg.mixer.Sound('explode_bomb.ogg')
    sound.play()
