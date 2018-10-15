#!/usr/bin/python
# -*- coding: UTF-8 -*-
import dlib
import cv2
import os
import logging as logger

current_path = os.path.abspath("..") # 获取当前路径
# 模型路径
predictor_path = current_path + os.sep + "collect" + os.sep + "model" + os.sep + "shape_predictor_68_face_landmarks.dat"
face_rec_model_path = current_path + os.sep + "collect" + os.sep + "model" + os.sep + "dlib_face_recognition_resnet_model_v1.dat"
# 读入模型
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

class Collect:
    def __init__(self):
        pass

    def collect(self, img):
        # opencv 读取图片，并显示
       # img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        # opencv的bgr格式图片转换成rgb格式
        b, g, r = cv2.split(img)
        img2 = cv2.merge([r, g, b])
        dets = detector(img, 1)  # 人脸标定
        logger.warning("Number of faces detected: {}".format(len(dets)))
        for index, face in enumerate(dets):
            logger.info('face {}; left {}; top {}; right {}; bottom {}'.format(index, face.left(), face.top(), face.right(),
                                                                               face.bottom()))
            shape = shape_predictor(img2, face)  # 提取68个特征点
            # for i, pt in enumerate(shape.parts()):
            #     # print('Part {}: {}'.format(i, pt))
            #     pt_pos = (pt.x, pt.y)
            #     cv2.circle(img, pt_pos, 2, (255, 0, 0), 1)
            #     # print(type(pt))
            # # print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))
            # cv2.namedWindow(img_path + str(index), cv2.WINDOW_AUTOSIZE)
            # cv2.imshow(img_path + str(index), img)

            face_descriptor = face_rec_model.compute_face_descriptor(img2, shape)  # 计算人脸的128维的向量
            return face_descriptor

