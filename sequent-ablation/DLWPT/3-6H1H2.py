from vtkplotter import *
import numpy as np
import os
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')

from setpara import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\preprocess')
from get_targetstxt import *
from math import radians, cos, sin, asin, sqrt,degrees,atan,acos
colordict= {'artery': (165,42,42,1), 'bone': (189,183,107,1), 'gallbladder': (255,182,193,1),
'liver': (255,160,122,0.3),  'livertumor': (105,105,105,0.8),  'livertumor1': (105,105,105,0.8),
  'livertumor2': (105,105,105,0.8),'portalvein': (32,178,170,1), 'skin': (255,255,255,0.3), 
  'venoussystem':(32,178,170,1)}
obname='gallbladder'
head=r'E:\thesis_task\3Dircadb_download\3Dircadb1.9\MESHES_VTK'
a=load(os.path.join(otxt_hardpath,'H1','H1_skin.txt'), c=color_dic[1], alpha=1)
b=load(os.path.join(otxt_hardpath,'H2','H2_skin.txt'), c=color_dic[2], alpha=1)
c=load(os.path.join(head,'livertumor.vtk'), c=(105,105,105), alpha=0.3)
d=load(os.path.join(deephead, 'MASKS_BMZB', obname,obname + "BMZB.txt"), c=(255,182,193), alpha=1)

e=load(os.path.join(otxt_hardpath,'H3',obname +'active.txt'), c=(0,0,225), alpha=1)
get_targetstxt()
targetpos=gl.get_value('targetpos')[0:3]
f=Point(targetpos, r=13, c='black')
# show(a,b,c,d,e,f,bg='black')
show(a,b,c,d,e,f)