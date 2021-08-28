from vtkplotter import *
import numpy as np
import os
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')

from setpara import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\preprocess')
from get_targetstxt import *
from math import radians, cos, sin, asin, sqrt,degrees,atan,acos
colordict= {'artery': (165,42,42), 'bone': (189,183,107), 'gallbladder': (255,182,193),
'liver': (255,160,122),  'livertumor': (105,105,105),  'livertumor1': (105,105,105),
  'livertumor2': (105,105,105),'portalvein': (32,178,170), 'skin': (255,255,255), 
  'venoussystem':(32,178,170)}
obname='portalvein'
head=r'E:\thesis_task\3Dircadb_download\3Dircadb1.9\MESHES_VTK'
# def add_vtk():
	
showlist=[]
def add_skin():
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H5','H5_back_skin.txt'))
	a=Points(helper,c=(255,99,71),r=6, alpha=1)
	pt1=helper[-15]
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H6','H6_back_skin.txt'))
	pt2=helper[-1450]
	b=Points(helper,c=(0,255,255),r=6, alpha=1)
	showlist.append(a)
	showlist.append(b)
	return pt1,pt2


def add_line():

	d=load(os.path.join(head,'skin.vtk'), c=(255,255,255), alpha=0.3)
	e=load(os.path.join(head,'livertumor.vtk'), c=(105,105,105), alpha=0.4)
	f=load(os.path.join(head,'liver.vtk'), c=(	200,160,122), alpha=0.8)
	showlist.append(d)
	showlist.append(e)
	showlist.append(f)


	pt1,pt2=add_skin()

	get_targetstxt()
	targetpos=gl.get_value('targetpos')[0:3]
	g=Point(targetpos, r=15, c='red')
	showlist.append(g)


	pt1=[pt1[0]+(pt1[0]-targetpos[0])*1,pt1[1]+(pt1[1]-targetpos[1])*1,pt1[2]+(pt1[2]-targetpos[2])*1]
	h = Line(targetpos,pt1, c='black',lw=4)
	pts = f.intersectWithLine(targetpos,pt1)
	i = Points(pts, r=15, c='r')
	showlist.append(h)
	showlist.append(i)

	pt2=[pt2[0]+(pt2[0]-targetpos[0])*2.3,pt2[1]+(pt2[1]-targetpos[1])*2.3,pt2[2]+(pt2[2]-targetpos[2])*2.3]
	h2 = Line(targetpos,pt2, c='black',lw=4)
	pts2 = f.intersectWithLine(targetpos,pt2)
	i2 = Points(pts2, r=15, c='r')
	showlist.append(h2)
	showlist.append(i2)
	show(showlist)
# showlist.append(i)
# pts = e.intersectWithLine(newtar,pt1)
# j = Points(pts, r=13, c='r')
# showlist.append(j)
add_line()

# print(showlist)


# helper=np.loadtxt(os.path.join(otxt_hardpath,'H5','H5_liver.txt'))

# # pt1=[3.928711473941805110e+01, 1.842129157781601805e+02, 5.200000000000000000e+01]
# pt1=[pt1[0]+(pt1[0]-targetpos[0])*2.3,pt1[1]+(pt1[1]-targetpos[1])*2.3,pt1[2]+(pt1[2]-targetpos[2])*2.3]
# # pt2=[1.702441638708115477e+02, 7.508204150199894400e+01, 6.400000000000000000e+01]
# # pt2=[pt2[0]+(pt2[0]-targetpos[0])*0.3,pt2[1]+(pt2[1]-targetpos[1])*0.3,pt2[2]+(pt2[2]-targetpos[2])*0.3]
# # newtar=[targetpos[0]-(pt1[0]-targetpos[0])*0.8,targetpos[1]-(pt1[1]-targetpos[1])*0.8,targetpos[2]-(pt1[2]-targetpos[2])*0.8]
# h = Line(targetpos,pt1, c='black',lw=4)
# # showlist.append(g)
# # h = Line(targetpos,pt2, c='r',lw=4)
# # showlist.append(h)

# pts = f.intersectWithLine(targetpos,pt1)
# print(pts )
# i = Points(pts, r=15, c='r')
# show(a,b,e,d,f,g,h,i)
# # show(showlist,bg='black')
