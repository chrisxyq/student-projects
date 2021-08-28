
from hard_tools import *
from kernel_helper import *
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\tools')
from vtkplotter import *
from H3_helper import *
def get_H1H2H3():
    #H1_list、H2_list为前胸和针长约束排除的[深度，[角度]，[直角坐标]]
    #allskin_angle为用于画原皮肤的球面角度
    #skin_dict的key是str([角度]),value是0或[直角坐标]

    #step1：计算
    H1_angle=[]
    H1_pts=[]
    H2_angle=[]
    H2_pts=[]
    H3_angle=[]
    H3_pts=[]
    # skin_dict={}
    skin_helper=[]
    global skin_angle
    skin_angle=[]

    liver_dic=get_liverdic()

    

    for ele in skin:
        sph=get_spheretf(ele)
        d=sph[0]
        xita=int(sph[1])
        phi=int(sph[2])
        angle=[xita,phi]
        if phi>9 and phi<171:
            H1_angle.append(angle)
            H1_pts.append(ele)

        elif d>ndlength:
            H2_angle.append(angle)
            H2_pts.append(ele)
        
        elif str(angle) in liver_dic:
            skin_helper.append([d,xita,phi,ele])
          

            ratio=d/liver_dic[str(angle)]


            


            if ratio>liverdist_rate_dic[test_index]:
                #H3_angle.append([xita,phi,ratio])
                H3_angle.append([xita,phi])
                #H3_pts.append(ele)

        else:
            skin_helper.append([d,xita,phi,ele])
            # skin_dict[str(angle)]=ele
        skin_angle.append([d,angle])

    #step2：画图skin、H1、H2
    
    gl.set_value('skin_helper', skin_helper)

    


    np.savetxt(os.path.join(otxt_hardpath,'H1','H1_skin.txt'),H1_pts)
    np.savetxt(os.path.join(otxt_hardpath,'H2','H2_skin.txt'),H2_pts)
    
    angle_to_pic([ele[1] for ele in skin_angle] ,'skin',0)
    closing(4,'skin')

    angle_to_pic(H1_angle,'H1',1)
    closing(4,'H1')

    angle_to_pic(H2_angle,'H2',2)
    closing(4,'H2')

    angle_to_pic(H3_angle,'H3',3)
    H3_helper(H3_angle)
    

    minus_pic("skin_back",'H1_back','round1')
    minus_pic("round1",'H2_back','round1')
    #H3_helper(H3_angle)
    #skin_helper在这里被用来生成skin_dic
    minus_pic_and_get_skin_dic("round1",'H3_back','round1')


def ratio_geter():
    biye_helper=[]
    liver_dic=get_liverdic()
    for ele in skin:
        sph=get_spheretf(ele)
        d=sph[0]
        xita=int(sph[1])
        phi=int(sph[2])
        angle=[xita,phi]
        if str(angle) in liver_dic:

            ratio=d/liver_dic[str(angle)]
            print(d,liver_dic[str(angle)],ratio)
            biye_helper.append([ele[0],ele[1],ele[2],d,ratio,d-liver_dic[str(angle)]])
    helper_path=r'E:\thesis_task\thesis2\3Dircadb_download\liverdist'
    if not os.path.exists(helper_path):
        os.makedirs(helper_path)
    np.savetxt(os.path.join(helper_path,'liverdist'+str(test_index)+'.txt'),biye_helper)
    print('liverdist保存！')

# def H3_helper():
#     img = cv2.imread(os.path.join(opic_ndlpath, 'H3.png'))  
#     imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #彩色转灰度  
#     ret,thresh = cv2.threshold(imgray,127,255,0)   #进行二值化  
#     image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # 检索模式为树形cv2.RETR_TREE，  
#     img = cv2.drawContours(img, contours, -1, color_dic[3],  6) 
#     cv2.imwrite(os.path.join(opic_ndlpath, 'H3_back.png'), img)




