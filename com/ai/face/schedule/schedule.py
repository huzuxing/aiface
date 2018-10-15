#!/usr/bin/python
# -*- coding: UTF-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
import pymysql
import configparser
import numpy as np
import cache
import logger

# 读取配置文件
config = configparser.ConfigParser()
config.read("../schedule/config.ini")
scheduler = BackgroundScheduler()
class FaceDescriptorSchedule():
    def __init__(self):
        pass

    '''
    定义为私有方法
    '''
    def __get_all_facesdescriptor(self):
        host = config.get("db", "host")
        port = config.get("db", "port")
        user = config.get("db", "user")
        password = config.get("db", "password")
        db = config.get("db", "db")
        dbdialect = config.get("db", "dbdialect")
        try:
            connection = self.getConnection(dbdialect, host, port, user, password, db)
        except:
            logger.error("connect db failed")
            return
        try:
            with connection.cursor() as cursor:
                allFaceDescriptorsSql = "select * from t_face_descriptor"
                cursor.execute(allFaceDescriptorsSql)
                result = cursor.fetchall()
                if len(result) > 0:
                    # 清空缓存数据
                    cache.clear()
                    for t in result:
                        dict = {}
                        dict["employeeNo"]=t["employeeNo"]
                        descriptor = t["face_descriptor"]
                        descriptor = descriptor.split(",")
                        descriptor = [float(i) for i in descriptor]
                        numpyArray = np.array(descriptor)
                        dict["face_descriptor"] = numpyArray
                        cache.append(dict)
        except:
            logger.error("get data from db failed")
        finally:
            connection.close()

    def schedule(self, seconds):
        # 初始化缓存列表
        cache._init()
        # 间隔3秒钟执行一次
        scheduler.add_job(self.__get_all_facesdescriptor, 'interval', seconds=seconds)
        # 这里的调度任务是独立的一个线程
        try:
            scheduler.start()
        except:
            logger.error("scheduler starts failed")
            scheduler.shutdown()

    def getConnection(self, dbdialect, host, port, user, password, db):
        if "mysql" == dbdialect:
            return pymysql.connect(host=host, port=int(port), user=user, password=password, db=db,  charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    FaceDescriptorSchedule().schedule()
