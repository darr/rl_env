#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : missile_class.py
# Create date : 2020-12-14 06:03
# Modified date : 2021-01-06 20:45
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import math
import pygame as pg
from explosion_class import Explosion
from dl_object import DLObject
import pylog

class Missile(pg.sprite.Sprite, DLObject):
    """ a bullet the Player sprite fires.
    """

    images = []

    def __init__(self, a_dic):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.init_the_object(a_dic)

        self.image = self.images[self.image_index]
        self.image = pg.transform.rotate(self.image,self.theta)
        self.rect = self.image.get_rect(midbottom=self.pos)
        self.start_center = (self.rect.centerx, self.rect.centery)

    def init_the_object(self, a_dic):
        super(Missile, self).init_the_object(a_dic)
        a_key_list = ["side", "theta", "speed", "image_index", "top", "left", "pos", "range"]
        self.init_with_a_key_list(a_dic, a_key_list)

    def _get_move_position(self):
        x_delta = -1 * math.cos(math.radians(self.theta))*self.speed
        y_delta = -1 * math.sin(math.radians(self.theta))*self.speed
        return x_delta, y_delta

    def _cal_fly_distance(self):
        current_center = (self.rect.centerx, self.rect.centery)

        x_delta = self.start_center[0] - current_center[0]
        y_delta = self.start_center[1] - current_center[1]

        fly_distance = math.sqrt(x_delta*x_delta + y_delta*y_delta)
        return fly_distance

    def update(self):

        x_delta, y_delta = self._get_move_position()
        self.rect.move_ip(y_delta, x_delta)
        fly_distance = self._cal_fly_distance()
        if fly_distance > self.range:
            #pylog.info("fiy distance is :%s" % fly_distance)
            Explosion(self)
            self.kill()

        if self.rect.top <= 0:
            self.kill()

    def kill(self):
        #pylog.info("a missile is killed")
        super(Missile, self).kill()
