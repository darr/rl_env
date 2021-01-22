#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : init_funcs.py
# Create date : 2021-01-02 01:04
# Modified date : 2021-01-08 22:19
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import etc
from aircraft_class import Aircraft
from missile_class import Missile
import pylog

def create_red_aircraft():
    a_dic = {}
    a_dic["side"] = "red"
    a_dic["missile_num"] = 1
    a_dic["missile_range"] = 400
    a_dic["missile_speed"] = 5
    a_dic["theta"] = -90
    a_dic["speed"] = 1
    a_dic["image_index"] = 0
    a_dic["top"] = 200
    a_dic["left"] = 350
    a_aircraft = Aircraft(etc.SCREENRECT, a_dic)
    return a_aircraft

def create_blue_aircraft():
    #a_side = "blue"
    a_dic = {}
    a_dic["side"] = "blue"
    a_dic["missile_num"] = 1
    a_dic["missile_range"] = 200
    a_dic["missile_speed"] = 5
    a_dic["theta"] = 90
    a_dic["speed"] = 0
    a_dic["image_index"] = 1
    a_dic["top"] = 200
    a_dic["left"] = 850
    a_aircraft = Aircraft(etc.SCREENRECT, a_dic)
    return a_aircraft
