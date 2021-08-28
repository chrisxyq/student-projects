from vtkplotter import *
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\preprocess')
from get_targetstxt import *
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
	alpha=1
	r=10
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H1','H1_skin.txt'))
	a=Points(helper,c=color_dic[1],r=r, alpha=alpha)
	showlist.append(a)
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H2','H2_skin.txt'))
	a=Points(helper,c=color_dic[2],r=r, alpha=alpha)
	showlist.append(a)
	helper= np.loadtxt(os.path.join(otxt_hardpath,'H3','H3_skin.txt'))
	a=Points(helper,c=color_dic[3],r=r, alpha=0.6)
	showlist.append(a)
	# helper= np.loadtxt(os.path.join(otxt_hardpath,'H4','H4_skin.txt'))
	# a=Points(helper,c=color_dic[4],r=r, alpha=alpha)
	# showlist.append(a)
	# helper= np.loadtxt(os.path.join(otxt_hardpath,'H5','H5_back_skin.txt'))
	# a=Points(helper,c=color_dic[5],r=r, alpha=alpha)
	# showlist.append(a)
	# if test_index!=3 and test_index!=2:
	# 	helper= np.loadtxt(os.path.join(otxt_hardpath,'H6','H6_back_skin.txt'))
	# 	a=Points(helper,c=color_dic[6],r=r, alpha=alpha)
	# 	showlist.append(a)
	# if order>1:
	# 	helper= np.loadtxt(os.path.join(otxt_hardpath,'H7','H7_back_skin.txt'))
	# 	a=Points(helper,c=color_dic[7],r=r, alpha=alpha)
	# 	showlist.append(a)

# def add_skin():
# 	alpha=1
# 	a1=load(os.path.join(otxt_hardpath,'H1','H1_skin.txt'), c=color_dic[1], alpha=alpha)
# 	a2=load(os.path.join(otxt_hardpath,'H2','H2_skin.txt'), c=color_dic[2], alpha=alpha)
	
# 	a3=load(os.path.join(otxt_hardpath,'H3','H3_skin.txt'), c=color_dic[3], alpha=alpha)
# 	# a4=load(os.path.join(otxt_hardpath,'H4','H4_back_skin.txt'), c=color_dic[4], alpha=alpha)
# 	# a5=load(os.path.join(otxt_hardpath,'H5','H5_back_skin.txt'), c=color_dic[5], alpha=alpha)
	
# 	showlist.append(a1)
# 	showlist.append(a2)
# 	showlist.append(a3)
# 	# showlist.append(a4)
# 	# showlist.append(a5)
# 	# if order>1:
# 	# 	a6=load(os.path.join(otxt_hardpath,'H6','H6_back_skin.txt'), c=color_dic[6], alpha=alpha)
# 	# 	showlist.append(a6)



def add_ndl():
	ndlpts=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_'+str(order),'line.txt'))
	a = Line(ndlpts[0],ndlpts[1], c=(255,0,255),lw=5)
	#a = Line(ndlpts[0],ndlpts[1], c='black',lw=5)
	b=Points([ndlpts[0]],r=25,c='white')
	c=show_elli(ndlpts[1],ndlpts[0],rlist[test_index],ratelist[test_index-1])
	showlist.append(a)
	showlist.append(b)
	showlist.append(c)

def add_pre_ndl():
	if order>1:
		ndlpts=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'ndl_1','line.txt'))
		a = Line(ndlpts[0],ndlpts[1], c='r',lw=5)
		b=Points([ndlpts[0]],r=25,c='r')
		c=show_elli(ndlpts[1],ndlpts[0],rlist[test_index-1],ratelist[test_index-1])
		showlist.append(a)
		showlist.append(b)
		showlist.append(c)

# def add_gradient():
# 	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
# 	a=Points(full[:,[2,3,4]],c=colorMap(-full[:,-3], name='hot', vmin=min(-full[:,-3]), vmax=max(-full[:,-3])),r=15, alpha=0.2)
# 	showlist.append(a)

# def add_gradient():
# 	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
# 	a=Points(full[:,[2,3,4]],c=colorMap(1/full[:,-2], name='hot', vmin=min(1/full[:,-2]), vmax=max(1/full[:,-2])),r=15, alpha=0.2)
# 	showlist.append(a)

def add_gradient():
	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
	a=Points(full[:,[2,3,4]],c=colorMap(1/full[:,-1], name='hot', vmin=min(1/full[:,-1]), vmax=max(1/full[:,-1])),r=15, alpha=0.2)
	showlist.append(a)





def show_res():
	add_basic()
	add_skin()
	
	# add_ndl()
	# # add_gradient()
	# add_pre_ndl()
	get_targetstxt()
	targetpos=gl.get_value('targetpos')[0:3]
	f=Point(targetpos, r=15, c='white')
	showlist.append(f)
	
	
	
	# add_par()
	# add_phy()
	show(showlist)



show_res()