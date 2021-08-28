from vtkplotter import *
from sys import path
from PIL import Image, ImageDraw
import numpy as np
import os
# path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
# from setpara import *


showlist=[]

# def add_gradient():
#     full=purefull()
# 	#full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
#     a=Points(full[:,[2,3,4]],c=colorMap(full[:,-3], name='rainbow', vmin=min(full[:,-3]), vmax=max(full[:,-3])),r=15, alpha=0.2)
#     showlist.append(a)
#     show(showlist)

# def add_gradient():
	
# 	#full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
# 	# a=Points(full[:,[2,3,4]],c=colorMap(1/full[:,-2], name='hot', vmin=min(1/full[:,-2]), vmax=max(1/full[:,-2])),r=15, alpha=0.2)
# 	# #showlist.append(a)
# 	full=purefull()
# 	print(full)
# 	a=Points(full[:,[2,3,4]],c=colorMap(full[:,-2], name='rainbow', vmin=min(full[:,-2]), vmax=max(full[:,-2])),r=15, alpha=0.2)
# 	showlist.append(a)

# 	show(showlist)
	# show(a,Text2D(__doc__))
	

def add_gradient():
    full=purefull()
    print(full)
    #full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'))
    #a=Points(full[:,[2,3,4]],c=colorMap(1/full[:,-1], name='rainbow', vmin=min(1/full[:,-1]), vmax=max(1/full[:,-1])),r=15, alpha=0.2)
    a=Points(full[:,[2,3,4]],c=colorMap(-1/full[:,-1], name='rainbow', vmin=min(-1/full[:,-1]), vmax=max(-1/full[:,-1])),r=15, alpha=0.2)
    
    showlist.append(a)
    show(showlist)


def purefull():
	opic_ndlpath=r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_png\ndl_2'
	otxt_violentpath=r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_txt\ndl_2\violent'
	a=Image.open(os.path.join(opic_ndlpath, 'helper.png'))
	full= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+'2'+'violent_fullresult.txt'))
	res=[]
	for ele in full:
		if a.getpixel((int(ele[0]),int(ele[1])))==(255,255,255):
			res.append(ele)
	return np.array(res)



# def helper():
#     opic_ndlpath=r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor1_ALLDATA\livertumor1_output_png\ndl_2'
#     a=Image.open(os.path.join(opic_ndlpath, 'helper.png'))
#     for x in range(181):
#         for y in range(355,361):
#             if a.getpixel((x,y))==(255,255,255):
#                 if a.getpixel((x,y))!=(0,0,0):
#                     a.putpixel([x,y],(0,0,0))
#     a.save(os.path.join(opic_ndlpath, 'helper.png'))

# helper()

def add_efficiency():

    data=np.loadtxt(r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_txt\ndl_2\efficiency.txt')
    full=purefull()
    # print(full)
    a=Points(full[:,[2,3,4]],c=colorMap(-data[:,-1], name='hot', vmin=min(-data[:,-1]), vmax=max(-data[:,-1])),r=15, alpha=0.2)
    showlist.append(a)
    showlist.append(Text2D('F_angle'))
    show(showlist)


# add_gradient()
add_efficiency()