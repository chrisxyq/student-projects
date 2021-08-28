from vtkplotter import *
from sys import path
from PIL import Image, ImageDraw
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
showlist=[]

filePath= os.path.join(deephead, 'MESHES_VTK')
k=37/30
rlist=[30,35,30,30,30,30,30,30,30]
ratelist=[0.05,0,0,0,0,0,0,0,0]

def add_basic():
    eles=os.listdir(filePath)
    for ele in eles:
        if ele!='liver.vtk' and ele!='skin.vtk':
            c=vtk_dic[ele][0:3]
            alpha=vtk_dic[ele][-1]
            a=load(os.path.join(filePath, ele), c=c, alpha=alpha)
            showlist.append(a)

def add_ndl():
    skin=load(os.path.join(filePath, 'skin.vtk'), c=vtk_dic['skin.vtk'][0:3], alpha=vtk_dic['skin.vtk'][-1])
    liver=load(os.path.join(filePath, 'liver.vtk'), c=vtk_dic['liver.vtk'][0:3], alpha=vtk_dic['liver.vtk'][-1])
    showlist.append(liver)
    showlist.append(skin)
    # tar1=[218.1780014634133, 143.88800096511844, 169.60000252723694]
    # in1=[218,73.5,194 ]
    # helper1=[in1[0]+(in1[0]-tar1[0])*0.5,in1[1]+(in1[1]-tar1[1])*0.5,in1[2]+(in1[2]-tar1[2])*0.5]
    tar2=[95.84699624776836, 148.5999941825866, 160.0000023841858]
    in2=[49.03799808, 131.51099485,160.00000238]
    helper2=[in2[0]+(in2[0]-tar2[0])*0.5,in2[1]+(in2[1]-tar2[1])*0.5,in2[2]+(in2[2]-tar2[2])*0.5]

    # a = Line(tar1,helper1, c='black',lw=5)
    # b=Points([tar1],r=15,c='white')
    # showlist.append(a)
    # showlist.append(b)
    a1 = Line(tar2,helper2, c='black',lw=5)
    b1=Points([tar2],r=5,c='white')
    showlist.append(a1)
    showlist.append(b1)
    # pts = skin.intersectWithLine(tar1,helper1)
    # # print(pts)
    # j = Points(pts, r=15, c='r')
    # showlist.append(j)
    pts = skin.intersectWithLine(tar2,helper2)
    print(pts)
    j = Points(pts, r=15, c='r')
    showlist.append(j)
    # pts = liver.intersectWithLine(tar1,helper1)
    # j = Points(pts, r=15, c='r')
    # showlist.append(j)
    pts = liver.intersectWithLine(tar2,helper2)
    j = Points(pts, r=15, c='r')

    showlist.append(j)
add_basic()
add_ndl()
show(showlist)