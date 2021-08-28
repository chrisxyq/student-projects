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
		c=vtk_dic[ele][0:3]
		alpha=vtk_dic[ele][-1]
		a=load(os.path.join(filePath, ele), c=c, alpha=alpha)
		showlist.append(a)
def add_skin():
	alpha=0.6
	r=10
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H1','H1_skin.txt'))
	a=Points(helper,c=color_dic[1],r=r, alpha=alpha)
	showlist.append(a)
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H2','H2_skin.txt'))
	a=Points(helper,c=color_dic[2],r=r, alpha=alpha)
	showlist.append(a)
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H3','H3_skin.txt'))
	a=Points(helper,c=color_dic[3],r=r, alpha=alpha)
	showlist.append(a)
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H4','H4_skin.txt'))
	a=Points(helper,c=color_dic[4],r=r, alpha=alpha)
	showlist.append(a)
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H5','H5_back_skin.txt'))
	a=Points(helper,c=color_dic[5],r=r, alpha=alpha)
	showlist.append(a)
	if test_index!=3 and test_index!=2:
		helper= np.loadtxt(os.path.join(otxt_hardpath,'H6','H6_back_skin.txt'))
		a=Points(helper,c=color_dic[6],r=r, alpha=alpha)
		showlist.append(a)
	if order>1:
		helper= np.loadtxt(os.path.join(otxt_hardpath,'H7','H7_back_skin.txt'))
		a=Points(helper,c=color_dic[7],r=r, alpha=alpha)
		showlist.append(a)
# def add_skin():
# 	alpha=1
# 	a1=load(os.path.join(otxt_hardpath,'H1','H1_skin.txt'), c=color_dic[1], alpha=alpha)
# 	a2=load(os.path.join(otxt_hardpath,'H2','H2_skin.txt'), c=color_dic[2], alpha=alpha)
	
# 	#a3=load(os.path.join(otxt_hardpath,'H3','H3_skin.txt'), c=color_dic[3], alpha=alpha)
# 	a4=load(os.path.join(otxt_hardpath,'H4','H4_back_skin.txt'), c=color_dic[4], alpha=alpha)
# 	a5=load(os.path.join(otxt_hardpath,'H5','H5_back_skin.txt'), c=color_dic[5], alpha=alpha)
	
# 	showlist.append(a1)
# 	showlist.append(a2)
# 	#showlist.append(a3)
# 	showlist.append(a4)
# 	showlist.append(a5)
# 	if order>1:
# 		a6=load(os.path.join(otxt_hardpath,'H6','H6_back_skin.txt'), c=color_dic[6], alpha=alpha)
# 		showlist.append(a6)


def add_phy():
	phy=np.loadtxt(os.path.join(otxt_hardpath,'phy.txt'))
	print(phy)
	a=Points(phy[:,[2,3,4]],r=15,c=RGB_doctor)
	showlist.append(a)

def add_par():
	if method==0:
		par=np.loadtxt(os.path.join(otxt_NSGApath,'ndl_'+str(order)+'NSGA_pareto.txt')) 
	#par=gl.get_value('Violent_pareto') if method==1 else gl.get_value('NSGApareto')
	else:
		if goalnum==3:
			par=np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_pareto.txt'))
		else:
			par=np.loadtxt(os.path.join(otxt_violentpath,'two_goal','ndl_'+str(order)+'violent_pareto.txt'))

	a=Points(par[:,[2,3,4]],r=15,c=RGB_pareto)
	showlist.append(a)

def add_parpath():
	if test_index==0:
			if method==0:
				par=np.loadtxt(os.path.join(otxt_NSGApath,'ndl_'+str(order)+'NSGA_pareto.txt')) 
			#par=gl.get_value('Violent_pareto') if method==1 else gl.get_value('NSGApareto')
			else:
				if goalnum==3:
					par=np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_pareto.txt'))
				else:
					par=np.loadtxt(os.path.join(otxt_violentpath,'two_goal','ndl_'+str(order)+'violent_pareto.txt'))
			helper=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_'+str(order),'line.txt'))
			
			inpt=par[0][2:5]
			tar=helper[0]
			lenth=((tar[0]-inpt[0])**2+(tar[1]-inpt[1])**2+(tar[2]-inpt[2])**2)**0.5
			rate=150/lenth
			sber=[inpt[0]+(inpt[0]-tar[0])*rate,inpt[1]+(inpt[1]-tar[1])*rate,inpt[2]+(inpt[2]-tar[2])*rate]
			a = Line(sber,helper[0], c=RGB_pareto,lw=5)	
			showlist.append(a)
			# c=show_elli(par[0][2:5],helper[0],22,0.05)
			# showlist.append(c)

