import pygame as pg

pg.mixer.init()


def load_music():
    pg.mixer.music.load('resources/snd/the_reckoning.ogg')


def music_play():
    load_music()
    pg.mixer.music.play(-1)


def music_stop():
    pg.mixer.music.stop()


def eat_apple():
    sound = pg.mixer.Sound('resources/snd/eatapple.ogg')
    sound.play()


def begin():
    sound = pg.mixer.Sound('resources/snd/beginning.ogg')
    sound.play()


def game_over():
    sound = pg.mixer.Sound('resources/snd/gameover.ogg')
    sound.play()


def xplode():
    sound = pg.mixer.Sound('resources/snd/explode.ogg')
    sound.play()


def bomb():
    sound = pg.mixer.Sound('resources/snd/explode_bomb.ogg')
    sound.play()

def scream():
    sound = pg.mixer.Sound('resources/snd/scream.ogg')
    sound.play()

def bling():
    sound = pg.mixer.Sound('resources/snd/bling.ogg')
    sound.play()
