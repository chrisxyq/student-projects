from sklearn.neighbors import KDTree
from hard_tools import *
import globalvar as gl
from kernel_helper import *
from get_ndl import *
from math import ceil


def get_H4():

    #输入分类的障碍字典
    #输出各个分类等级的障碍点闭运算前后的图片
    
    #将H3图片初始化为全黑
    H4_exclude= cv2.imread(os.path.join(head, 'bg.png'))
    allactive= []

    # oblist=['portalvein']



    for obname in oblist:
        #print('正计算',obname)
        obname_exclude= cv2.imread(os.path.join(head, 'bg.png'))
        (sortob_dic,active)=get_sortob_dic(obname)
        allactive.extend(active)
        if sortob_dic!=0:
            for i in range(len(sortob_dic)):
                #对每一个分类等级进行相应的闭运算
                helper=list(sortob_dic.values())[i]
                if len(helper)>20:
                    angle=[[int(ele[1]),int(ele[2])] for ele in helper]
                    size=list(sortob_dic.keys())[i]
                    anglename=obname+'sort'+str(size)
                    angle_to_pic(angle,anglename,0)
                    closing(size,anglename)


                    #合并所有的障碍
                    picname=anglename+'_back.png'
                    add= cv2.imread(os.path.join(opic_ndlpath, picname))
                    obname_exclude = cv2.add(obname_exclude,add)

            cv2.imwrite(os.path.join(opic_ndlpath, obname+'_exclude.png'), obname_exclude )
            minus_pic_and_get_Hskin( "round1",obname+'_exclude','round2')
            
        else:
            #如果这类障碍物点云为空
            cv2.imwrite(os.path.join(opic_ndlpath, obname+'_exclude.png'), obname_exclude )
        


        H4_exclude = cv2.add(H4_exclude,obname_exclude)

    if len(allactive)<500:
        gl.set_value('allactive',np.array(allactive))
    else:
        rate=ceil(len(allactive)/500)
        allactive=npsampling(allactive,rate)
        gl.set_value('allactive',allactive)

    cv2.imwrite(os.path.join(opic_ndlpath, 'H4.png'), H4_exclude )
    #dilate('H4',4)
    OPEN(2,'H4')
    helper_H4()
    change_color('H4',list(color_dic.values())[4])
    minus_pic("round1",'H4','round2')
    get_Hskin("round2")
    get_Hskin("H4")
    








def helper_H4():
    H4=Image.open(os.path.join(opic_ndlpath, 'H4.png'))
    
    F=Image.open(os.path.join(opic_ndlpath, 'skin_back.png'))
    for x in range(181):
        for y in range(361):
            if H4.getpixel((x,y))!=(0,0,0) and F.getpixel((x,y))==(0,0,0):
                H4.putpixel([x,y],(0,0,0))
    H4.save(os.path.join(opic_ndlpath, 'H4.png'))















def get_H5():
    #切角约束
    round2=Image.open(os.path.join(opic_ndlpath, 'round2.png'))
    targetpos=gl.get_value('targetpos')
    H5_angle=[]
    H5_liver=[]
    liver_and_angle=[]
    selected_liver_and_angle=[]
    liverdic={}

    for i,ele in enumerate(livernor):
        sph = get_spheretf(ele[0:3])
        xita=int(sph[1])
        phi=int(sph[2])
        liverdic[str(xita)+','+str(phi)]=[sph[0],ele[0:3]]

        liver_and_angle.append([ele[0],ele[1],ele[2],xita,phi])

        if round2.getpixel((xita,phi))==(255,255,255):

            selected_liver_and_angle.append([ele[0],ele[1],ele[2],xita,phi])


            res1 = 0
            res2 = 0
            #res3 = 0.0
            for j in range(3):
                res1 += (ele[j]-targetpos[j]) * ele[j+3]#靶肝向量与肝法向量之积
                res2 += (ele[j]-targetpos[j]) ** 2#靶肝向量的模的平方
                #res3 += ele[j+3] ** 2#肝法向量的模的平方
            # liverangle=degrees(acos(abs(res1 / ((res2 * res3) ** 0.5))))
            liverangle=degrees(acos(abs(res1 / (res2 ** 0.5))))
            if liverangle>liverangle_threshold:
                H5_angle.append([xita,phi])
                H5_liver.append(ele[0:3])
    np.savetxt(os.path.join(otxt_hardpath,'H5','H5_liver.txt'),H5_liver)
    np.savetxt(os.path.join(otxt_hardpath,'H5','SELECTED_liver.txt'),selected_liver_and_angle)
    gl.set_value('selected_liver_and_angle', selected_liver_and_angle)
    gl.set_value('liver_and_angle', liver_and_angle)

    angle_to_pic(H5_angle,'H5',5)
    closing(7,'H5') if test_index!=6 else closing(15,'H5')

    # closing(2,'H4') if test_index!=5 or test_index!=6 else closing(9,'H4')
    minus_pic_and_get_Hskin("round2",'H5_back','round2')
    gl.set_value('liverdic',liverdic)





