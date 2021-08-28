from vtkplotter import *
from sys import path
from PIL import Image, ImageDraw
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
showlist=[]

# filePath= os.path.join(deephead, 'MESHES_VTK')
# k=5/4
# rlist=[30,35,30,30,30,30,30,30,30]
# ratelist=[0.05,0,0,0,0,0,0,0,0]

# def add_basic():
# 	eles=os.listdir(filePath)
# 	for ele in eles:
		
# 		c=vtk_dic[ele][0:3]
# 		alpha=vtk_dic[ele][-1]
# 		a=load(os.path.join(filePath, ele), c=c, alpha=alpha)
# 		if ele=='livertumor1.vtk':
# 			print(a)
# 		showlist.append(a)

# def add_vtk():
# 	adder=load(r'E:/livertumor1.vtk', c=(50,50,50), alpha=0.8).scale(0.9)
# 	adder.pos(10,14,16)
# 	showlist.append(adder)


# def add_ndl():
# 	ndlpts=[]
	

# 	ndlpts=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_'+str(order),'line.txt'))
# 	# a = Line([95.8,148.6,160],[-99.4,104.2-20,160], c='black',lw=5)
# 	a = Line([95.8+(95.8+99.4)*0.01,148.6+(148.6-104.2)*0.01,160],[-99.4,104.2-60,160], c='black',lw=5)
# 	b=Points([[95.8+(95.8+99.4)*0.01,148.6+(148.6-104.2)*0.01,160]],r=25,c='black')
# 	c=show_elli([-99.4,104.2-60,160],[95.8+(95.8+99.4)*0.01,148.6+(148.6-104.2)*0.01,160],36,0)
# 	showlist.append(a)
# 	showlist.append(b)
# 	showlist.append(c)


# def add_pre_ndl():
# 	if order>1:

# 		a = Line([108.4,127.0,160],[-60.4,10.8+10,160], c='r',lw=5)
# 		b=Points([[108.4,127.0,160]],r=25,c='r')
# 		c=show_elli([-60.4,10.8+10,160],[108.4,127.0,160],36,0)
# 		showlist.append(a)
# 		showlist.append(b)
# 		showlist.append(c)

# def show_res():
# 	add_basic()
# 	add_ndl()
# 	add_pre_ndl()
# 	add_vtk()
# 	show(showlist)

# #================helper====================

# def show_elli(inpt,tar,r,rate):
#     #苍白绿
#     R=get_elliaxis(inpt,tar)
#     #每一个axis指的是直径，因此r要乘以2
#     helper=[tar[0]+(inpt[0]-tar[0])*rate,tar[1]+(inpt[1]-tar[1])*rate,tar[2]+(inpt[2]-tar[2])*rate]


#     elli_actor=Ellipsoid(pos=helper, axis1=[R[0][0]*2*r/k, R[1][0]*2*r/k, R[2][0]*2*r/k], 
#         axis2=[R[0][1]*2*r, R[1][1]*2*r, R[2][1]*2*r], axis3=[R[0][2]*2*r/k, R[1][2]*2*r/k, R[2][2]*2*r/k], c=(152,251,152), alpha=0.8)
#     return elli_actor


# def get_elliaxis(inpt,tar):
#     #输入进针单位向量，输出的单位矩阵每一列分别为椭球坐标系的xyz轴
#     lenth=((tar[0]-inpt[0])**2+(tar[1]-inpt[1])**2+(tar[2]-inpt[2])**2)**0.5
#     alpha=(tar[0]-inpt[0])/lenth
#     beta=(tar[1]-inpt[1])/lenth
#     gama=(tar[2]-inpt[2])/lenth

#     init=[0,(1-alpha**2)**0.5,gama/((1-alpha**2)**0.5),
#     -alpha*beta/((1-alpha**2)**0.5),-beta/((1-alpha**2)**0.5),-alpha*gama/(1-alpha**2)**0.5]
#     sol_fsolve =init
#     R=[[sol_fsolve[0], alpha, sol_fsolve[1]], [sol_fsolve[2],beta,sol_fsolve[3]], [sol_fsolve[4], gama,sol_fsolve[5]]]
#     return R

# show_res()
# A=load(r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\MASKS_PNGPTS\MESHES_VTK/livertumor2.vtk', c=(50,50,50), alpha=0.8)
# print(A)
# show(A)
import numpy as np
import vtkplotter
a=np.loadtxt(r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\MASKS_PNGPTS\MASKS_BMZB\livertumor1/livertumor1BMZB.txt')
print(max(a[:,0])-min(a[:,0]),max(a[:,1])-min(a[:,1]),max(a[:,2])-min(a[:,2]))
a=load(r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.15\MASKS_PNGPTS\MASKS_BMZB\livertumor1/livertumor1BMZB.txt')
show(a)
print(a)