def get_liverdic():
    liver_dic={}
    for ele in liver:
        sph=get_spheretf(ele)
        x=int(sph[1])
        y=int(sph[2])
        liver_dic[str([x,y])]=sph[0]

    return liver_dic


# get_targetstxt()
# ratio_geter()



















# def H3_helper(H3_angle):
#     sort_dic=get_sortliver_dic(H3_angle)
#     H3_exclude= cv2.imread(os.path.join(head, 'bg.png'))
#     if sort_dic!=0:
#         for i in range(len(sort_dic)):
#             #对每一个分类等级进行相应的闭运算
#             helper=list(sort_dic.values())[i]
#             if len(helper)>20:
#                 angle=[[int(ele[0]),int(ele[1])] for ele in helper]
#                 size=list(sort_dic.keys())[i]
#                 anglename='H3_sort'+str(size)
#                 angle_to_pic(angle,anglename,0)
#                 closing(size,anglename)


#                 #合并所有的障碍
#                 picname=anglename+'_back.png'
#                 add= cv2.imread(os.path.join(opic_ndlpath, picname))
#                 H3_exclude = cv2.add(H3_exclude,add)

#         cv2.imwrite(os.path.join(opic_ndlpath, 'H3.png'), H3_exclude )
#         erode('H3',2)







# def get_sortliver_dic(H3_angle):
#     H3_angle=sorted(H3_angle,key=lambda x:x[-1])
#     gvf = 0.0
#     nclasses = 2    
#     array = np.array([ele[-1] for ele in H3_angle] )    
#     while gvf < .9:
#         (gvf,array_sort,classes) = goodness_of_variance_fit(array, nclasses)
#         #print(nclasses, gvf)
#         nclasses += 1
#     #3.对ob进行分类并保存txt
#     start=0
#     end=len(array_sort[0])+1
#     sort_dic={}
#     for i in range(len(array_sort)):
#         #print(start,end)
#         sort_i=H3_angle[start:end]
#         #计算断点与闭运算size的关系

#         size= int(classes[i+1]*liverkernel_dic[test_index]) 
#         sort_dic[size]=sort_i
#         # np.savetxt(os.path.join(otxt_path ,'sort'+str(size)+'.txt'),sort_i)
#         if i<len(array_sort)-1:
#            start=end
#            end=start+len(array_sort[i+1])+1
#     return sort_dic







# def get_liverdic():
#     # mesh=load(os.path.join(deephead, 'MASKS_BMZB', 'liver', "liverBMZB.txt"))
#     # a=densifyCloud(mesh, 1, closestN=6, radius=0, maxIter=None, maxN=None)
#     # # show(a,mesh)
#     # helper=a.points()



#     liver_dic={}
#     res=[]
#     for ele in liver:
#         sph=get_spheretf(ele)
#         res.append(sph)
#     np.savetxt(os.path.join(otxt_hardpath,'H3','liver_sph.txt'),res)
#     mesh=load(os.path.join(otxt_hardpath,'H3','liver_sph.txt'))
#     a=densifyCloud(mesh, 1, closestN=6, radius=0, maxIter=None, maxN=None)
#     # show(a,mesh)
#     helper=a.points()
#     for ele in helper:

#         x=int(ele[1])
#         y=int(ele[2])
#         liver_dic[str([x,y])]=ele[0]
#     #print(list(liver_dic.keys()))
#     #np.savetxt(r'E:/NN.txt',list(liver_dic.keys()),fmt='%s')
#     return liver_dic









# def H3_helper(H3_angle):
#     angle_to_pic(H3_angle,'H3_angle',3)
#     np.savetxt(os.path.join(otxt_hardpath,'H3','H3_angle.txt'),H3_angle)
#     mesh=load(os.path.join(otxt_hardpath,'H3','H3_angle.txt'))
#     a=densifyCloud(mesh, 0.2, closestN=6, radius=0, maxIter=None, maxN=None)
#     # show(a,mesh)
#     helper=a.points().astype(int)[:,[0,1]]
#     print(helper)
#     angle_to_pic(helper,'H3',3)
#     # print(a.points())
