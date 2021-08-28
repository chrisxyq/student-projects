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
        if ele!='liver.vtk' and ele!='livertumor1.vtk':
            c=vtk_dic[ele][0:3]
            alpha=vtk_dic[ele][-1]
            a=load(os.path.join(filePath, ele), c=c, alpha=alpha)
            showlist.append(a)

a=load(os.path.join(filePath, 'livertumor1.vtk'), c=vtk_dic['livertumor1.vtk'][0:3], alpha=vtk_dic['livertumor1.vtk'][-1])
b=load(os.path.join(filePath, 'liver.vtk'), c=vtk_dic['liver.vtk'][0:3], alpha=vtk_dic['liver.vtk'][-1])
# b.distanceToMesh(a, signed=False, negate=False)
b.distanceToMesh(a, signed=False, negate=True)
# b.addScalarBar(title='Distance\nTo\nTumor(mm)')

#print(s1.getPointArray("Distance"))
showlist=[]
showlist.append(a)
showlist.append(b)
add_basic()
# showlist.append(Text2D(__doc__))
show(showlist)
# show(a, b, Text2D(__doc__))