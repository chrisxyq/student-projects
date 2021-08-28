from vtkplotter import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import MultipleLocator
import numpy as np
import os
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')

from setpara import *
full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
a=Points(full[:,[2,3,4]],c=colorMap(1/full[:,-1], name='rainbow', vmin=min(1/full[:,-1]), vmax=max(1/full[:,-1])), alpha=0.3)
show(a)

# ob=np.loadtxt(r'E:/pureob.txt')
# mylist=[]
# # a=Points(ob[:,[4,5,6]],c=colorMap(ob[:,7], name='rainbow', vmin=min(ob[:,7]), vmax=max(ob[:,7])))
# a=Points(ob[:,[4,5,6]],c=colorMap(ob[:,-1], name='rainbow', vmin=min(ob[:,-1]), vmax=max(ob[:,-1])))
# b=load('E:/skin.vtk', c=(255,255,255), alpha=0.2)
# c=Point([96.0, 185.9, 72.0], r=15, c='r')
# d=load('E:/livertumor.vtk', c=(105,105,105), alpha=0.5)
# e = Line([96.0, 185.9, 72.0],[316.9+(316.9-96), 226.9+(226.9-185.9) ,84+(84-72)], c='white',lw=5)
# pts = b.intersectWithLine([96.0, 185.9, 72.0],[316.9+(316.9-96), 226.9+(226.9-185.9) ,84+(84-72)])
# f = Points(pts, r=15, c='r')
# g = Point([316.9, 226.9 ,84], r=15, c='r')
# # show(a,b,c,d,e,f,g,bg='black')
# show(a,b,c,d,e,f,g)
