import pygame as pg
import os


def music_play(song):
    _path = os.path.join('resources', 'snd', song)
    pg.mixer.music.load(_path)
    pg.mixer.music.play(-1)


def music_stop():
    pg.mixer.music.stop()


def eat_apple():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'eatapple.ogg'))
    sound.play()


def begin():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'beginning.ogg'))
    sound.play()


def game_over():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'gameover.ogg'))
    sound.play()


def xplode():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'explode.ogg'))
    sound.play()


def bomb():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'explode_bomb.ogg'))
    sound.play()


def scream():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'scream.ogg'))
    sound.play()


def bling():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'bling.ogg'))
    sound.play()


def text():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'text.ogg'))
    sound.play()


def startgame():
    sound = pg.mixer.Sound(os.path.join('resources', 'snd', 'startgame.ogg'))
    sound.play()



