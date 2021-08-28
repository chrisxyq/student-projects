from math import radians, cos, sin, asin, sqrt
from myaim import *


def get_fullresult():

    Feasible=gl.get_value('Feasible')
    if goalnum==2:
        Feasible = [n for n in Feasible if 79<n[0]<101 ]
    skin_dic=gl.get_value('skin_dic')
    # if goalnum==2:
    #     Feasible = [n for n in Feasible if n[0]==90 ]
    res1=traj_angle(Feasible)
    res2=traj_depth(Feasible)
    res3=traj_risk(Feasible,res2)
    skinpt=[skin_dic[str(ele)][1] for ele in Feasible]
    res1=np.array(res1).reshape(-1,1)
    res2=np.array(res2).reshape(-1,1)
    res3=np.array(res3).reshape(-1,1)
    print(np.array(Feasible).shape,np.array(skinpt).shape)
    res=np.concatenate((Feasible,skinpt,res1,res2,res3),axis=1)

    # np.savetxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'),res, fmt='%s')
    # print('可行域点遍历结束，结果已保存')

    if goalnum==3:
        np.savetxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt'),res, fmt='%s')
        print('可行域点遍历结束，结果已保存')
    else:
        np.savetxt(os.path.join(otxt_violentpath,'two_goal', 'ndl_'+str(order)+'violent_fullresult.txt'),res, fmt='%s')
        print('同层可行域点遍历结束，结果已保存')
    return res

"""--------------------------violent_pareto.py转移过来的函数---------------------------------------"""
def get_Violent_pareto(result):

    print('开始筛选Violent_pareto点')  
    a = result[:, [5, 6, 7]]
    pareto = []
    i = 0  # i是被考核的，j是考验的
    while i < len(a):
        # 上一个i打到最后一个，由于此时i新+1，vi很陌生，不确定前i-1个数与vi的强弱关系，因此从第一个数开始考验
        j = 0
        while j < len(a):
            if i != j:
                vj1, vj2, vj3 = a[j][0], a[j][1],a[j][2]
                vi1, vi2, vi3 = a[i][0], a[i][1],a[i][2]
                if (vj1 <= vi1 and vj2 <= vi2 and vj3 <= vi3):
                    i += 1
                    break
                else:
                    j += 1
                if j == len(a):
                    pareto.append(result[i])
                    i += 1
                    break
            else:
                # 上一个i是很快死的，j只要从i+1开始考验即可
                j += 1
                if i == len(a) - 1 and j == len(a):
                    pareto.append(result[i])
                    # 需要i+1来跳出最外层的while i < len(a)
                    i += 1
    
    #np.savetxt(os.path.join(otxt_violentpath,'three_goal','ndl_'+str(order)+'violent_pareto.txt'), pareto, fmt='%s')    


    # Violent_pareto=np.array(pareto)
    Violent_pareto=selecter(pareto)

    if goalnum==3:
        np.savetxt(os.path.join(otxt_violentpath,'three_goal','ndl_'+str(order)+'violent_pareto.txt'), Violent_pareto, fmt='%s')    
    else:
        np.savetxt(os.path.join(otxt_violentpath,'two_goal','ndl_'+str(order)+'violent_pareto.txt'),Violent_pareto,  fmt='%s')
    


    gl.set_value('Violent_pareto', Violent_pareto)
    print('Violent_pareto',Violent_pareto)
    get_Hdist_and_Rep(Violent_pareto)
    return Violent_pareto



def selecter(pareto):
    res=[]
    finres=[]
    for ele in pareto:
        #层差<20、phi大于200
        if test_index==5 :
            if ele[5]<20 and ele[1]>250 and ele[1]<285:
                res.append(ele)
        elif test_index==6:
            if ele[5]<20 and ele[1]>250 and ele[1]<285:
                res.append(ele)
        elif test_index==7 or test_index==8:
            if ele[5]<30 and ele[1]<250 and ele[1]>180:
                res.append(ele)
        elif test_index==0 or test_index==1:
            if ele[1]>200: 
                res.append(ele)
        elif test_index==2 :
            # if ele[1]>200 : 
            #     res.append(ele)
            if ele[1]>200 and ele[1]<273: 
                res.append(ele)
        elif test_index==4 :
            if ele[5]<20 and ele[1]>200 and ele[1]<250: 
                res.append(ele)
        else:
            res.append(ele)  
    if goalnum==2:#进一步对针长筛选
        for ele in res:
            if ele[6]<100:
                finres.append(ele) 
    else:
        finres=res
    return np.array(finres)
