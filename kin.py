# -*- coding：utf-8 -*-
"""
time:2021/2/24
author:李辰旭
organization: BIT
contact: QQ:316469360
——————————————————————————————
description：
$ 基于Pykinect2写的一个Kinect的类。
主要包括：
彩色图像、深度图像的获取
求彩色像素点的深度值
——————————————————————————————
note:
python3.7以上版本才可运行
"""
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import ctypes
# import math
import cv2 as cv


class Kinect(object):
    def __init__(self):
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
        self.depth_ori = None
        self.color_frame = None
        self.w_color = 1920
        self.h_color = 1080
        self.w_depth = 512
        self.h_depth = 424
    """获取最新的图像数据"""
    def get_the_last_color(self):
        """
        Time :2019/5/1
        FunC:获取最新的图像数据
        Input:无
        Return:无
        """
        # 获得的图像数据是二维的，需要转换为需要的格式
        frame = self._kinect.get_last_color_frame()
        # 返回的是4通道，还有一通道是没有注册的
        gbra = frame.reshape([self._kinect.color_frame_desc.Height, self._kinect.color_frame_desc.Width, 4])
        # 取出彩色图像数据#是镜像,::-1用来反转左右
        self.color_frame = gbra[:, ::-1, 0:3]
        return self.color_frame
    """————————————————(2019/5/1)——————————————————"""
    """获取最新的深度数据"""
    def get_the_last_depth(self):
        """
        Time :2019/5/1
        FunC:获取最新的图像数据
        Input:无
        Return:无
        """
    
        # 获得深度图数据
        frame = self._kinect.get_last_depth_frame()
        image_depth_all = frame.reshape([self._kinect.depth_frame_desc.Height,
                                            self._kinect.depth_frame_desc.Width])
        #深度图反转左右
        self.depth_ori = image_depth_all[:,::-1]

        return self.depth_ori

def get_depth_value(dep,h,w):
    return dep[(h*424)//1080,(w*512)//1920]

def draw_points_value(frame,dep):
    #h从上至下0-1080  #w从左到右0-1920
    #!!!!frame被改变了
    for i in range(6):
        for j in range(6):
            w=200*i+50
            h=160*j
            cv.circle(frame,(h,w),5,(20,255,255),-1)
            cv.putText(frame, "[{},{}]".format(h,w), (w, h), cv. FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 1)
            cv.putText(frame, "{}".format(frame[h][w]), (w, h+25), cv. FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 1)
            cv.putText(frame, "depth[{}]".format(get_depth_value(dep,h,w)), 
                           (w, h+50), cv. FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)


if __name__ == '__main__':
    a = Kinect()
    while 1:
        a.get_the_last_color()
        a.get_the_last_depth()
        img=a.color_frame.copy()
        draw_points_value(img,a.depth_ori)
        cv.imshow('color', img)
        depth_img=a.depth_ori.astype(np.uint8)
        cv.imshow('depth', depth_img)
        #print(a.get_depth_value(500,500))
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
   