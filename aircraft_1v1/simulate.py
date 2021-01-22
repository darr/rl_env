#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : simulate.py
# Create date : 2020-12-30 22:25
# Modified date : 2021-01-21 18:16
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import random
from random import randint
import os

# import basic pygame modules
import pygame as pg
from aircraft_class import Aircraft
from explosion_class import Explosion
from missile_class import Missile

from funcs import load_image

from funcs import check_finish_event
from funcs import run_a_step
from funcs import get_a_screen
from funcs import create_a_background
from funcs import get_observation
from funcs import get_two_object_distance

from init_funcs import create_red_aircraft
from init_funcs import create_blue_aircraft

import etc
import time
import pylog



def get_a_action(a_actor, a_observation):
    a_action = a_actor.exploration(a_observation)
    return a_action

def get_a_inference_action(a_actor, a_observation):
    a_action = a_actor.inference(a_observation)
    return a_action

def update_a_data(a_actor, a_observation, a_action, a_reward):
    a_actor.update_critic(a_observation, a_action, a_reward)

def run_the_game(a_game_dic):

    a_actor = a_game_dic["model_dic"]["actor"]

    red_aircraft = a_game_dic["object_dic"]["red_aircraft"]
    blue_aircraft = a_game_dic["object_dic"]["blue_aircraft"]

    if etc.RENDER:
        a_screen = a_game_dic["screen_dic"]["a_screen"]
        background = a_game_dic["screen_dic"]["background"]

    all_objects = a_game_dic["object_dic"]["all_objects"]
    clock= a_game_dic["clock"]

    a_observation = get_observation(a_game_dic)
    start_time = time.time()
    step_count = 0
    a_distance = get_two_object_distance(red_aircraft, blue_aircraft)
    while blue_aircraft.alive() and red_aircraft.alive() and a_distance > 10:
        a_distance = get_two_object_distance(red_aircraft, blue_aircraft)
        event_lt = pg.event.get()
        if check_finish_event(event_lt): break

        if etc.RENDER:
            all_objects.clear(a_screen, background)
        all_objects.update()

        if step_count % 10 == 0:
            if a_game_dic["state"] == "train":
                a_action = get_a_action(a_actor, a_observation)
            else:
                a_action = get_a_inference_action(a_actor, a_observation)

            a_game_dic["action"] = a_action
            step_start = time.time()
            new_observation, a_reward = run_a_step(a_game_dic)
            update_a_data(a_actor, a_observation, a_action, a_reward)
            a_observation = new_observation
        step_end = time.time()
        step_duration = step_end - step_start

        #pylog.info("step_count:%s step_duration:%.5fs observation:%s action:%s reward:%s" % (step_count, step_duration, a_observation, a_action, a_reward))
        if etc.RENDER:
            dirty = all_objects.draw(a_screen)
            pg.display.update(dirty)

        step_count += 1

        clock.tick(etc.CLOCK_FREQUENCY)

    end_time = time.time()
    duration = end_time - start_time
    #pylog.info("step_count:%s duration:%.2fs" % (step_count, duration))

def init_the_game(winstyle):
    pg.init()
    a_screen, bestdepth = get_a_screen()
    if etc.RENDER:
        background = create_a_background(a_screen)

    a_img = load_image("red_cross.gif")
    blue_img = load_image("blue_cross.gif")
    Explosion.images = [a_img, pg.transform.flip(a_img, 1, 1), blue_img]

    Aircraft.images = [load_image("red_aircraft.gif"), load_image("blue_aircraft.gif")]
    Missile.images = [load_image("red_missile.gif"), load_image("blue_missile.gif")]


    # decorate the game window
    #icon = pg.transform.scale(Alien.images[0], (32, 32))
    #pg.display.set_icon(icon)

    pg.display.set_caption("aircraft 1v1")
    pg.mouse.set_visible(0)

    missiles = pg.sprite.Group()
    aircrafts = pg.sprite.Group()
    all_objects = pg.sprite.RenderUpdates()

    Aircraft.containers = aircrafts, all_objects
    Missile.containers = missiles, all_objects
    Explosion.containers = all_objects

    clock = pg.time.Clock()

    # initialize our starting sprites

    red_aircraft = create_red_aircraft()
    blue_aircraft = create_blue_aircraft()

    #a_actor = Actor()

    screen_dic = {}
    if etc.RENDER:
        screen_dic["a_screen"] = a_screen
        screen_dic["background"] = background

    object_dic = {}
    object_dic["red_aircraft"] = red_aircraft
    object_dic["blue_aircraft"] = blue_aircraft
    object_dic["all_objects"] = all_objects
    object_dic["missiles"] = missiles
    object_dic["aircrafts"] = aircrafts


    a_game_dic = {}
    a_game_dic["screen_dic"] = screen_dic
    a_game_dic["object_dic"] = object_dic
    a_game_dic["clock"] = clock

    return a_game_dic
