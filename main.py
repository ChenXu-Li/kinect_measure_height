# -*- coding：utf-8 -*-
"""
time:2021/2/24
author:李辰旭
organization: BIT
contact: QQ:316469360
——————————————————————————————
description：
$ 求取发球高度的主函数
主要包括：
控制台界面
绘制函数
求取给定范围内的深度
将像素高度转换为实际高度
——————————————————————————————
note:
python3.7以上版本才可运行
"""
from kin import*
from process import*
import numpy as np
import ctypes
import math
import cv2 as cv
import time
import copy
#x从上至下0-1080  #y从左到右0-1920
def colorframe_to_frame(img):
    '''帧差法求运动的像素
    输入：三通道图片
    输出：单通道灰度图片'''
    global gray0
    #前后帧灰度化，求差
    gray1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    foreground = cv.absdiff(gray0,gray1)
    gray0=gray1.copy()
    #对差进行二值化
    ret,thresh_foreground = cv.threshold(foreground, 50, 255, cv.THRESH_BINARY)
    return thresh_foreground
def is_valid_depth_value(d):
    '''判断是否是有效深度值'''
    #0.5m到6m之间有效
    if d>500&d<6000:
        return True
    else:
        return False
def averge_depth(dep,x0,y0,x1,y1):
    n=1
    sum_depth=0
    for h in range(x0,x1):
        for w in range(y0,y1):
            dep_value = get_depth_value(dep,h,w)
            if(is_valid_depth_value(dep_value)):
                sum_depth+=dep_value
                n+=1
    
    cv.putText(img, "[{}]".format(int(sum_depth/n)), (y1, x1), cv.FONT_HERSHEY_SIMPLEX,2, (0, 0, 255), 5)
 
    return int(sum_depth/n)
def draw_depth_caculate_area(img,x0,y0,x1,y1):
    cv.line(img,(y0,x0), (y1,x0), (255,0,0),3)
    cv.line(img,(y1,x0), (y1,x1), (255,0,0),3)
    cv.line(img,(y1,x1), (y0,x1), (255,0,0),3)
    cv.line(img,(y0,x1), (y0,x0), (255,0,0),3)

def draw_grand_and_start_lines(img,grand,startline):
    cv.line(img,(0,grand), (1919,grand), (255,0,0),3)
    cv.line(img,(startline,0), (startline,1079), (255,0,0),3)
def draw_points_depth_value(img,dep):
    for w in range(10,1920,200):
        for h in range(10,1080,200):
            cv.circle(img,(w,h),5,(20,255,255),-1)
            cv.putText(img, "[{}]".format(get_depth_value(dep,h,w)), 
                           (w, h), cv. FONT_HERSHEY_SIMPLEX,2, (0, 0, 255), 3)
def get_real_hight(height,depth):
    '''像素高度转化为实际高度
        垂直视角43.5°
        cos21.75=0.92881
    '''
    return int((height/1080)*depth*0.92881*2)
  
grand=950
startline=1250   
x0=200
x1=800
y0=1300
y1=1600

a = Kinect()
cv.namedWindow("color_now", cv.WINDOW_NORMAL)
cv.resizeWindow("color_now", int(a.w_color/3), int(a.h_color/3))
cv.moveWindow("color_now", 0, 0)   
cv.namedWindow("frame", cv.WINDOW_NORMAL)
cv.resizeWindow("frame", int(a.w_color/3), int(a.h_color/3))
cv.moveWindow("frame", int(a.w_color/3), 0)                                               
cv.namedWindow("track", cv.WINDOW_NORMAL)
cv.resizeWindow("track", int(a.w_color/3), int(a.h_color/3))
cv.moveWindow("track", int(a.w_color/3), int(a.h_color/3))
cv.namedWindow("obj", cv.WINDOW_NORMAL)
cv.resizeWindow("obj", int(a.w_color/3), int(a.h_color/3))
cv.moveWindow("obj", int(a.w_color/3), int(a.h_color/3)+300)
cv.namedWindow("console", cv.WINDOW_NORMAL)
cv.resizeWindow("console", 400, 400)
cv.moveWindow("console", 400, 400)
def move_grand(x):
    global grand
    grand=x 
cv.createTrackbar('grand','console',950,1079,move_grand)
def move_startline(x):
    global startline
    startline=x 
cv.createTrackbar('startline','console',1250,1919,move_startline)
def move_x0(x):
    global x0
    x0=x 
cv.createTrackbar('x0','console',200,1079,move_x0)
def move_x1(x):
    global x1
    x1=x 
cv.createTrackbar('x1','console',800,1079,move_x1)
def move_y0(x):
    global y0
    y0=x 
cv.createTrackbar('y0','console',1300,1919,move_y0)
def move_y1(x):
    global y1
    y1=x 
cv.createTrackbar('y1','console',1600,1919,move_y1)
while 1:
    flag = 1
    track = np.zeros((1080, 1920), np.uint8)
    while 1:
        a.get_the_last_color()
        a.get_the_last_depth()
        if flag:
            print("按下b键开始处理视频流")
            img=a.color_frame.copy()
            gray0 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            #实时彩色视频流
            draw_grand_and_start_lines(img,grand,startline)
            draw_depth_caculate_area(img,x0,y0,x1,y1)
            draw_points_depth_value(img,a.depth_ori)
            cv.imshow('color_now', img)
            #按b开始处理视频流
            if cv.waitKey(1) & 0xFF == ord('b'):
                depth0 = a.depth_ori
                flag = 0
        else:
            print("帧间差分中，按n结束帧间差分")
            img=a.color_frame.copy()
            #处理彩色帧,变成二值帧
            frame = colorframe_to_frame(img)
            cv.imshow('frame',frame)
            #叠加
            track = cv.bitwise_or(track,frame)
            cv.imshow('track',track)
            #实时彩色视频流
            draw_grand_and_start_lines(img,grand,startline)
            draw_depth_caculate_area(img,x0,y0,x1,y1)
            draw_points_depth_value(img,a.depth_ori)
            cv.imshow('color_now', img)
            #按n结束读入视频流，开始对track进行处理
            if cv.waitKey(1) & 0xFF == ord('n'):
                break
    track_3color=cv.cvtColor(track,cv.COLOR_GRAY2BGR)
    height,progressed_track= track_progress(track,track_3color,grand,startline)
    depth = averge_depth(depth0,x0,y0,x1,y1)
    print("height=",height,"depth=",depth)
    cv.imshow('track',progressed_track)
    cv.imshow('obj',track_3color)
    real_height=get_real_hight(height,depth)
    print("估计发球高度为{}mm".format(real_height))
    print("按C继续，按任意键退出")
    #按c进行下一轮判断，按其它键退出程序
    if cv.waitKey(0) & 0xFF == ord('c'):
        continue
    else:
        break
    
