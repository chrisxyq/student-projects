from vtkplotter import *
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
showlist=[]

filePath= os.path.join(deephead, 'MESHES_VTK')
k=37/30
rlist=[30,35,30,30,30,30,30,30]
ratelist=[0.05,0,0,0,0,0,0,0]

def add_basic():
	eles=['liver.vtk','livertumor.vtk','skin.vtk']
	for ele in eles:
		c=vtk_dic[ele][0:3]
		alpha=vtk_dic[ele][-1]
		a=load(os.path.join(filePath, ele), c=c, alpha=alpha)
		showlist.append(a)

# 

# def add_ndl():
# 	ndlpts=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_'+str(order),'line.txt'))
# 	TXT=np.loadtxt(os.path.join(otxt_hardpath,'H6','H6_back_skin.txt'))
# 	og=TXT[0]
# 	xx=og[0]-ndlpts[0][0]
# 	yy=og[1]-ndlpts[0][1]
# 	zz=og[2]-ndlpts[0][2]
# 	LENTH=(xx**2+yy**2+zz**2)**0.5
# 	helper=[og[0]+xx*150/LENTH,og[1]+yy*150/LENTH,og[2]+zz*150/LENTH]
# 	a = Line(ndlpts[0],helper, c='black',lw=5)
# 	b=Points([ndlpts[0]],r=10,c='black')
# 	showlist.append(a)
# 	showlist.append(b)

def add_ob():
	#eles=['boneactive.txt']
	eles=['boneactive.txt','gallbladderactive.txt','portalveinactive.txt','venoussystemactive.txt']
	for ele in eles:
		c=(255,255,0)
		alpha=1
		a=load(os.path.join(otxt_hardpath,'H3', ele), c=c, alpha=alpha)
		showlist.append(a)


def show_res():
	add_basic()
	#add_ndl()
	add_ob()
	show(showlist)





show_res()


# def add_phy():
# # 	phy=np.loadtxt(os.path.join(otxt_hardpath,'phy.txt'))
# # 	print(phy)
# # 	a=Points(phy[:,[2,3,4]],r=10,c=RGB_doctor)
# 	showlist.append(a)

# # def add_par():
# # 	par=np.loadtxt(os.path.join(otxt_NSGApath,'ndl_'+str(order)+'NSGA_pareto.txt')) 
# # 	a=Points(par[:,[2,3,4]],r=10,c=RGB_pareto)
# # 	showlist.append(a)