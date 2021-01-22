#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : run_game.py
# Create date : 2020-12-31 18:48
# Modified date : 2021-01-21 18:16
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import pygame as pg
from simulate import run_the_game
from simulate import init_the_game
from model import Actor
import time
import pylog
import etc
import sys

def do_eval(a_actor):
    etc.RENDER = True
    etc.CLOCK_FREQUENCY = 200
    winstyle=0
    start_time = time.time()
    count = 100
    while count:
        a_game_dic = init_the_game(winstyle)
        a_game_dic["state"] = "eval"

        model_dic = {}
        model_dic["actor"] = a_actor

        a_game_dic["model_dic"] = model_dic

        run_the_game(a_game_dic)
        a_actor.update_reward()
        pg.quit()
        count -= 1
    a_actor.write_observation_dic()
    end_time = time.time()
    pylog.info("spend time:%.2f " % (end_time-start_time))

def train(a_actor):
    winstyle=0
    count = 1000
    start_time = time.time()
    while count:

        pylog.info("train ep:%s" % count)
        a_game_dic = init_the_game(winstyle)
        a_game_dic["state"] = "train"

        model_dic = {}
        model_dic["actor"] = a_actor

        a_game_dic["model_dic"] = model_dic

        run_the_game(a_game_dic)
        a_actor.update_reward()
        pg.quit()
        count -= 1
    a_actor.write_observation_dic()
    end_time = time.time()
    pylog.info("spend time:%.2f " % (end_time-start_time))

def main(winstyle=0):
    a_actor = Actor()
    train(a_actor)
    do_eval(a_actor)

if __name__ == "__main__":
    main()
