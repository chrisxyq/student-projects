from hard_tools import *
import globalvar as gl
from round1 import *

from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\tools')
from get_ndl import *

def get_H7():
    if order>1:
        ndlcloud=read_ndlcloud()
        round2=Image.open(os.path.join(opic_ndlpath, 'round2.png'))
        bg = Image.open(os.path.join(head,"bg.png"))
        for ele in ndlcloud:
        	sph=get_spheretf(ele)
        	helper=[int(sph[1]),int(sph[2])]
        	if round2.getpixel((helper[0],helper[1]))==(255,255,255):
        		bg.putpixel(helper,color_dic[7])
        bg.save(os.path.join(opic_ndlpath, 'H7.png'))
        closing(8,'H7')
        minus_pic_and_get_Hskin( "round2",'H7_back','round3')

        denoise('round3')
        read_Feasible()



def read_ndlcloud():
    ndlcloud=[1,1,1] #1.将order之前的消融针圆柱点云增加到obstacles
    for i in range(1,order): 
        ndlname='ndl_'+str(i)
        ndlcloudi = np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', ndlname,ndlname + "BMZB.txt"))    
        ndlcloud=np.vstack((ndlcloud,ndlcloudi))                
    ndlcloud = np.delete(ndlcloud,0, axis = 0)


    allactive = gl.get_value('allactive')
    helper=npsampling(ndlcloud,5)
    allactive_and_ndl = np.vstack((allactive,helper)) 
    gl.set_value('allactive_and_ndl',allactive_and_ndl)

    return ndlcloud