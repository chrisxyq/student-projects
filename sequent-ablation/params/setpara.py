import os
import numpy as np
import sys
import re
import globalvar as gl
gl._init()


"""病例参数"""
test_index=8

# """算法参数"""
method=1 #0是NSGA-II、1是遍历
if method==1:    
	goalnum=3#method=1的时候有用，遍历法的时候设置的目标数
	only_feasible_flag=1#用于hard_exclude(only_feasible_flag)和get_ndlplan(only_feasible_flag)
if method==0:
	NIND=50 #种群的规模
	MAXGEN = 50 #迭代代数

liverdist_rate_dic={0:3, 1:3, 2:5, 3:4, 4:3, 5:3, 6:3, 7:3, 8:3}

H3kernel_dic={0:15, 1:25, 2:20, 3:15, 4:15, 5:36, 6:30, 7:15, 8:14}

head =r"E:\thesis_task\thesis2\3Dircadb_download"
if test_index==0:
	case,tmrname,order="3Dircadb1.9" ,"livertumor1" ,1
	oblist=['artery','bone','gallbladder','portalvein','venoussystem']
	verse='Test1'
	# obkernel_dic={'artery':6,'bone':4,'gallbladder':20,'portalvein':5,'venoussystem':5}
if test_index==1:
	case,tmrname,order="3Dircadb1.9" ,"livertumor1" ,2
	oblist=['artery','bone','gallbladder','portalvein','venoussystem']
	verse='Test2'
	# obkernel_dic={'artery':6,'bone':6,'gallbladder':20,'portalvein':6,'venoussystem':6}
if test_index==2:
	case,tmrname,order="3Dircadb1.15" ,"livertumor1" ,1
	oblist=['livertumor2','bone','portalvein','venoussystem']
	verse='Test3'
	# obkernel_dic={'livertumor2':4,'bone':4,'portalvein':4,'venoussystem':4}
if test_index==3:
	case,tmrname,order="3Dircadb1.15" ,"livertumor2" ,1
	oblist=['livertumor1','bone','portalvein','venoussystem']
	verse='Test4'
	# obkernel_dic={'livertumor1':4,'bone':4,'portalvein':4,'venoussystem':4}
if test_index==4:
	case,tmrname,order="3Dircadb1.16" ,"livertumor1" ,1
	oblist=['bone','portalvein','venoussystem']
	verse='Test5'
	# obkernel_dic={'bone':4,'portalvein':4,'venoussystem':4}
if test_index==5:
	case,tmrname,order="3Dircadb1.17" ,"livertumor1" ,1
	oblist=['artery','bone','livertumor2','portalvein','venoussystem']
	verse='Test6'
	# obkernel_dic={'artery':4,'bone':4,'livertumor2':4,'portalvein':4,'venoussystem':4}
if test_index==6:
	case,tmrname,order="3Dircadb1.17" ,"livertumor1" ,2
	oblist=['artery','bone','livertumor2','portalvein','venoussystem']
	verse='Test7'
	# obkernel_dic={'artery':4,'bone':4,'livertumor2':4,'portalvein':4,'venoussystem':4}
if test_index==7:
	case,tmrname,order="3Dircadb1.17" ,"livertumor2" ,1
	oblist=['artery','bone','livertumor1','portalvein','venoussystem']
	verse='Test8'
	# obkernel_dic={'artery':4,'bone':4,'livertumor1':4,'portalvein':4,'venoussystem':4}
if test_index==8:
	case,tmrname,order="3Dircadb1.17" ,"livertumor2" ,2
	oblist=['artery','bone','livertumor1','portalvein','venoussystem']
	verse='Test9'
	# obkernel_dic={'artery':6,'bone':4,'livertumor1':4,'portalvein':6,'venoussystem':6}


deephead = os.path.join(head, case, 'MASKS_PNGPTS')




