#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : explosion_class.py
# Create date : 2020-12-14 06:00
# Modified date : 2021-01-08 19:22
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import pygame as pg

class Explosion(pg.sprite.Sprite):
    """ An explosion. Hopefully the Alien and not the player!
    """

    defaultlife = 12
    animcycle = 3
    images = []

    def __init__(self, target):
        pg.sprite.Sprite.__init__(self, self.containers)
        if target.side == "red":
            self.image = self.images[0]
        else:
            self.image = self.images[2]
        self.rect = self.image.get_rect(center=target.rect.center)
        self.life = self.defaultlife

    def update(self):
        """ called every time around the game loop.

        Show the explosion surface for 'defaultlife'.
        Every game tick(update), we decrease the 'life'.

        Also we animate the explosion.
        """
        self.life = self.life - 1
        self.image = self.images[self.life // self.animcycle % 2]
        if self.life <= 0:
            self.kill()

