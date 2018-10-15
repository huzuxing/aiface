#!/usr/bin/python
# -*- coding: UTF-8 -*-
from face_collect import Collect
from compare import Compare
import time
import numpy as np
import logger
import cv2
import cache
from schedule import FaceDescriptorSchedule
from concurrent.futures import ThreadPoolExecutor

collect = Collect()
compare = Compare()
threadPool = ThreadPoolExecutor(5)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

'''
人脸特征比对，判断是否是同一个人
'''
def reg(faceImg):
    _128descriptor = collect.collect(faceImg)
    if _128descriptor is None:
        logger.info("no face to det")
        return
    allDescriptors = cache.getCacheList()
    if allDescriptors is None or len(allDescriptors) <= 0:
        time.sleep(0.5) # 若没有数据，则等0.5秒，系统加载数据
    if allDescriptors is None or len(allDescriptors) <= 0:
        logger.info("no cache descritors") #还没有数据，则返回
        return
    '''
    人脸比对，此处可以做一个优化：当比对成功后，缓存列表中删除这个数据，减少循环次数
    '''
    _128descriptor_nparray = np.array(_128descriptor)
    for desc in allDescriptors:
        result = compare.compare(_128descriptor_nparray, desc["face_descriptor"])
        # 根据比对结果，进行考勤处理
        if result < 0.6:
            print("考勤成功[员工编号：" + desc["employeeNo"] + "]")
            break

def getFace():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # 图像灰化，降低计算复杂度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测出人脸
        rect = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=9,
                                             minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(rect) > 0:
            for x, y, w, h in rect:
                detImg = frame[y:y + h, x:x + w]
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0), 3)
                # 开启一个线程去处理人脸数据
                threadPool.submit(reg, detImg)
        cv2.imshow("Esc exit", frame)
        key = cv2.waitKey(1)
        if key & 0xff == ord('q') or key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    fds = FaceDescriptorSchedule()
    fds.schedule(1) # 开启定时器
    getFace()