skin = np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'skin', "skinBMZB.txt"))
"""1.3切角约束"""
livernor = np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'liver', "liver_surfnormal.txt")) 
"""1.4肝脏距离约束：使用肝脏、肿瘤表面坐标"""
liver = np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', 'liver', "liverBMZB.txt") )
tmrsurf = np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', tmrname,tmrname + "BMZB.txt"))



ndlength=150
# r ,k ,ndlength= 30,37/30,150 #短轴最大直径为3cm、长短轴比例为1.2,针长为15cm



liverangle_threshold=70  
safe_dic={0:10**(-4), 1:0.5*10**(-5), 2:5, 3:5, 4:15, 5:5, 6:5, 7:0.3*10**(-5), 8:0.3*10**(-5)}#肝脏肿瘤安全距离设置
ratek_dic={0:2, 1:2, 2:100, 3:100, 4:7, 5:4, 6:4, 7:2, 8:2}#ratek用于风险水平计算真实的靶点


vtk_dic= {'artery.vtk': (165,42,42,1), 'bone.vtk': (189,183,107,1), 'gallbladder.vtk': (255,182,193,1),
'liver.vtk': (255,160,122,0.5),  'livertumor.vtk': (105,105,105,0.5),'livertumor1.vtk': (10,10,10,0.5),'livertumor2.vtk': (10,10,10,0.5),
'portalvein.vtk': (32,178,170,1), 'skin.vtk': (255,255,255,0.3), 'venoussystem.vtk':(32,178,170,1)}

#livertumor(105,105,105,1)

#键为硬约束的编号
# color_dic = {0:(255,255,255),	1:(200,200,169),2: (131,175,155), 3: (240,230,140), 4: (255,20,147),
# 5: (0,255,255), 6: (0,0,128), 7: (255,99,71)}
color_dic = {0:(255,255,255),	1:(200,200,169),2: (131,175,155), 3:(249 ,205 ,173),4: (240,230,140), 5: (255,99,71),
6: (0,255,255), 7: (0,0,128)}
RGB_feasible=(255,165,0)#橙色 Orange
RGB_feasible_inv=(0,165,255)

RGB_pareto=(0,255,0)#酸橙色 Lime
RGB_doctor=(255,0,255)#洋红	Magenta







tmrdcm_dir = os.path.join(deephead, 'MASKS_DICOM', tmrname)       
tmr_dir = os.path.join(deephead, 'MASKS_体素坐标', tmrname, tmrname + "体素坐标.txt")  

otxt_path = os.path.join(head, case, tmrname+ '_ALLDATA',tmrname+'_output_txt')
opic_path = os.path.join(head, case, tmrname+ '_ALLDATA',tmrname+'_output_png') 

otxt_hardpath=os.path.join(otxt_path,'ndl_'+str(order))
otxt_NSGApath=os.path.join(otxt_hardpath, "NSGA-II")
otxt_violentpath=os.path.join(otxt_hardpath,'violent')

opic_ndlpath = os.path.join(opic_path,'ndl_'+str(order))
result_path = os.path.join(head, case, tmrname+ '_ALLDATA',tmrname+'_result') 


result_ndl_NSGApath=os.path.join(result_path,'ndl_'+str(order), "NSGA-II")
result_ndl_violentpath=os.path.join(result_path, 'ndl_'+str(order),'violent')
# pngouthead=result_ndl_NSGApath if method==0 else result_ndl_violentpath
result_NSGApath=os.path.join(result_path, "NSGA-II") #这两个路径在plot_tools.py里面的get_tmrplan(targets)函数内定义:
result_violentpath=os.path.join(result_path, 'violent')

if not os.path.exists(otxt_NSGApath):
    os.makedirs(otxt_NSGApath)
if not os.path.exists(otxt_violentpath):
    os.makedirs(otxt_violentpath)


for i in range(1,8):
	ppath=os.path.join(otxt_hardpath,'H'+str(i))
	if not os.path.exists(ppath):
		os.makedirs(ppath)




if not os.path.exists(os.path.join(otxt_violentpath,'three_goal')):
    os.makedirs(os.path.join(otxt_violentpath,'three_goal'))
