#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : funcs.py
# Create date : 2020-12-27 00:16
# Modified date : 2021-01-22 00:00
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################
import os
import random
import pygame as pg
from explosion_class import Explosion
from missile_class import Missile
from aircraft_class import Aircraft

import etc
import math

import pylog

def load_image(a_file):
    """ loads an image, prepares it for play
    """
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    a_file = os.path.join(main_dir, "data", a_file)
    try:
        surface = pg.image.load(a_file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (a_file, pg.get_error()))
    return surface.convert()

def check_missile_hit_aircraft(a_aircraft, missiles):
    for a_missile in pg.sprite.spritecollide(a_aircraft, missiles, False):
        if a_missile.side != a_aircraft.side:
            Explosion(a_missile)
            Explosion(a_aircraft)
            a_aircraft.kill()

#   def check_shots_hit_aliens(shots, aliens, boom_sound, a_score):
#       # See if shots hit the aliens.
#       for alien in pg.sprite.groupcollide(shots, aliens, 1, 1).keys():
#           if pg.mixer:
#               boom_sound.play()
#           Explosion(alien)
#           #SCORE = SCORE + 1
#           a_score += 1
#       return a_score

def handle_player_input(keystate, a_game_dic):
    # handle player input
    red_firing_a_missile = keystate[pg.K_k]
    blue_firing_a_missile = keystate[pg.K_l]

    red_aircraft = a_game_dic["object_dic"]["red_aircraft"]
    a_action =a_game_dic["action"]
    if a_action == 1:
        red_firing_a_missile = 1

    handle_a_aircraft(red_aircraft, red_firing_a_missile)

    blue_aircraft = a_game_dic["object_dic"]["blue_aircraft"]
    distance = get_two_object_distance(red_aircraft, blue_aircraft)
    if distance < blue_aircraft.missile_range:
        blue_firing_a_missile = 1

    handle_a_aircraft(blue_aircraft, blue_firing_a_missile)

def get_two_object_distance(a_obj, another_obj):
    delta_x = (a_obj.rect.centerx - another_obj.rect.centerx)
    delta_y = (a_obj.rect.centery - another_obj.rect.centery)

    return math.sqrt(delta_x*delta_x + delta_y*delta_y)

def handle_a_aircraft(a_aircraft, is_firing):
    if is_firing:
        a_aircraft.fire()
    a_aircraft.reloading = is_firing

def check_finish_event(event_lt):
    for event in event_lt:
        if event.type == pg.QUIT:
            return True
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            return True

    return False

def get_observation(a_game_dic):
    red_aircraft = a_game_dic["object_dic"]["red_aircraft"]
    blue_aircraft = a_game_dic["object_dic"]["blue_aircraft"]

    distance = get_two_object_distance(red_aircraft, blue_aircraft)
    can_hit = 0
    if distance < red_aircraft.missile_range:
        can_hit = 1

    can_be_hited = 0
    if distance < blue_aircraft.missile_range:
        can_be_hited = 1

    a_observation = [
    red_aircraft.missile_num,
    blue_aircraft.missile_num,
    int(distance),
    can_hit,
    can_be_hited
    ]
    return a_observation

def run_a_step(a_game_dic):
    red_aircraft = a_game_dic["object_dic"]["red_aircraft"]
    blue_aircraft = a_game_dic["object_dic"]["blue_aircraft"]
    missiles = a_game_dic["object_dic"]["missiles"]
    keystate = pg.key.get_pressed()
    handle_player_input(keystate, a_game_dic)

    check_missile_hit_aircraft(blue_aircraft, missiles)
    check_missile_hit_aircraft(red_aircraft, missiles)

    a_observation = get_observation(a_game_dic)

    a_reward = 0
    a_action =a_game_dic["action"]
    if a_action == 1:
        a_reward -= 0.01

    if not blue_aircraft.alive():
        a_reward += 1.0

    if not red_aircraft.alive():
        a_reward -= 1.0

    return a_observation, a_reward

def get_a_screen():
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(etc.SCREENRECT.size, winstyle, 32)
    a_screen = pg.display.set_mode(etc.SCREENRECT.size, winstyle, bestdepth)
    return a_screen, bestdepth

def create_a_background(a_screen):
    screen_rect = etc.SCREENRECT
    a_background = pg.Surface(etc.SCREENRECT.size)
    # create the background, tile the bgd image
    bgdtile = load_image("background.gif")
    for x in range(0, screen_rect.width, bgdtile.get_width()):
        a_background.blit(bgdtile, (x, 0))
    a_screen.blit(a_background, (0, 0))
    pg.display.flip()
    return a_background

