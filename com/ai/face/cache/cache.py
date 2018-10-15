#!/usr/bin/python
# -*- coding: UTF-8 -*-

def _init():
    global _cache_list
    _cache_list = []

def clear():
    _cache_list.clear()

def append(val):
    _cache_list.append(val)

def getCacheList():
    return _cache_list
