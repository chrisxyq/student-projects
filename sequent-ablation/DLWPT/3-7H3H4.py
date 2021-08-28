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

# a=load(os.path.join(otxt_hardpath,'H4','H4_liver.txt'), c='r', alpha=0.5)
# b=load(os.path.join(otxt_hardpath,'H4','H4_skin.txt'), c='g', alpha=0.5)


o=load(os.path.join(otxt_hardpath,'H4','round1_skin.txt'), c=(255,165,0), alpha=0.5)

c=load(os.path.join(otxt_hardpath,'H4','SELECTED_liver.txt'), c='b', alpha=0.5)

d=load(os.path.join(head,'skin.vtk'), c=(255,255,255), alpha=0.3)

e=load(os.path.join(head,'livertumor.vtk'), c=(105,105,105), alpha=0.4)

f=load(os.path.join(head,'liver.vtk'), c=(255,160,122), alpha=0.4)


get_targetstxt()
targetpos=gl.get_value('targetpos')[0:3]
g=Point(targetpos, r=13, c='red')


# pt1=[3.928711473941805110e+01, 1.842129157781601805e+02, 5.200000000000000000e+01]
# pt1=[pt1[0]+(pt1[0]-targetpos[0])*0.3,pt1[1]+(pt1[1]-targetpos[1])*0.3,pt1[2]+(pt1[2]-targetpos[2])*0.3]
# pt2=[1.702441638708115477e+02, 7.508204150199894400e+01, 6.400000000000000000e+01]
# pt2=[pt2[0]+(pt2[0]-targetpos[0])*0.3,pt2[1]+(pt2[1]-targetpos[1])*0.3,pt2[2]+(pt2[2]-targetpos[2])*0.3]
# newtar=[targetpos[0]-(pt1[0]-targetpos[0])*0.8,targetpos[1]-(pt1[1]-targetpos[1])*0.8,targetpos[2]-(pt1[2]-targetpos[2])*0.8]
# g = Line(newtar,pt1, c='r',lw=4)
# showlist.append(g)
# h = Line(targetpos,pt2, c='r',lw=4)
# showlist.append(h)

# pts = e.intersectWithLine(targetpos,pt2)
# i = Points(pts, r=13, c='r')
# showlist.append(i)
# pts = e.intersectWithLine(newtar,pt1)
# j = Points(pts, r=13, c='r')
# showlist.append(j)

# print(showlist)
show(o,c,d,e,f,g)
# show(showlist,bg='black')

