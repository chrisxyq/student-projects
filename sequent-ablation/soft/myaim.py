import cv2
import os
# from numpy import *
import numpy as np
import time
from sklearn.neighbors import KDTree
from math import radians, cos, sin, asin, sqrt

from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\results')
from plot_tools import *

from sklearn.neighbors import NearestNeighbors

def get_NSGApareto(NDSet,NDSetObjV):
    #从NSGA-II输出结果中整合出pareto
    Feasible=gl.get_value('Feasible')
    skin_dic=gl.get_value('skin_dic')
    pareto=[]
    for ele in NDSet:
        sph=Feasible[int(ele[0])]
        skinpt=skin_dic[str(sph)][1]
        pareto.append([sph[0],sph[1],skinpt[0],skinpt[1],skinpt[2]])
    #[球面角度，皮肤点，目标函数]
    NSGApareto=np.unique(np.concatenate((pareto,NDSetObjV),axis=1),axis=0)
    np.savetxt(os.path.join(otxt_NSGApath,'ndl_'+str(order)+'NSGA_pareto.txt'), NSGApareto, fmt='%s')    

    gl.set_value('NSGApareto',NSGApareto)
    np.set_printoptions(precision=3, suppress=True)
    #print('len(NSGApareto)',len(NSGApareto),'NSGApareto',NSGApareto) 
    get_Hdist_and_Rep(NSGApareto)

def myaim(Chrom, LegV): 
    """
    目标函数规范定义：[f,LegV] = aimfuc(Phen,LegV)
    输入：
    Phen：种群的表现型矩阵
    LegV：种群的可行性列向量，初始化为np.ones((NIND, 1))
    输出：
    f：种群的目标函数值矩阵
    LegV：种群的可行性列向量   
    """
    #目标顺序：角度、深度、风险
    Feasible=gl.get_value('Feasible')
    iterangle=[Feasible[ele[0]] for ele in Chrom]      
    ObjV1 = traj_angle(iterangle)
    ObjV2 = traj_depth(iterangle)
    ObjV3 = traj_risk(iterangle,ObjV2)
    print(1)

    exIdx=[]
    for i in range(len(Chrom)):
        if ObjV1[i]>10 or ObjV2[i]>100  :
            exIdx.append(i) # 得到非可行解在种群中的下标        
    # 惩罚方法： 标记非可行解在可行性列向量LegV中对应的值为0，使用punishing罚函数实质上是对非可行解个体的适应度Fintv作进一步的修改
    LegV[exIdx] = 0 


    return [np.array([ObjV1, ObjV2 , ObjV3]).T, LegV]
    #return [np.array([ObjV2, ObjV3 ]).T, LegV]

"""----------------------------------------------------"""
def traj_angle(iterangle):
    return [abs(ele[0]-90) for ele in iterangle]
    # return abs(iterangle[:,0]-90) 


def traj_depth(iterangle):
    skin_dic=gl.get_value('skin_dic')

    # res=[]
    # for ele in iterangle:
    #     if str(ele) not in skin_dic:
    #         skin_dic[str(ele)]=[10000,[100,100,100]]
    #         res.append(skin_dic[str(ele)][0])
    # return res

    return [skin_dic[str(ele)][0] for ele in iterangle]



