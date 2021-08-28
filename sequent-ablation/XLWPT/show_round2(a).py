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
oblist=['bone','gallbladder','portalvein','venoussystem']
# oblist=['gallbladder']
showlist=[]
def add_skin():
	alpha=1
	r=10
	# helper= np.loadtxt(os.path.join(otxt_hardpath,'H1','H1_skin.txt'))
	# a=Points(helper,c=color_dic[1],r=r, alpha=alpha)
	# showlist.append(a)
	# helper= np.loadtxt(os.path.join(otxt_hardpath,'H2','H2_skin.txt'))
	# a=Points(helper,c=color_dic[2],r=r, alpha=alpha)
	# showlist.append(a)
	# helper= np.loadtxt(os.path.join(otxt_hardpath,'H3','H3_skin.txt'))
	# a=Points(helper,c=color_dic[3],r=r, alpha=0.6)
	# showlist.append(a)
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H4','H4_skin.txt'))
	a=Points(helper,c=color_dic[4],r=r, alpha=0.6)
	showlist.append(a)

add_skin()	
def add_basic():
	filePath= os.path.join(deephead, 'MESHES_VTK')
	for ele in oblist:
		c=vtk_dic[ele+'.vtk'][0:3]
		alpha=vtk_dic[ele+'.vtk'][-1]
		a=load(os.path.join(filePath, ele+'.vtk'), c=c, alpha=alpha)
		showlist.append(a)
# for ele in oblist:

# 	a=load(os.path.join(deephead, 'MASKS_BMZB', ele, ele+"BMZB.txt"), c=(150,150,150), alpha=0.5)
# 	showlist.append(a)
add_basic()

for ele in oblist:
	a=load(os.path.join(otxt_hardpath,'H4',ele+'active.txt'), c=(0,0,225), alpha=1)
	showlist.append(a)
# for ele in oblist:
# 	d=load(os.path.join(otxt_hardpath,'H4',ele+'_exclude_skin.txt'), c=(240,230,140), alpha=0.6)
# 	showlist.append(d)

b=load(os.path.join(head,'skin.vtk'), c=(255,255,255), alpha=0.3)
showlist.append(b)
c=load(os.path.join(head,'livertumor.vtk'), c=(105,105,105), alpha=0.4)
showlist.append(c)
e=load(os.path.join(head,'gallbladder.vtk'), c=(255,182,193), alpha=0.3)
showlist.append(e)

get_targetstxt()
targetpos=gl.get_value('targetpos')[0:3]
f=Point(targetpos, r=15, c='white')
showlist.append(f)

pt1=[3.430273878574372759e+01, 2.060390906333924477e+02, 4.600000000000000000e+01]
pt1=[pt1[0]+(pt1[0]-targetpos[0])*0.3,pt1[1]+(pt1[1]-targetpos[1])*0.3,pt1[2]+(pt1[2]-targetpos[2])*0.3]
# pt2=[1.475449420213700193e+02 ,8.643165242671970816e+01, 1.080000000000000000e+02]
# pt2=[pt2[0]+(pt2[0]-targetpos[0])*0.3,pt2[1]+(pt2[1]-targetpos[1])*0.3,pt2[2]+(pt2[2]-targetpos[2])*0.3]
newtar=[targetpos[0]-(pt1[0]-targetpos[0])*0.8,targetpos[1]-(pt1[1]-targetpos[1])*0.8,targetpos[2]-(pt1[2]-targetpos[2])*0.8]
g = Line(newtar,pt1, c='black',lw=4)
showlist.append(g)
# h = Line(targetpos,pt2, c='r',lw=4)
# showlist.append(h)

# pts = e.intersectWithLine(targetpos,pt2)
# i = Points(pts, r=13, c='r')
# showlist.append(i)
pts = e.intersectWithLine(newtar,pt1)
j = Points(pts, r=15, c='r')
showlist.append(j)


# print(showlist)
show(showlist)
# show(showlist,bg='black')

