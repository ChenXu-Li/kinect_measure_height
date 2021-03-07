# -*- coding：utf-8 -*-
"""
time:2021/2/24
author:李辰旭
organization: BIT
contact: QQ:316469360
——————————————————————————————
description：
$ 处理二值合成轨迹图的一些函数。
主要包括：
滤波降噪
提取轮廓质心
拟合二次曲线
计算像素高度
——————————————————————————————
note:
python3.7以上版本才可运行
"""
import numpy as np
import cv2 as cv
from scipy.optimize import leastsq
def apply(img_BW,k):
    '''输入二值单通道图像
    返回特定区域被涂黑(k=0)或涂白(k=1)的图像'''
    a=img_BW.copy()
    left=400
    right=1920-left
    mid_left=650
    mid_right=1920-mid_left
    mid_high=500
    a[:,:left]=255*k
    a[:,right:]=255*k
    a[mid_high:,mid_left:mid_right]=255*k
    return a
def find_centroid(img_BW):
    '''输入：二值图像
    返回：质心xy列表'''
    cnts,_ = cv.findContours(img_BW, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    X_Y=[]
    # 遍历轮廓集
    for c in cnts:
        # 计算轮廓区域的图像矩。 在计算机视觉和图像处理中，图像矩通常用于表征图像中对象的形状。这些力矩捕获了形状的基本统计特性，包括对象的面积，质心（即，对象的中心（x，y）坐标），方向以及其他所需的特性。
        M = cv.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        X_Y.append((cX,cY))
    return X_Y

def func(params, x):
    a, b, c = params
    return a * x * x + b * x + c
# 误差函数，即拟合曲线所求的值与实际值的差
def error(params, x, y):
    return func(params, x) - y
# 对参数求解
def slovePara(X,Y):
    '''输入：两个列表
       返回：二次函数的三个参数abc
    '''
    p0 = [10, 10, 10]#abc的初值，还要迭代呢
    X=np.array(X)
    Y=np.array(Y)
    Para = leastsq(error, p0, args=(X, Y))
    a, b, c = Para[0]
    return a,b,c

def track_progress(img_BW,img,grand=950,startline=1250):
    '''输入合成的轨迹图（二值化的单通道图及二值化的三通道图）
       返回发球点的像素高度,返回处理过的图片'''
    #涂抹噪声
    applied=apply(img_BW,0)
    #滤波降噪
    #中值滤波
    mid_filer=cv.medianBlur(applied,3)
    #膨胀
    kernel = np.ones((5, 5), np.uint8)
    frame = cv.dilate(mid_filer, kernel, iterations=2)
    #找质心
    X_Y = find_centroid(frame)
    X=[]
    Y=[]
    for i in X_Y:
        X.append(i[0])
        Y.append(i[1])
        cv.circle(img, (i[0], i[1]), 10, (0, 0, 255), -1)
    #拟合抛物线
    try:
        a,b,c=slovePara(X,Y)
        print('抛物线参数：a=',a,'b=',b,'c=',c)
        #画抛物线
        for w in range(1920):
            h=int(a*(w*w)+b*w+c)
            if h>0&h<1080:
                cv.circle(img, (w, h), 3, (0, 255, 0), -1)
    except:
        print('拟合抛物线时出现错误，好像是因为拟合点少于三个')
    #画地面和起始线
    cv.line(img,(0,grand), (1919,grand), (255,0,0),3)
    cv.line(img,(startline,0), (startline,1079), (255,0,0),3)
    #找发球点，求高度
    try:
        height=a*(startline*startline)+b*startline+c - grand
        if height < 0:
            height*=-1
        print('像素高度=',height)
        return height,frame
    except:
        print('拟合抛物线时出现错误，abc没值')
        return -1,frame
    

if __name__ == '__main__':
    import os
    cv.namedWindow("obj", cv.WINDOW_NORMAL)
    cv.resizeWindow("obj", int(1920/3), int(1080/3))
    cv.moveWindow("obj", 0, 0)
    cv.namedWindow("applied", cv.WINDOW_NORMAL)
    cv.resizeWindow("applied", int(1920/3), int(1080/3))
    cv.moveWindow("applied", int(1920/3), 0)
    img = cv.imread("D:\\lalala.png")
    img_BW = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    track_progress(img_BW,img)
    cv.imshow("obj",img)
    cv.imshow("applied",img_BW)
    cv.waitKey(0)
    
    

