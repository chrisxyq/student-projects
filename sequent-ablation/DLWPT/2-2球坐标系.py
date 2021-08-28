from vtkplotter import *
import numpy as np
import os
from math import radians, cos, sin, asin, sqrt,degrees,atan,acos
colordict= {'artery': (165,42,42,1), 'bone': (189,183,107,1), 'gallbladder': (255,182,193,1),
'liver': (255,160,122,0.3),  'livertumor': (105,105,105,0.8),  'livertumor1': (105,105,105,0.8),
  'livertumor2': (105,105,105,0.8),'portalvein': (32,178,170,1), 'skin': (255,255,255,0.3), 
  'venoussystem':(32,178,170,1)}

head=r'E:\thesis_task\3Dircadb_download\3Dircadb1.9\MESHES_VTK'

a=load(os.path.join(head,'artery.vtk'), c=(165,42,42), alpha=0.2)
b=load(os.path.join(head,'bone.vtk'), c=(189,183,107), alpha=0.2)
c=load(os.path.join(head,'gallbladder.vtk'), c=(255,182,193), alpha=1)
h=load(os.path.join(head,'venoussystem.vtk'), c=(32,178,170), alpha=0.2)
f=load(os.path.join(head,'portalvein.vtk'), c=(32,178,170), alpha=0.2)

d=load(os.path.join(head,'liver.vtk'), c=(255,160,122), alpha=0.3)
e=load(os.path.join(head,'livertumor.vtk'), c=(105,105,105), alpha=0.8)
g=load(os.path.join(head,'skin.vtk'), c=(255,255,255), alpha=0.8)


i=Arrow((0,0, 0), (200, 0, 0),  c='r', alpha=1)
j=Arrow((0,0, 0), (0, 200, 0),  c='g', alpha=1)
k=Arrow((0,0, 0), (0, 0, 200),  c='b', alpha=1)


l=Arrow((80,190, 55), (280, 190, 55), c='r', alpha=1)
m=Arrow((80,190, 55), (80,390, 55),  c='g', alpha=1)
n=Arrow((80,190, 55), (80,190, 255),  c='b', alpha=1)

o=load(r'E:\thesis_task\3Dircadb_download\3Dircadb1.9\PATIENT_PNG\image_0.png')
o.rotate(180, axis=(0, 1, 0), axis_point=(0,0,0), rad=False)
o.rotate(180, axis=(0, 0, 1), axis_point=(-512/2,512/2,0), rad=False).pos((0,512,0))
p=Line((80,190, 55), (80+150*sin(radians(80))*cos(radians(300)),190+150*sin(radians(80))*sin(radians(300)), 55+150*cos(radians(300))), c=(255,255,255), alpha=1, lw=3, dotted=False, res=None)
# show(a,b,c,f,h,g,d,e,i,j,k,i1,j1,k1,l,m,n,l1,m1,n1,o,p)
q=g.intersectWithLine([80,190, 55], [80+150*sin(radians(80))*cos(radians(300)),190+150*sin(radians(80))*sin(radians(300)), 55+150*cos(radians(300))])
q = Points(q, r=20, c=(0,0,0))
# print(q)
 
r=Line((139.1160888671875, 87.60791778564453, 55), (139.1160888671875, 87.60791778564453, 115.0280532836914), c=(255,255,255), alpha=1, lw=3, dotted=True, res=None)
s=Line((139.1160888671875, 87.60791778564453, 55), (80,190, 55), c=(255,255,255), alpha=1, lw=3, dotted=True, res=None)

v=Arc((80,190, 55), (80+40,190, 55), (80+40*cos(radians(60)),190-40*sin(radians(60)), 55), normal=None, angle=None, invert=True, c=(255,255,255), alpha=1, res=48)
w=Arc((80,190, 55), (80,190, 55+60), (80+60*sin(radians(80))*cos(radians(300)),190+60*sin(radians(80))*sin(radians(300)), 55+60*cos(radians(300))), normal=None, angle=80, invert=False, c=(255,255,255), alpha=1, res=48)



i1=Text('Xc', pos=(200, 0, 0), s=30, justify='bottom-right',  c='r')
i1.rotate(180, axis=(0, 1, 1), axis_point=(200, 0, 0), rad=False)
i1.rotate(-45, axis=(0, 0, 1), axis_point=(200, 0, 0), rad=False)
j1=Text('Yc', pos=(0, 200, 0), s=30, justify='bottom-left',  c='g')
j1.rotate(-270, axis=(1, 0, 0), axis_point=(0, 200, 0), rad=False)
j1.rotate(180, axis=(0, 1, 0), axis_point=(0, 200, 0), rad=False)
j1.rotate(180, axis=(1, 0, 0), axis_point=(0, 200, 0), rad=False)
j1.rotate(-45, axis=(0, 0, 1), axis_point=(0, 200, 0), rad=False)
k1=Text('Zc', pos=(0, 0, 200), s=30, justify='bottom-left',  c='b')
k1.rotate(-270, axis=(1, 0, 0), axis_point=(0, 0, 200), rad=False)
k1.rotate(135, axis=(0, 0, 1), axis_point=(0, 0, 200), rad=False)
l1=Text('Xs', pos=(280, 190, 55), s=30, justify='bottom-right',  c='r')
l1.rotate(180, axis=(0, 1, 1), axis_point=(280, 190, 55), rad=False)
l1.rotate(-45, axis=(0, 0, 1), axis_point=(280, 190, 55), rad=False)
m1=Text('Ys', pos=(80,390, 55), s=30, justify='bottom-left',  c='g')
m1.rotate(-270, axis=(1, 0, 0), axis_point=(80,390, 55), rad=False)
m1.rotate(180, axis=(0, 1, 0), axis_point=(80,390, 55), rad=False)
m1.rotate(180, axis=(1, 0, 0), axis_point=(80,390, 55), rad=False)
m1.rotate(-45, axis=(0, 0, 1), axis_point=(80,390, 55), rad=False)
n1=Text('Zs', pos=(80,190, 255), s=30, justify='bottom-left',  c='b')
n1.rotate(-270, axis=(1, 0, 0), axis_point=(80,190, 255), rad=False)
n1.rotate(135, axis=(0, 0, 1), axis_point=(80,190, 255), rad=False)
t=Text('t', pos=(80,190, 55), s=30, justify='bottom-right',  c=(0,0,0))
u=Text('p(r,θ,φ)', pos=(130.1160888671875, 80.60791778564453, 125.0280532836914), s=30, justify='bottom-right',  c=(0,0,0))
u.rotate(90, axis=(1, 0, 0), axis_point=(130.1160888671875, 80.60791778564453, 125.0280532836914), rad=False)
u.rotate(135, axis=(0, 0, 1), axis_point=(130.1160888671875, 80.60791778564453, 125.0280532836914), rad=False)

show(g,e,i,j,k,l,m,n,o,p,q,r,s,v,w)
# show(g,e,i,j,k,i1,j1,k1,l,m,n,l1,m1,n1,o,p,q,r,s,t,u,v,w)
# show(g,d,e,i,j,k,i1,j1,k1,l,m,n,l1,m1,n1,o,p,q,bg=(0,0,0))