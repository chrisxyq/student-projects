from vtkplotter import *
from sys import path
from PIL import Image, ImageDraw
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
showlist=[]

filePath= os.path.join(deephead, 'MESHES_VTK')


def add_basic():
	eles=os.listdir(filePath)
	for ele in eles:
		c=vtk_dic[ele][0:3]
		alpha=vtk_dic[ele][-1]
		a=load(os.path.join(filePath, ele), c=c, alpha=alpha)
		showlist.append(a)

add_basic()
show(showlist)