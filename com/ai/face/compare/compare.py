#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import logging as logger
class Compare:
    def __init__(self):
        pass

    def compare(self, d1, d2):
        # diff = 0
        # for i in range(len(d1)):
        #     diff += (d1[i] - d2[i])**2
        diff = np.sqrt(np.sum(np.square((d1 - d2))))
        return diff

