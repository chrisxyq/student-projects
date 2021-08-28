from vtkplotter import *
import numpy as np
from vtkplotter import colorMap
import matplotlib.cm as cm
import matplotlib.pyplot as plt
ob=np.loadtxt(r'E:/pureob.txt')
mylist=[]
# a=Points(ob[:,[4,5,6]],c=colorMap(ob[:,7], name='rainbow', vmin=min(ob[:,7]), vmax=max(ob[:,7])))
a=Points(ob[:,[4,5,6]],c=colorMap(ob[:,-1], name='rainbow', vmin=min(ob[:,-1]), vmax=max(ob[:,-1])))
b=load('E:/skin.vtk', c=(255,255,255), alpha=0.2)
c=Point([96.0, 185.9, 72.0], r=15, c='r')
d=load('E:/livertumor.vtk', c=(105,105,105), alpha=0.5)
e = Line([96.0, 185.9, 72.0],[316.9+(316.9-96), 226.9+(226.9-185.9) ,84+(84-72)], c='white',lw=5)
pts = b.intersectWithLine([96.0, 185.9, 72.0],[316.9+(316.9-96), 226.9+(226.9-185.9) ,84+(84-72)])
f = Points(pts, r=15, c='r')
g = Point([316.9, 226.9 ,84], r=15, c='r')
# show(a,b,c,d,e,f,g,bg='black')
show(a,b,c,d,e,f,g)



# import matplotlib.pyplot as plt
# cm = plt.cm.get_cmap('RdYlBu')
# xy = range(20)
# z = xy
# sc = plt.scatter(xy, xy, c=1, vmin=0, vmax=20, s=35, cmap=cm)
# plt.colorbar(sc)
# plt.show()
