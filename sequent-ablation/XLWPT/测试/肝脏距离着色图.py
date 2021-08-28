from vtkplotter import *
a=load(r'E:/livertumor.vtk')
b=load(r'E:/liver.vtk', alpha=0.3)
# b.distanceToMesh(a, signed=False, negate=False)
b.distanceToMesh(a, signed=False, negate=True)
b.addScalarBar(title='Signed\nDistance')

#print(s1.getPointArray("Distance"))
showlist=[]
showlist.append(a)
showlist.append(b)
# showlist.append(Text2D(__doc__))
show(showlist)
# show(a, b, Text2D(__doc__))