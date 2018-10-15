#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging as logger

#日志配置
logger.basicConfig(filename="../facereg.log",level=logger.INFO)

def debug(msg):
    logger.debug(msg)

def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def warn(msg):
    logger.warn(msg)

def error(msg):
    logger.error(msg)
