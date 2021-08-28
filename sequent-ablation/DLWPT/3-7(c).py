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

a=load(os.path.join(otxt_hardpath,'H5','H5_liver.txt'), c=(0,255,255), alpha=1)
b=load(os.path.join(otxt_hardpath,'H5','selected_tmr.txt'), c='b', alpha=1)
c=load(os.path.join(otxt_hardpath,'H5','H5_back_skin.txt'), c=(0,255,255), alpha=1)

# o=load(os.path.join(otxt_hardpath,'H4','round1_skin.txt'), c=(255,165,0), alpha=0.5)
# c=load(os.path.join(otxt_hardpath,'H4','SELECTED_liver.txt'), c='b', alpha=0.5)

d=load(os.path.join(head,'skin.vtk'), c=(255,255,255), alpha=0.3)

e=load(os.path.join(head,'livertumor.vtk'), c=(105,105,105), alpha=0.4)

f=load(os.path.join(head,'liver.vtk'), c=(255,160,122), alpha=0.4)


get_targetstxt()
targetpos=gl.get_value('targetpos')[0:3]
g=Point(targetpos, r=13, c='red')

show(a,c,d,e,d,f,g)
# show(b,d,e,d,f,g)
# show(showlist,bg='black')
