#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : dl_object.py
# Create date : 2020-09-05 17:13
# Modified date : 2021-01-01 23:56
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

import uuid


class DLObject(object):

    def __init__(self):
        self.class_name = "%s" % self.__class__.__name__
        uid = "".join(str(uuid.uuid4()).split("-"))
        self.uid = uid

    def delete_self(self):
        pass

    def init_the_object(self, a_dic):
        pass

    def __repr__(self):
        return "'%s'" % self.uid

    def init_with_a_key_list(self, a_dic, a_key_list):
        for key in a_dic:
            if key in a_key_list:
                self.__dict__[key]= a_dic[key]

    def update_attr(self, **kwargs):
        update_dic = {k: v for k, v in kwargs.items() if k in self.__dict__.keys                                                                                            ()}
        self.__dict__.update(update_dic)