def add_ndl():
	ndlpts=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_'+str(order),'line.txt'))
	# if test_index==0:
	# 	a = Line(ndlpts[0],ndlpts[1], c=(255,0,255),lw=5)
	# else:
	# 	a = Line(ndlpts[0],ndlpts[1], c='black',lw=5)
	a = Line(ndlpts[0],ndlpts[1], c='black',lw=5)
	b=Points([ndlpts[0]],r=5,c='black')
	#c=show_elli(ndlpts[1],ndlpts[0],rlist[test_index],ratelist[test_index-1])
	showlist.append(a)
	showlist.append(b)
	#showlist.append(c)

def add_pre_ndl():
	if order>1:
		ndlpts=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_1','line.txt'))
		a = Line(ndlpts[0],ndlpts[1], c='r',lw=5)
		b=Points([ndlpts[0]],r=5,c='r')
		#c=show_elli(ndlpts[1],ndlpts[0],rlist[test_index-1],ratelist[test_index-1])
		showlist.append(a)
		showlist.append(b)
		#showlist.append(c)

def add_gradient():
	#full=purefull()
	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
	a=Points(full[:,[2,3,4]],c=colorMap(-full[:,-3], name='hot', vmin=min(-full[:,-3]), vmax=max(-full[:,-3])),r=15, alpha=0.2)
	#a.addScalarBar(title='F_angle')
	showlist.append(a)
	showlist.append(Text2D('F_angle'))

# def add_gradient():
# 	#full=purefull()
# 	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
# 	a=Points(full[:,[2,3,4]],c=colorMap(1/full[:,-2], name='hot', vmin=min(1/full[:,-2]), vmax=max(1/full[:,-2])),r=15, alpha=0.2)
# 	#showlist.append(a)
# 	#a.addScalarBar(title='F_distance')
# 	showlist.append(a)
# 	showlist.append(Text2D('F_distance'))
# 	# show(a,Text2D(__doc__))
	

# def add_gradient():
# 	#full=purefull()
# 	#print(full)
# 	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
# 	a=Points(full[:,[2,3,4]],c=colorMap(1/full[:,-1], name='hot', vmin=min(1/full[:,-1]), vmax=max(1/full[:,-1])),r=15, alpha=0.2)
# 	#a.addScalarBar(title='F_risk')
# 	showlist.append(a)
# 	showlist.append(Text2D('F_risk'))

def purefull():
	a=Image.open(os.path.join(opic_ndlpath, 'Final_denoise.png'))
	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
	res=[]
	for ele in full:
		if a.getpixel((int(ele[0]),int(ele[1])))==(255,255,255):
			res.append(ele)
	return np.array(res)



# def add_ndl2():
# 	ndlpts=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_'+str(order),'line.txt'))
# 	a = Line(ndlpts[0],[20,180,107], c=(255,0,255),lw=5)
# 	#a = Line(ndlpts[0],ndlpts[1], c='black',lw=5)
# 	b=Points([ndlpts[0]],r=25,c='black')
# 	c=show_elli(ndlpts[1],ndlpts[0],rlist[test_index],ratelist[test_index-1])
# 	showlist.append(a)
# 	showlist.append(b)
# 	showlist.append(c)



def show_res():
	add_basic()
	add_skin()
	# #add_ndl2()
	add_ndl()
	# add_gradient()
	add_pre_ndl()
	# add_parpath()
	
	
	add_par()
	# add_phy()
	show(showlist)

#================helper====================

def show_elli(inpt,tar,r,rate):
    #苍白绿
    R=get_elliaxis(inpt,tar)
    #每一个axis指的是直径，因此r要乘以2
    helper=[tar[0]+(inpt[0]-tar[0])*rate,tar[1]+(inpt[1]-tar[1])*rate,tar[2]+(inpt[2]-tar[2])*rate]


    elli_actor=Ellipsoid(pos=helper, axis1=[R[0][0]*2*r/k, R[1][0]*2*r/k, R[2][0]*2*r/k], 
        axis2=[R[0][1]*2*r, R[1][1]*2*r, R[2][1]*2*r], axis3=[R[0][2]*2*r/k, R[1][2]*2*r/k, R[2][2]*2*r/k], c=(152,251,152), alpha=0.8)
    return elli_actor


def get_elliaxis(inpt,tar):
    #输入进针单位向量，输出的单位矩阵每一列分别为椭球坐标系的xyz轴
    lenth=((tar[0]-inpt[0])**2+(tar[1]-inpt[1])**2+(tar[2]-inpt[2])**2)**0.5
    alpha=(tar[0]-inpt[0])/lenth
    beta=(tar[1]-inpt[1])/lenth
    gama=(tar[2]-inpt[2])/lenth

    init=[0,(1-alpha**2)**0.5,gama/((1-alpha**2)**0.5),
    -alpha*beta/((1-alpha**2)**0.5),-beta/((1-alpha**2)**0.5),-alpha*gama/(1-alpha**2)**0.5]
    sol_fsolve =init
    R=[[sol_fsolve[0], alpha, sol_fsolve[1]], [sol_fsolve[2],beta,sol_fsolve[3]], [sol_fsolve[4], gama,sol_fsolve[5]]]
    return R










# # add_gradient()

# show_res()