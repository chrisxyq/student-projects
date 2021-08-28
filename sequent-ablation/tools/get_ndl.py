from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
from math import radians, cos, sin, asin, sqrt

# def get_nearst_pareto():
#     """===============1230修改为医生标记点集的某点,
#     输出的chosen即为get_ndlpointcloud的ptorder==============="""
#     if method==0:
#         pareto=gl.get_value('NSGApareto')
#     else:
#         pareto=gl.get_value('Violent_pareto')
#     phy=gl.get_value('phy')
#     res=[]
    
#     for i in range(len(pareto)):
#         subres=0
#         for j in range(len(phy)):
#             subres+=(pareto[i][2]-phy[j][2])**2+(pareto[i][3]-phy[j][3])**2+(pareto[i][4]-phy[j][4])**2
#         res.append(subres)
#     index=res.index(min(res))

#     return pareto[index,[2,3,4]]


def get_nearst_phy():
    """===============1230修改为医生标记点集的某点,
    输出的chosen即为get_ndlpointcloud的ptorder==============="""
    if method==0:
        pareto=gl.get_value('NSGApareto')
    else:
        pareto=gl.get_value('Violent_pareto')
    phy=gl.get_value('phy')
    res=[]
    
    for j in range(len(phy)):
        subres=0
        for i in range(len(pareto)):
            subres+=(pareto[i][2]-phy[j][2])**2+(pareto[i][3]-phy[j][3])**2+(pareto[i][4]-phy[j][4])**2
        res.append(subres)
    index=res.index(min(res))
    return phy[index][-3:]



def get_ndlline(tar,inpt):
    res=[tar[0:3]]
    a=inpt[0]-tar[0]
    b=inpt[1]-tar[1]
    c=inpt[2]-tar[2]
    lenth=(a**2+b**2+c**2)**0.5
    realin=[inpt[0]+a*ndlength/lenth, inpt[1]+b*ndlength/lenth, inpt[2]+c*ndlength/lenth]
    res.append(realin)
    return res



def get_ndlpointcloud(r):
    ndlname='ndl_'+str(order)
    outpath=os.path.join(deephead, 'MASKS_BMZB', ndlname,ndlname + "BMZB.txt")
    if not os.path.exists(os.path.join(deephead, 'MASKS_BMZB', ndlname)):
        os.makedirs(os.path.join(deephead, 'MASKS_BMZB', ndlname))
    pt1=gl.get_value('targetpos')
    pt2=get_nearst_phy()

    helper=get_ndlline(pt1,pt2)
    np.savetxt(os.path.join(deephead, 'MASKS_BMZB', ndlname,'line.txt'),helper)
    if test_index==0 or test_index==5 or test_index==7:
        
        
        #首先获取笛卡尔坐标：在ct层上的坐标乘以pixel_info

      
        lenn=((pt2[0] - pt1[0])**2+(pt2[1] - pt1[1])**2+(pt2[2] - pt1[2])**2)**0.5
        o = (pt2[0] - pt1[0])/lenn
        p = (pt2[1] - pt1[1])/lenn
        q = (pt2[2] - pt1[2])/lenn    
        n=[o,p,q]
        #求出与n垂直的圆所在平面的两个单位向量u,v
        lenu=(p**2+o**2)**0.5
        ux=p/lenu
        uy=-o/lenu
        uz=0
        u=[ux,uy,uz]
        lenv=((o*q)**2+(p*q)**2+(o**2+p**2)**2)**0.5
        vx=o*q/lenv
        vy=p*q/lenv
        vz=-(o**2+p**2)/lenv
        v=[vx,vy,vz]
        #根据参数方程生成以靶点pt1为圆心，uv为方向坐标轴，半径为r的底面圆的点云circlept(r作为函数参数输入进去的)
        A=[]
        for t in range(0,360,10):   
            circlept=[pt1[0]+r*(ux*cos(radians(t))+vx*sin(radians(t))),pt1[1]+r*(uy*cos(radians(t))+vy*sin(radians(t))),pt1[2]+r*(uz*cos(radians(t))+vz*sin(radians(t)))]
            #对circlept每个点结合进针的方向向量n=[o,p,q]和针长ndlength生成直线散点保存到A
            #1229更新：生成点云长度为针长！而不是进靶距离！
            for s in range(0,int(ndlength),1):
                A.append([circlept[0]+s*n[0],circlept[1]+s*n[1],circlept[2]+s*n[2]])           
        #将结束后的所有点保存为txt即为消融针圆柱表面采样点云
        res=npsampling(A,5)
        np.savetxt(outpath, res, fmt='%s')
        print('点云保存到',outpath)



def txtsampling(txt_path,txtsampled_path,rate):

    txt = open(txt_path, 'r')
    txtall = txt.readlines()
    i = 0    
    txtwrite = []
    while i < len(txtall) - 1:
        if i % rate == 0:
            txtchange = txtall[i]
            txtwrite.append(txtchange)
        i = i + 1
    txtF = open(txtsampled_path, 'w+')
    txtF.writelines(txtwrite)
    txtF.close()

def npsampling(innp,rate):
    #1224用于obsample
    #obsample全局变量，产生于避障约束、利用于myaim.py
    outnp=np.array([])
    i = 0
    while i < len(innp) - 1:
        if i % rate == 0:
            outnp = np.append(outnp,innp[i])
        i = i + 1
    return outnp.reshape(-1,3)
