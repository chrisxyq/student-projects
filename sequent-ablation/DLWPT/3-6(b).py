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
# oblist=['bone','gallbladder','portalvein']
oblist=['gallbladder']
showlist=[]
for ele in oblist:
	a=load(os.path.join(otxt_hardpath,'H3',ele+'active.txt'), c=(0,0,225), alpha=1)
	showlist.append(a)
for ele in oblist:
	d=load(os.path.join(otxt_hardpath,'H3',ele+'_exclude_skin.txt'), c=(240,230,140), alpha=0.5)
	showlist.append(d)

b=load(os.path.join(head,'skin.vtk'), c=(255,255,255), alpha=0.3)
showlist.append(b)
c=load(os.path.join(head,'livertumor.vtk'), c=(105,105,105), alpha=0.4)
showlist.append(c)
e=load(os.path.join(head,'gallbladder.vtk'), c=(255,182,193), alpha=0.3)
showlist.append(e)

get_targetstxt()
targetpos=gl.get_value('targetpos')[0:3]
f=Point(targetpos, r=13, c='black')
showlist.append(f)

pt1=[3.230273878574372759e+01, 2.060390906333924477e+02, 5.200000000000000000e+01]
pt1=[pt1[0]+(pt1[0]-targetpos[0])*0.3,pt1[1]+(pt1[1]-targetpos[1])*0.3,pt1[2]+(pt1[2]-targetpos[2])*0.3]
pt2=[1.475449420213700193e+02 ,8.643165242671970816e+01, 1.080000000000000000e+02]
pt2=[pt2[0]+(pt2[0]-targetpos[0])*0.3,pt2[1]+(pt2[1]-targetpos[1])*0.3,pt2[2]+(pt2[2]-targetpos[2])*0.3]
newtar=[targetpos[0]-(pt1[0]-targetpos[0])*0.8,targetpos[1]-(pt1[1]-targetpos[1])*0.8,targetpos[2]-(pt1[2]-targetpos[2])*0.8]
g = Line(newtar,pt1, c='r',lw=4)
showlist.append(g)
h = Line(targetpos,pt2, c='r',lw=4)
showlist.append(h)

pts = e.intersectWithLine(targetpos,pt2)
i = Points(pts, r=13, c='r')
showlist.append(i)
pts = e.intersectWithLine(newtar,pt1)
j = Points(pts, r=13, c='r')
showlist.append(j)

k=load(os.path.join(otxt_hardpath,'H1','H1_skin.txt'), c=color_dic[1], alpha=1)
l=load(os.path.join(otxt_hardpath,'H2','H2_skin.txt'), c=color_dic[2], alpha=1)
showlist.append(k)
showlist.append(l)

# print(showlist)
show(showlist)
# show(showlist,bg='black')

