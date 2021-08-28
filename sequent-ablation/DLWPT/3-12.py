from vtkplotter import *
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
showlist=[]
head=r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.9\livertumor1_ALLDATA\livertumor1_output_txt\ndl_2\NSGA-II'
zero=[0,47.5,0.044*20/0.02]
def add_arrow():
	
	a=Arrow(zero, [zero[0]+25,zero[1],zero[2]], s=None, c='r', alpha=1, res=12)
	b=Arrow(zero, [zero[0],zero[1]+25,zero[2]], s=None, c='g', alpha=1, res=12)
	c=Arrow(zero, [zero[0],zero[1],zero[2]+25], s=None, c='b', alpha=1, res=12)
	showlist.append(a)
	showlist.append(b)
	showlist.append(c)

def add_par():
	pareto=np.loadtxt(os.path.join(head,'PARETO_data.txt'))
	a=np.array(pareto[:,5]).reshape(-1,1)
	b=np.array(pareto[:,6]+zero[0]).reshape(-1,1)
	c=np.array(pareto[:,7]*20/0.02).reshape(-1,1)
	res=np.concatenate((a,b),axis=1)
	res=np.concatenate((res,c),axis=1)
	par=Points(res,r=14,c='g')
	showlist.append(par)

def add_pt():
	pt=np.loadtxt(os.path.join(head,'ALL_data.txt'))
	a=np.array(pt[:,5]).reshape(-1,1)
	b=np.array(pt[:,6]+zero[0]).reshape(-1,1)
	c=np.array(pt[:,7]*20/0.02).reshape(-1,1)
	res=np.concatenate((a,b),axis=1)
	res=np.concatenate((res,c),axis=1)
	par=Points(res,r=14,c='black')
	showlist.append(par)









add_arrow()
add_par()
add_pt()
show(showlist)