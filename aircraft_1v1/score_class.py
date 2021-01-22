#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : score_class.py
# Create date : 2020-12-14 06:06
# Modified date : 2020-12-14 06:11
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import pygame as pg

SCORE = 0

class Score(pg.sprite.Sprite):
    """ to keep track of the score.
    """

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = pg.Color("white")
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        """ We only update the score in update() when it has changed.
        """
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)

