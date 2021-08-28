
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\hard')

from round1 import *
from round2 import *
from round3 import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\soft')
from myaim import *
from violent_pareto import *
import geatpy as ga
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\results')
from plot_tools import *
from show_res import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\tools')
from get_ndl import *
import time


get_targetstxt()
# get_H1H2H3()


# get_H4()

# get_H5()

# get_newH6() if test_index==4 else get_H6()

# get_H7()
# if method==0:
# 	FNUM=gl.get_value('FNUM' )
# 	FieldDR=np.array([[0], [FNUM-1]])  
# 	AIM_M = __import__('myaim') 
# 	AIM_F = 'myaim'
# 	chrom = ga.crtip(NIND, FieldDR)    
# 	[ObjV, NDSet, NDSetObjV, times] = ga.moea_nsga2_templet(AIM_M, AIM_F,None, None, FieldDR, problem = 'I', maxormin = 1, MAXGEN=MAXGEN ,
# 	    MAXSIZE = 2000, NIND=NIND , SUBPOP = 1, GGAP = 0.5, selectStyle ='tour', recombinStyle = 'xovdprs',
# 	     recopt = 0.9, pm = 0.1,distribute = True, drawing = 0) 
# 	pareto=get_NSGApareto(NDSet,NDSetObjV)
# else:
# 	result=get_fullresult()
# 	pareto=get_Violent_pareto(result)
# get_ndlpointcloud(0.8)
# mark_phyandpar_2D()
# show_res()
# get_phyres()
# NewQuan_analysis()

