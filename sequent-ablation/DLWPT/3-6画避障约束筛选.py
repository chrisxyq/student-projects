from vtkplotter import *
import numpy as np
from vtkplotter import colorMap
import matplotlib.cm as cm
import matplotlib.pyplot as plt

colordict= {'artery': (165,42,42,1), 'bone': (189,183,107,1), 'gallbladder': (255,182,193,1),
'liver': (255,160,122,0.3),  'livertumor': (105,105,105,0.8),  'livertumor1': (105,105,105,0.8),
  'livertumor2': (105,105,105,0.8),'portalvein': (32,178,170,1), 'skin': (255,255,255,0.3), 
  'venoussystem':(32,178,170,1)}


bone=np.loadtxt(r'E:/2/bone.txt')
a=Points(bone[:,[3,4,5]],c=(189,183,107))
gallbladder=np.loadtxt(r'E:/2/gallbladder.txt')
i=Points(gallbladder[:,[3,4,5]],c=(			244,164,96))
portalvein=np.loadtxt(r'E:/2/portalvein.txt')
j=Points(portalvein[:,[3,4,5]],c=(32,178,170))
venoussystem=np.loadtxt(r'E:/2/venoussystem.txt')
k=Points(venoussystem[:,[3,4,5]],c=(32,178,170))
b=load('E:/skin.vtk', c=(255,255,255), alpha=0.2)
c=Point([96.0, 185.9, 72.0], r=15, c='r')
d=load('E:/livertumor.vtk', c=(105,105,105), alpha=0.5)


# e=load('E:/portalvein.txt', c=(	128,128,128), alpha=0.5)
# f=load('E:/2/H1.txt', c=(255,127,80), alpha=0.7)
# g=load('E:/2/H2.txt', c=(255,192,203), alpha=0.7)
h=load('E:/2/bone_exclude.txt', c=(189,183,107), alpha=0.7)
l=load('E:/2/gallbladder_exclude.txt', c=(		244,164,96), alpha=0.7)
m=load('E:/2/venoussystem_exclude.txt', c=(32,178,170), alpha=0.7)
n=load('E:/2/portalvein_exclude.txt', c=(32,178,170), alpha=0.7)
show(a,b,c,d,h,i,j,k,l,m,n)