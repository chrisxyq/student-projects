import os
import numpy as np
from math import radians, cos, sin, asin, sqrt,degrees,atan,acos

from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *



def get_spheretf(pt):
    """ 功能：直角坐标点(如：皮肤、肿瘤表面、肝脏表面、障碍物表面)→→→→→→→→→real球坐标点(θ∈[0, π]， φ∈[0,2π] )"""
    target=gl.get_value('targetpos')
    pt_SPH=[0,0,0]
    pt_SPH[0]=((pt[0]-target[0])**2+(pt[1]-target[1])**2+(pt[2]-target[2])**2)**0.5
    #对的，参照arccosx的图像，x在[-1,0]时，y属于[90,180]，x在[0,1]时，y属于[0,90]，这部分相当于确定了上部分/下部分
    pt_SPH[1] =degrees(acos((pt[2]-target[2])/pt_SPH[0]))
    if pt[0]-target[0]>0 and pt[1]-target[1]>0:
        pt_SPH[2] = degrees(atan((pt[1] - target[1]) / (pt[0] - target[0])))
    elif pt[0]-target[0]<0:# 第二/第三象限
        pt_SPH[2] = degrees(atan((pt[1] - target[1]) / (pt[0] - target[0])))+180
    elif pt[0]-target[0]>0 and pt[1]-target[1]<0:# 第四象限
        #0823bug:不一定满足这个条件导致角度大于360
        #print(pt[0]-target[0]>0 and pt[1]-target[1]<0)
        pt_SPH[2] = degrees(atan((pt[1] - target[1]) / (pt[0] - target[0]))) + 360
    if pt[0]-target[0]==0 and pt[1]-target[1]>0:
        pt_SPH[2] = 90
    if pt[0]-target[0]<0 and pt[1]-target[1]==0:
        pt_SPH[2] = 180
    if pt[0]-target[0]==0 and pt[1]-target[1]<0:
        pt_SPH[2] = 270
    return pt_SPH






















# def get_spheretf(pts):
#     """
#     工具1：
#     功能：直角坐标点(如：皮肤、肿瘤表面、肝脏表面、障碍物表面)→→→→→→→→→real球坐标点    
#     (θ∈[0, π]， φ∈[0,2π] )
#     """
#     targetpos=gl.get_value('targetpos')
#     pts=np.array(pts)
#     pts_sphere=np.zeros((pts.shape[0], 3))
#     for i in range(pts.shape[0]):
#         pts_sphere[i,0]=((pts[i, 0]-targetpos[0])**2+(pts[i, 1]-targetpos[1])**2+(pts[i, 2]-targetpos[2])**2)**0.5
#         #对的，参照arccosx的图像，x在[-1,0]时，y属于[90,180]，x在[0,1]时，y属于[0,90]，这部分相当于确定了上部分/下部分
#         pts_sphere[i, 1] =degrees(acos((pts[i, 2]-targetpos[2])/pts_sphere[i,0]))
#         if pts[i, 0]-targetpos[0]>=0 and pts[i, 1]-targetpos[1]>0:
#             pts_sphere[i, 2] = degrees(atan((pts[i, 1] - targetpos[1]) / (pts[i, 0] - targetpos[0])))
#         elif pts[i, 0]-targetpos[0]<0 :# 第二/第三象限
#             pts_sphere[i, 2] = degrees(atan((pts[i, 1] - targetpos[1]) / (pts[i, 0] - targetpos[0])))+180

#         elif pts[i, 0]-targetpos[0]>0 and pts[i, 1]-targetpos[1]<0:# 第四象限
#             #0823bug:不一定满足这个条件导致角度大于360
#             #print(pts[i, 0]-targetpos[0]>0 and pts[i, 1]-targetpos[1]<0)
#             pts_sphere[i, 2] = degrees(atan((pts[i, 1] - targetpos[1]) / (pts[i, 0] - targetpos[0]))) + 360
#         if pts[i,0]-targetpos[0]==0 and pts[i,1]-targetpos[1]>0:
#             pts_sphere[i, 2]= 90
#         if pts[i,0]-targetpos[0]<0 and pts[i,1]-targetpos[1]==0:
#             pts_sphere[i, 2] = 180
#         if pts[i,0]-targetpos[0]==0 and pts[i,1]-targetpos[1]<0:
#             pts_sphere[i, 2] = 270
#     # print(pts_sphere)
#     return pts_sphere
#     # return np.array([ele for ele in pts_sphere if ele[2]!=0])



































def get_Cartesian(Cartesian_dir,angle_dir):
    """工具2：
    功能：二维不可行角度点→→→→→→→→→targetpos为球心的球面上的直角坐标点(乘以针长然后加上靶点坐标)
    输入参数：输出直角坐标点的路径、读取的待转化二维不可行角度点路径

    注意不是get_spheretf的逆过程"""
    targetpos=gl.set_value('targetpos')
    angle_list = np.loadtxt(angle_dir)
    angle_list = angle_list[:,[0,1]]
    Spherical=np.column_stack((np.ones(len(angle_list)) * ndlength, angle_list))
    Cartesian=np.ones( Spherical.shape )
    for i in range(len(angle_list)):
        Cartesian[i][0] = ndlength * sin(radians(Spherical[i][1]))\
                          *cos(radians(Spherical[i][2]))+targetpos[0]
        Cartesian[i][1] = ndlength * sin(radians(Spherical[i][1]))\
                          *sin(radians(Spherical[i][2]))+targetpos[1]
        Cartesian[i][2] = ndlength * cos(radians(Spherical[i][1]))+targetpos[2]
    #np.savetxt(Cartesian_dir, Cartesian, fmt='%.02f')
    return Cartesian