def get_newH6():
    #肝脏距离约束
    round2=Image.open(os.path.join(opic_ndlpath, 'round2.png'))
    targetpos=gl.get_value('targetpos')

    liver_and_angle=gl.get_value('liver_and_angle')
    # selected_liver=[ele[0:3] for ele in selected_liver_and_angle]
    tree = KDTree(liver)

    H6_angle=[]
    H6_liver=[]
    indices_list=[]
    selected_tmr=[]

    R=safe_dic[test_index]
    for ele in tmrsurf:
        sph = get_spheretf(ele)
        xita=int(sph[1])
        phi=int(sph[2])
        # if round2.getpixel((xita,phi))==(255,255,255):
        #     selected_tmr.append(ele)

        indices = tree.query_radius([ele], r=R)
        indices_list.extend(indices[0])# indices[0]即为indices的内容，是一个list

        if test_index==4:
            if len(indices[0])>0 and round2.getpixel((xita,phi))==(255,255,255) :
                # print(xita,phi)
                H6_angle.append([xita,phi])
    indices_list = list(set(indices_list))# 1343062→7568
    #为了同时排除延长线不符合距离约束的情况
    print('len(indices_list)',len(indices_list))
    if len(indices_list)>10:
        for j in range(len(indices_list)):
            angle=liver_and_angle[indices_list[j]][-2:]
            liverpt=liver_and_angle[indices_list[j]][:3]
            mirror=[180-angle[0],angle[1]+180] if angle[1]<=180 else [180-angle[0],angle[1]-180]
            if round2.getpixel((int(angle[0]),int(angle[1])))==(255,255,255) :
                H6_angle.append(angle)
            # if round2.getpixel((int(mirror[0]),int(mirror[1])))==(255,255,255) :
            #     H6_angle.append(mirror)
            #if round2.getpixel((int(liverpt[0]),int(liverpt[1])))==(255,255,255):
            #print((int(liverpt[0]),int(liverpt[1])))
                H6_liver.append(liverpt)
        np.savetxt(os.path.join(otxt_hardpath,'H6','H6_liver.txt'),H6_liver)
        np.savetxt(os.path.join(otxt_hardpath,'H6','selected_tmr.txt'),selected_tmr)
        angle_to_pic(H6_angle,'H6',6)
        closing(16,'H6')
        helper()

        minus_pic_and_get_Hskin("round2",'H6_back','round2')
    else:
        bg = Image.open(os.path.join(head,"bg.png"))
        bg.save(os.path.join(opic_ndlpath, 'H6_back.png'))
    H6_helper()



def helper():
    
    a=Image.open(os.path.join(opic_ndlpath, 'H4.png')) 
    #c=Image.open(os.path.join(opic_ndlpath, 'round2.png')) 
    b=Image.open(os.path.join(opic_ndlpath, 'H6_back.png')) 
    for x in range(181):
        for y in range(360):
            #if a.getpixel((x,y))==255:
            if a.getpixel((x,y))!=(0,0,0) and b.getpixel((x,y))!=(0,0,0):
                b.putpixel([x,y],(0,0,0))
    b.save(os.path.join(opic_ndlpath, 'H6_back.png'))


















