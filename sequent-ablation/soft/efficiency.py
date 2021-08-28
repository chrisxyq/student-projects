import cv2
import os
# from numpy import *
import numpy as np
import time
from sklearn.neighbors import KDTree
from math import radians, cos, sin, asin, sqrt
from PIL import Image, ImageDraw
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\preprocess')
from get_targetstxt import *
from scipy.optimize import root,fsolve
from vtkplotter import *

def get():
    res=[]
    a=Image.open(os.path.join(opic_ndlpath, 'helper.png')) 
    for x in range(181):
        for y in range(360):
            #if a.getpixel((x,y))==255:
            if a.getpixel((x,y))==(255,255,255):
                res.append([x,y])
    return res

def purefull():
	opic_ndlpath=r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_png\ndl_2'
	otxt_violentpath=r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_txt\ndl_2\violent'
	a=Image.open(os.path.join(opic_ndlpath, 'helper.png'))
	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+'2'+'violent_fullresult.txt'))
	res=[]
	for ele in full:
		if a.getpixel((int(ele[0]),int(ele[1])))==(255,255,255):
			res.append(ele)
	return np.array(res)

def efficiency():
	#根据iterangle对肿瘤作坐标变换
    pi=3.1415926
    feasible=purefull()[:,[0,1]]
    #pts=np.loadtxt(r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\MASKS_PNGPTS\MASKS_BMZB\livertumor2/livertumor2BMZB.txt')
    pts=np.loadtxt(r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\MASKS_PNGPTS\MASKS_BMZB\livertumor2/helper.txt')
    pts=pts.T
    T_box = np.mat(np.zeros((3, pts.shape[1])))
    get_targetstxt()
    tar=gl.get_value('targetpos')
    T_box[0, :], T_box[1, :], T_box[2, :] = tar[0],tar[1],tar[2] 
    helper=np.array([[0]*pts.shape[1]]*3,dtype=np.float)
    res=[]
    for ele in feasible: #遍历可行域每个点
        #根据球面角度求解变换矩阵
        print(ele)
        alpha=sin(ele[0]*pi/180)*cos(ele[1]*pi/180)
        beta=sin(ele[0]*pi/180)*sin(ele[1]*pi/180)
        gama=cos(ele[0]*pi/180)
        dwxl=[alpha,beta,gama]
        def f(x,args=dwxl):              
            return np.array([x[0]**2+x[1]**2+alpha**2-1,
                    x[0]*x[2]+alpha*beta+x[1]*x[3],
                    x[0]*x[4]+alpha*gama+x[1]*x[5],
                    x[2]**2+x[3]**2+beta**2-1,    
                    x[4]**2+x[5]**2+gama**2-1,
                    x[2]*x[4]+gama*beta+x[3]*x[5]])
        if abs(alpha)-1<0.05:
            init=[0,0,0,1,1,0]      
        else:
            init=[0,(1-alpha**2)**0.5,gama/((1-alpha**2)**0.5),-alpha*beta/((1-alpha**2)**0.5),beta/((1-alpha**2)**0.5),-alpha*gama/(1-alpha**2)**0.5]
        sol_fsolve = fsolve(f,init,args=dwxl,xtol=1.49012e-03, maxfev=10000)


        R=np.matrix([[sol_fsolve[0], alpha, sol_fsolve[1]], [sol_fsolve[2],beta,sol_fsolve[3]], [sol_fsolve[4], gama,sol_fsolve[5]]])                      
        helper = R.I * (pts - T_box) #给i个3行n列的pts_newtf赋值
        cnt=0
        
        helper = np.array(helper.T)
        # print(helper)
        # a=Points(helper)
        # show(a)
        for sb in helper:
            if judge(sb)==1:
                cnt+=1
        print(cnt)
        res.append([ele[0],ele[1],cnt])
    np.savetxt(os.path.join(otxt_hardpath,'efficiency.txt'),res)
    return res



def judge(pt):
	R=35
	k=0.8
	r=R/k
	#print(pt[0])
	res=pt[0]**2/(r**2)+pt[1]**2/(R**2)+pt[2]**2/(r**2)
	#print(res)

	# res=pt[0]**2/((0.5*R)**2)+pt[1]**2/((0.5*R)**2)+pt[2]**2/((0.5*R)**2)
	if res<1:
		#print(pt,R,res)
		return 1
	else:
		#print(res)
		return 0

efficiency()