#!/usr/bin/python
# -*- cme : aircraft_class.py
# Create date : 2020-12-31 04:42
# Modified date : 2021-01-02 05:25
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import random
import pygame as pg
from dl_object import DLObject
from missile_class import Missile
import pylog

def create_a_missile(a_aircraft):
    location = a_aircraft.gunpos()
    heading = a_aircraft.theta
    if a_aircraft.missile_num > 0 and not a_aircraft.reloading:
        a_aircraft.missile_num -= 1
        a_dic = {}
        a_dic["side"] = a_aircraft.side
        a_dic["theta"] = a_aircraft.theta
        a_dic["speed"] = a_aircraft.missile_speed

        if a_aircraft.side == "red":
            a_dic["image_index"] = 0
        else:
            a_dic["image_index"] = 1

        a_dic["top"] = a_aircraft.rect.top
        a_dic["left"] = a_aircraft.rect.left
        a_dic["pos"] = location
        a_dic["range"] = a_aircraft.missile_range

        a_missile = Missile(a_dic)
    else:
        pass
        #pylog.info("there are no missiles")

class Aircraft(pg.sprite.Sprite, DLObject):
    """ An alien space ship. That slowly moves down the screen.
    """

    speed = 1
    animcycle = 12
    images = []

    def __init__(self, screen_rect, a_dic):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.reloading = 0
        self.init_the_object(a_dic)
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.top = self.top
        self.rect.left = self.left
        self.screen_rect = screen_rect
        self.image = pg.transform.rotate(self.image, self.theta)
        #self.facing = random.choice((-1, 1)) * self.speed
        self.facing = self.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = screen_rect.right

    def init_the_object(self, a_dic):
        super(Aircraft, self).init_the_object(a_dic)
        a_key_list = ["side", "missile_num", "theta", "speed", "image_index", "top", "left", "missile_range", "missile_speed"]
        self.init_with_a_key_list(a_dic, a_key_list)

    def update(self):

        self.rect.move_ip(self.facing, 0)

        if not self.screen_rect.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(self.screen_rect)
        self.frame = self.frame + 1

        self.image = self.images[self.image_index]
        self.image = pg.transform.rotate(self.image, self.theta)

    def gunpos(self):
        #pos = self.facing * self.gun_offset + self.rect.centerx
        #return pos, self.rect.top
        return self.rect.centerx, self.rect.centery

    def fire(self):
        create_a_missile(self)
    