def get_H6():
    #肝脏距离约束
    round2=Image.open(os.path.join(opic_ndlpath, 'round2.png'))
    targetpos=gl.get_value('targetpos')

    selected_liver_and_angle=gl.get_value('selected_liver_and_angle')
    selected_liver=[ele[0:3] for ele in selected_liver_and_angle]
    tree = KDTree(selected_liver)

    H6_angle=[]
    H6_liver=[]
    indices_list=[]
    selected_tmr=[]

    R=safe_dic[test_index]
    for ele in tmrsurf:
        sph = get_spheretf(ele)
        xita=int(sph[1])
        phi=int(sph[2])
        if round2.getpixel((xita,phi))==(255,255,255):
            selected_tmr.append(ele)

            indices = tree.query_radius([ele], r=R)
            indices_list.extend(indices[0])# indices[0]即为indices的内容，是一个list
    indices_list = list(set(indices_list))# 1343062→7568
    #为了同时排除延长线不符合距离约束的情况
    print('len(indices_list)',len(indices_list))
    if len(indices_list)>10:
        for j in range(len(indices_list)):
            angle=selected_liver_and_angle[indices_list[j]][-2:]
            liverpt=selected_liver_and_angle[indices_list[j]][:3]
            mirror=[180-angle[0],angle[1]+180] if angle[1]<=180 else [180-angle[0],angle[1]-180]
            H6_angle.append(angle)
            if round2.getpixel((int(mirror[0]),int(mirror[1])))==(255,255,255):
                H6_angle.append(mirror)
            #if round2.getpixel((int(liverpt[0]),int(liverpt[1])))==(255,255,255):
            #print((int(liverpt[0]),int(liverpt[1])))
            H6_liver.append(liverpt)
        np.savetxt(os.path.join(otxt_hardpath,'H6','H6_liver.txt'),H6_liver)
        np.savetxt(os.path.join(otxt_hardpath,'H6','selected_tmr.txt'),selected_tmr)
        angle_to_pic(H6_angle,'H6',6)
        closing(12,'H6') if test_index!=8 else closing(16,'H6')
        if test_index!=4:
            OPEN(2,'H6_back')
        print('test_index',test_index)
        if test_index==8 or test_index==7 or test_index==0:
            erode('H6_back',3)
        minus_pic_and_get_Hskin("round2",'H6_back','round2')
    else:
        bg = Image.open(os.path.join(head,"bg.png"))
        bg.save(os.path.join(opic_ndlpath, 'H6_back.png'))
    H6_helper()




# def get_H6():
#     #肝脏距离约束
#     round2=Image.open(os.path.join(opic_ndlpath, 'round2.png'))
#     targetpos=gl.get_value('targetpos')

#     R=safe_dic[test_index]
#     H6_angle=[]
#     H6_liver=[]

#     tmrdic=get_tmrdic()
#     liverdic=gl.get_value('liverdic')

#     np.savetxt(r'E:/liverdic.txt',list(liverdic.keys()),fmt='%s')
#     np.savetxt(r'E:/tmrdic.txt',list(tmrdic.keys()),fmt='%s')


#     for key in liverdic:
#         helper = key.split(",")
#         xita=int(helper[0])
#         phi=int(helper[1])
#         mirror=str([180-xita,phi+180]) if phi<=180 else str([180-xita,phi-180])
#         if round2.getpixel((xita,phi))==(255,255,255) :
#             if key in tmrdic and mirror in tmrdic and mirror in liverdic:
#                 print(liverdic[key][0],tmrdic[key][0])
#                 if liverdic[key][0]-tmrdic[key][0]<R or liverdic[mirror][0]-tmrdic[mirror][0]<R:
#                     H6_angle.append([xita,phi])
#                     H6_liver.append(liverdic[key][1])

#     if len(H6_angle)>10:
#         np.savetxt(os.path.join(otxt_hardpath,'H6','H6_liver.txt'),H6_liver)
#         np.savetxt(os.path.join(otxt_hardpath,'H6','H6_angle.txt'),H6_angle)
#         angle_to_pic(H6_angle,'H6',6)
#         closing(12,'H6')
#         if test_index!=4:
#             OPEN(2,'H6_back')
#         if test_index==8 or test_index==7 or test_index==0:
#             erode('H6_back',3)
#         minus_pic_and_get_Hskin("round2",'H6_back','round2')
#     else:
#         bg = Image.open(os.path.join(head,"bg.png"))
#         bg.save(os.path.join(opic_ndlpath, 'H6_back.png'))
#     H6_helper()
