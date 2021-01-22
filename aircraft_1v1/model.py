#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : model.py
# Create date : 2021-01-07 02:12
# Modified date : 2021-01-08 22:24
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

from random import randint
import random
import pylog
import json
import pyfile

def bernoulli(p):
    if random.random() > p:
        return 1
    return 0

class Actor():
    def __init__(self):
        self.a_critic = Critic()

    def inference(self, a_observation):
        a_state_dic = self.a_critic.query_a_observation(a_observation)
        a_action = 0
        if a_state_dic:
            pylog.info("state:%s a_state_dic:%s" % (a_observation, a_state_dic))
            max_value = None
            select_key = None
            for key in a_state_dic:
                a_value = a_state_dic[key]["avg_reward"]
                if max_value == None:
                    max_value = a_value
                    select_key = key
                else:
                    if a_value > max_value:
                        max_value = a_value
                        select_key = key

            a_action = select_key
        #else:
        #    a_action = bernoulli(0.005)

        return a_action

    def exploration(self, a_observation):
        a_state_dic = self.a_critic.query_a_observation(a_observation)
        epsilon = 0.01
        is_use = bernoulli(epsilon)
        a_action = 0

        if a_observation[0] == 1 and a_observation[2] <= 200:
            a_action = bernoulli(0.05)

        return a_action

    def update_critic(self, a_observation, a_action, a_reward):
        #self.a_critic.add_item(a_observation, a_action, a_reward)
        self.a_critic.append_item_to_episode(a_observation, a_action, a_reward)

    def update_reward(self):
        self.a_critic.update_current_episode_reward()

    def write_observation_dic(self):
        ret = json.dumps(self.a_critic.observation_dic, indent=2)
        pyfile.write_file(ret, "observation_dic.json","./")

class Critic():
    def __init__(self):
        self.observation_data_list = []
        self.observation_dic = {}
        self.current_episode = []
        self.episode_lt = []

    def append_item_to_episode(self, a_observation, a_action, a_reward):
        item = [a_observation, a_action, a_reward]
        self.current_episode.insert(0, item)
    
    def update_current_episode_reward(self):
        gama = 0.95

        a_reward = 0
        for item in self.current_episode:
            #pylog.info("before:%s" % item)
            a_reward = item[2] + gama * a_reward
            item[2] = a_reward
            #pylog.info("after:%s" % item)
            self.add_item(item[0],item[1],item[2])

        self.episode_lt.append(self.current_episode)
        self.current_episode = []

    def add_item(self, a_observation, a_action, a_reward):
        a_item = [a_observation, a_action, a_reward]

        a_state_dic = self.observation_dic.get(str(a_observation), {})
        a_action_dic = a_state_dic.get(a_action, {})
        if a_action_dic:
            reward_sum = a_action_dic["avg_reward"] * a_action_dic["count"]
            a_action_dic["count"] += 1
            a_action_dic["avg_reward"] = (reward_sum + a_reward) / a_action_dic["count"]
        else:
            a_action_dic["count"] = 1
            a_action_dic["avg_reward"] = a_reward

        a_state_dic[a_action] = a_action_dic
        self.observation_dic[str(a_observation)] = a_state_dic

        #pylog.info(a_item)
        self.observation_data_list.append(a_item)

    def query_a_observation(self, a_observation):
        a_state_dic = self.observation_dic.get(str(a_observation), {})
        return a_state_dic