def traj_risk(iterangle,F_depth):
    tar=gl.get_value('targetpos')
    skin_dic=gl.get_value('skin_dic')
    obsample =gl.get_value('allactive') if order==1 else gl.get_value('allactive_and_ndl')
    #obsample =gl.get_value('allactive') if order==1 and test_index!=1 else gl.get_value('allactive_and_ndl')
    F_risk=[]
    ratek=ratek_dic[test_index]

    for j in range(len(iterangle)):#这里面j的大小即为种群的规模100
        #print(j,iterangle[j])
        inpt=skin_dic[str(iterangle[j])][1]

        """靶点到障碍点向量TO=(o,p,q)"""
        realtar=[tar[0]-(inpt[0]-tar[0])/ratek,tar[1]-(inpt[1]-tar[1])/ratek,tar[2]-(inpt[2]-tar[2])/ratek]
        o = (obsample[:,0] - realtar[0]).reshape(-1, 1)
        p = (obsample[:,1] - realtar[1]).reshape(-1, 1)
        q = (obsample[:,2] - realtar[2]).reshape(-1, 1)
        TO = np.concatenate((o, p, q), axis=1)



        """消融针的方向向量nvec=(l,m,n)"""
        l = sin(radians(iterangle[j][0])) * cos(radians(iterangle[j][1]))
        m = sin(radians(iterangle[j][0])) * sin(radians(iterangle[j][1]))
        n = cos(radians(iterangle[j][0]))
        nvec = [l, m, n]
        ob_sort1 =  []
        ob_sort2 =  []
        ob_vec=[]
        ob_sort3 =  []
        #print("采样后障碍点共有%d个"% (len(obsample)))
     

        for i in range(len(TO)): #对所有障碍物点计算向量之积
            dist=l * TO[i, 0] + m * TO[i, 1] + n * TO[i, 2]
            #print(dist , F_depth[j])
            #1229与针长相比而不是与进针深度相比
            
            if dist <0: #ob_sort1最近点为靶点
                ob_sort1.append(obsample[i])
            elif dist <= ndlength: #ob_sort2最近点为垂足
                ob_vec.append(TO[i])
                ob_sort2.append(obsample[i])
            else: #ob_sort3最近点为针头
                ob_sort3.append(obsample[i])
        ob_vec=np.array(ob_vec)
        # print("离靶点最近的障碍点有%d个，离垂足最近的障碍点有%d个，离针头最近的障碍点有%d个"
        #        % (len(ob_sort1), len(ob_sort2), len(ob_sort3)))


        if len(ob_sort1)>0:
            risk1, ind = KDTree(ob_sort1).query([realtar[0:3]], k=1)
            #print('分类一(离靶点最近)的最近距离',risk1[0][0])
        else:
            risk1=[[10000]]

        #ob_sort2最近点为垂足，向量外积为三角形面积的二倍，底×高也为三角形面积二倍，底为1
        #高=向量外积
        helper1=(1*(m * ob_vec[:, 2] - n * ob_vec[:, 1]))
        helper2=(1*(n * ob_vec[:, 0]-l * ob_vec[:, 2]) )
        helper3=(1*(l * ob_vec[:, 1] - m * ob_vec[:, 0]))
        helper4=(helper1**2+helper2**2+helper3**2)**0.5
        risk2=min(helper4)
        #print('分类二(离垂足最近)的最近距离',risk2)

        if len(ob_sort3)>0: #最近点为进针点
            #print(len(ob_sort3))  
            ndlhead=[realtar[0]+l*ndlength,realtar[1]+m*ndlength,realtar[2]+n*ndlength]             
            risk3, ind = KDTree(ob_sort3).query([ndlhead], k=1)
            #print('分类三(离针头最近)的最近距离',risk3[0][0])
        else:
            risk3=[[10000]]
        risk = 1/(min(risk1[0][0], risk2, risk3[0][0]))
        #print('最终风险水平为',risk)
        F_risk.append(risk)
    return np.array(F_risk).T






def get_phyres():
    phyres=[]
    phy=np.loadtxt(os.path.join(otxt_hardpath,'phy.txt'), dtype=int)
    angle=phy[:,[0,1]].tolist()
    F_depth=traj_depth(angle)
    F_risk=traj_risk(angle,F_depth)
    print(F_depth,F_risk)
    phyres=np.hstack((phy,np.array(F_depth).reshape(-1,1)))
    phyres=np.hstack((phyres,np.array(F_risk).reshape(-1,1)))
    gl.set_value('phyres',phyres)
    # return phyres
	
    