if not os.path.exists(os.path.join(otxt_violentpath,'two_goal')):
    os.makedirs(os.path.join(otxt_violentpath,'two_goal'))

if not os.path.exists(opic_ndlpath):
    os.makedirs(opic_ndlpath)
if not os.path.exists(result_ndl_NSGApath):
    os.makedirs(result_ndl_NSGApath)
if not os.path.exists(result_ndl_violentpath):
    os.makedirs(result_ndl_violentpath)
# tmr_sampled_dir = os.path.join(deephead, 'MASKS_体素坐标_DILATED', tmrname, tmrname + "体素坐标_DILATED_c5.txt")
# tmr_sampled = np.loadtxt(tmr_sampled_dir) 

"""
otxt_path：存放某肿瘤的各针的：两种方法的帕累托点、时间表现、消融针生成点云&遍历的fullresult
opic_path：存放某肿瘤的各针的：可行域渐变图、final_NSGA-II_200_50.png、final_violent_marked.png
"""


"""
otxt_path的子路径：
otxt_hardpath:存放某肿瘤该针的：硬约束输出的txt
otxt_NSGApath:存放某肿瘤该针的：NSGA帕累托点、时间表现、消融针生成点云
otxt_violentpath:存放某肿瘤该针的：violent帕累托点、时间表现、消融针生成点云&遍历的fullresult
"""

#采样障碍点txt：产生于hard.py,调用于soft.py和myaim.py
#obsample_path = os.path.join(otxt_hardpath, 'obstacles_c'+str(int(100//rate))+'.txt')

#某针的图片输出路径

"""result_path：存放某肿瘤的各针的：两种方法的ct进针标记txt、进针路径ct标记图&整体的进针路径ct标记图"""

"""
result_path的子路径：
result_ndl_NSGApath:存放某肿瘤该针的：NSGA的ct进针标记txt、进针路径ct标记图
result_ndl_violentpath:存放某肿瘤该针的：violent的ct进针标记txt、进针路径ct标记图
result_NSGApath:存放某肿瘤NSGA最终规划的进针路径ct标记图
result_violentpath:存放某肿瘤violent最终规划的进针路径ct标记图
"""


"""膨胀kernel尺寸设置"""
# kernel_dic={0:[2], 1:2, 2:100, 3:100, 4:7, 5:4, 6:4, 7:2, 8:2}
#rate=5 #用隔5行采样的障碍计算风险
"""hardcolorpic颜色设置"""
# invcolordict = {'RGB1': (203,192,255), 'RGB2': (140,230,240), 'RGB3': (147,20,255),
# 'RGB4': (255,255,0), 'RGB5': (255,0,0), 'RGB6': (71,99,255)}#用于hard_exclude(only_feasible_flag,verse) BGR
# colordict = {'RGB1': (255,192,203), 'RGB2': (240,230,140), 'RGB3': (255,20,147),
# 'RGB4': (0,255,255), 'RGB5': (0,0,255), 'RGB6': (255,99,71)}
# RGB1=(255,192,203)#粉红	Pink
# RGB2=(240,230,140)#卡其 Khaki
# RGB3=(255,20,147)#	深粉色 	DeepPink
# RGB4=(0,255,255)#青色	Cyan
# RGB5=(0,0,255)#	纯蓝  Blue
# RGB6=(255,99,71)#番茄	Tomato




 

# dict = {'3Dircadb1.16': '1', '3Dircadb1.9': '2', '3Dircadb1.17': '3',
# '3Dircadb1.15': '3', '3Dircadb1.8': '3', '3Dircadb1.2': '1',
# '3Dircadb1.3': '1'}#病例字典类型：1单发小肿瘤、2单发大肿瘤、3多发大肿瘤


# #20200102增加病例编号
# if case!="3Dircadb1.9":
#     verse=(re.findall(r"\d+\.?\d*",case)[1][-2:]+'-'+re.findall(r"\d+\.?\d*",tmrname)[0]+
#         '-'+str(order))
# else:
#     verse=('9-1-'+str(order))
# gl.set_value('verse', verse)