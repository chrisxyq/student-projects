from sklearn.cluster import KMeans
from jenkspy import jenks_breaks
import numpy as np

from hard_tools import *
 
def goodness_of_variance_fit(array, classes):
    # classes是端点，分成n类即有n+1个断点
    classes = jenks_breaks(array, classes)
    #print('classes',classes)
    # 分类
    classified = np.array([classify(i, classes) for i in array])
    #print('classified',classified)
    maxz = max(classified)
    zone_indices = [[idx for idx, val in enumerate(classified) if zone + 1 == val] for zone in range(maxz)]
    #print('zone_indices',len(zone_indices))
    sdam = np.sum((array - array.mean()) ** 2)
    #print('sdam',sdam)
    # 分类后的各个子部分的数据
    array_sort = [np.array([array[index] for index in zone]) for zone in zone_indices]
    #print('array_sort',len(array_sort))
    sdcm = sum([np.sum((classified - classified.mean()) ** 2) for classified in array_sort])
    #print('sdcm',sdcm)
    #分类效果好坏评价指标
    gvf = (sdam - sdcm) / sdam
    return (gvf,array_sort,classes)
 
 
def classify(value, breaks):
    for i in range(1, len(breaks)):
        if value < breaks[i]:
            return i
    return len(breaks) - 1



def get_sortob_dic(obname):
    #pureob：[ob类型，球坐标，直角坐标，皮肤距离/障碍距离]
    # #1.根据dist_ratio排序pureob
    (ob,active)=get_dist_ratio(obname) 
    #print(len(ob))
    if len(ob)>50:
        ob=sorted(ob,key=lambda x:x[-1])
        # ob=ob[np.lexsort(ob.T)]#按最后一列从小到大排序
        # np.savetxt(os.path.join(otxt_hardpath,'H3',obname+'active.txt'),ob)

        ##2.确定分类种类数array_sort,classes
        gvf = 0.0
        nclasses = 2
        
        array = np.array([ele[-1] for ele in ob] )
        
        while gvf < .8:
            #gvf方差拟合优度：分类判断好坏
            #array_sort：分的nclasses类的具体数据
            #classes：断点，nclasses类共有nclasses+1个断点
            (gvf,array_sort,classes) = goodness_of_variance_fit(array, nclasses)
            #print(nclasses, gvf)
            nclasses += 1
        #3.对ob进行分类并保存txt
        start=0
        end=len(array_sort[0])+1
        sortob_dic={}
        for i in range(len(array_sort)):
            #print(start,end)
            sort_i=ob[start:end]
            #计算断点与闭运算size的关系
            # size= int(4.5*classes[i+1])
            #size= int(2*classes[i+1])

            size= int(classes[i+1])+3 if classes[i+1]<4 else int(2.5*classes[i+1])

            #size= int(classes[i+1]/10)


            sortob_dic[size]=sort_i
            # np.savetxt(os.path.join(otxt_path ,'sort'+str(size)+'.txt'),sort_i)
            if i<len(array_sort)-1:
               start=end
               end=start+len(array_sort[i+1])+1
        return (sortob_dic,active)

    else:
        return (0,active)



def get_dist_ratio(obname):
    #筛选出满足H1H2点云的同时，计算出其dist_ratio
    pureob=[]

    # global skin_angle
    # neigh = NearestNeighbors(n_neighbors=1)
    # neigh.fit([ele[1] for ele in skin_angle])

    skin_dic=gl.get_value('skin_dic')

    ob=np.loadtxt(os.path.join(deephead, 'MASKS_BMZB', obname,obname + "BMZB.txt"))
    round1=Image.open(os.path.join(opic_ndlpath, 'round1.png'))
    active=[]

    if obname=='gallbladder':
        for ele in ob:
            sph=get_spheretf(ele)
            d=sph[0]
            xita=int(sph[1])
            phi=int(sph[2])
            angle=[xita,phi]
            if round1.getpixel((xita,phi))==(255,255,255):

                dist_skin=skin_dic[str(angle)][0]
                dist_ratio=dist_skin/d

                # dist_ratio=d
                pureob.append([d,xita,phi,ele[0],ele[1],ele[2],dist_ratio])
                active.append(ele)
            #这里的mirror不是由筛选后的angle产生的，和angle是并行的两条线
            #最终得到的是筛选后的angle和镜像
            mirror=get_mirror(angle)
            if round1.getpixel((mirror[0],mirror[1]))==(255,255,255):
                #print(angle,mirror)
                pureob.append([d,mirror[0],mirror[1],ele[0],ele[1],ele[2],dist_ratio])
        np.savetxt(os.path.join(otxt_hardpath,'H4',obname+'active.txt'),active)
    elif obname=='ndl_1':
        for ele in ob:
            sph=get_spheretf(ele)
            d=sph[0]
            xita=int(sph[1])
            phi=int(sph[2])
            angle=[xita,phi]

            #dist_ratio=d

            dist_skin=skin_dic[str(angle)][0]
            dist_ratio=dist_skin/d
            pureob.append([d,xita,phi,ele[0],ele[1],ele[2],dist_ratio])
            active.append(ele)
        np.savetxt(os.path.join(otxt_hardpath,'H7',obname+'active.txt'),active)
    else:
        for ele in ob:
            sph=get_spheretf(ele)
            d=sph[0]
            xita=int(sph[1])
            phi=int(sph[2])
            angle=[xita,phi]
            if round1.getpixel((xita,phi))==(255,255,255):

                #dist_ratio=d


                dist_skin=skin_dic[str(angle)][0]
                dist_ratio=dist_skin/d
                pureob.append([d,xita,phi,ele[0],ele[1],ele[2],dist_ratio])
                active.append(ele)
        np.savetxt(os.path.join(otxt_hardpath,'H4',obname+'active.txt'),active)
    return (pureob,active)














