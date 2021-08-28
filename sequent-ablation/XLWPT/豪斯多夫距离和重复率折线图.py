from vtkplotter import *
from sys import path
from PIL import Image, ImageDraw
from matplotlib import pyplot
import matplotlib.pyplot as plt
from hausdorff import hausdorff_distance
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *
par_path_dic={1:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.9\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\violent\three_goal\ndl_1violent_pareto.txt',
2:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.9\livertumor1_ALLDATA\livertumor1_output_txt\ndl_2\violent\three_goal\ndl_2violent_pareto.txt',
3:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.15\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\violent\three_goal\ndl_1violent_pareto.txt',
4:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.15\livertumor2_ALLDATA\livertumor2_output_txt\ndl_1\violent\three_goal\ndl_1violent_pareto.txt',
5:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.16\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\violent\three_goal\ndl_1violent_pareto.txt',
6:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\violent\three_goal\ndl_1violent_pareto.txt',
7:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor1_ALLDATA\livertumor1_output_txt\ndl_2\violent\three_goal\ndl_2violent_pareto.txt',
8:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_txt\ndl_1\violent\three_goal\ndl_1violent_pareto.txt',
9:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_txt\ndl_2\violent\three_goal\ndl_2violent_pareto.txt',
}
phy_path_dic={1:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.9\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\phy1.txt',
2:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.9\livertumor1_ALLDATA\livertumor1_output_txt\ndl_2\phy2.txt',
3:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.15\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\phy1.txt',
4:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.15\livertumor2_ALLDATA\livertumor2_output_txt\ndl_1\phy1.txt',
5:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.16\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\phy1.txt',
6:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor1_ALLDATA\livertumor1_output_txt\ndl_1\phy1.txt',
7:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor1_ALLDATA\livertumor1_output_txt\ndl_2\phy2.txt',
8:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_txt\ndl_1\phy1.txt',
9:r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.17\livertumor2_ALLDATA\livertumor2_output_txt\ndl_2\phy2.txt',
    
}

colordic={1:(1,0,0),2:(255/255,165/255,0),3:(1,1,0),4:(0,1,0),5:(0,127/255,1),
6:(0,0,1),7:(139/255,0,1),8:(1,192/255,203/255),9:(0,0,0)}
def Hdistance_angel():
    # x=[100,80,60,40,20]
    x=[100,90,80,70,60,50,40,30,20,10]
    fig,ax = plt.subplots(figsize=(8,8))
    font = {'family':'Times New Roman','weight':'normal','size':22}
    font1 = {'family':'Times New Roman','weight':'normal','size':12}
    for i in range(1,10):
        pareto=np.loadtxt(par_path_dic[i])
        phy=np.loadtxt(phy_path_dic[i])

        pareto = pareto[pareto[:,5].argsort()] #按照第6列对行排序 ,角度 
        res=[]
        for j in range(0,10):
            helper=pareto[0:int(len(pareto)*(1-j/10))+1]
            Hdist=hausdorff_distance(helper[:,[2,3,4]], phy[:,[2,3,4]], distance="euclidean")
            res.append(Hdist)
        plt.plot(x, res, marker='o', mec=colordic[i], mfc='w', c=colordic[i],label='Test NO'+str(i))
    plt.margins(0)
    plt.legend(prop=font1)
    plt.subplots_adjust(bottom=0.10)
    plt.title('Selected by '+'$\\mathregular{F_{angle}}$(°)',font)
    plt.xlabel('Select rate(%)',font) #X轴标签
    pyplot.xticks([100,90,80,70,60,50,40,30,20,10])

    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.tick_params(labelsize=16)

    plt.ylabel("Hausdorff distance(mm)",font)
    plt.savefig(r'E:\thesis_task\thesis2\3Dircadb_download\res\Hdistance_angel.png',dpi = 300)
    plt.show()


def Hdistance_dist():
    x=[100,90,80,70,60,50,40,30,20,10]
    fig,ax = plt.subplots(figsize=(8,8))
    font = {'family':'Times New Roman','weight':'normal','size':22}
    font1 = {'family':'Times New Roman','weight':'normal','size':12}
    for i in range(1,10):
        pareto=np.loadtxt(par_path_dic[i])
        phy=np.loadtxt(phy_path_dic[i])

        pareto = pareto[pareto[:,6].argsort()] #按照第6列对行排序 ,角度 
        res=[]
        for j in range(0,10):
            helper=pareto[0:int(len(pareto)*(1-j/10))+1]
            Hdist=hausdorff_distance(helper[:,[2,3,4]], phy[:,[2,3,4]], distance="euclidean")
            res.append(Hdist)
        plt.plot(x, res, marker='o', mec=colordic[i], mfc='w', c=colordic[i],label='Test NO'+str(i))
    plt.margins(0)
    plt.legend(prop=font1)
    plt.subplots_adjust(bottom=0.10)
    plt.title('Selected by '+'$\\mathregular{F_{distance}}$(mm)',font)
    plt.xlabel('Select rate(%)',font) #X轴标签
    pyplot.xticks([100,90,80,70,60,50,40,30,20,10])

    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.tick_params(labelsize=16)

    plt.ylabel("Hausdorff distance(mm)",font)
    plt.savefig(r'E:\thesis_task\thesis2\3Dircadb_download\res\Hdistance_dist.png',dpi = 300)
    plt.show()

def Rep_angel():
    x=[100,90,80,70,60,50,40,30,20,10]
    fig,ax = plt.subplots(figsize=(8,8))
    font = {'family':'Times New Roman','weight':'normal','size':22}
    font1 = {'family':'Times New Roman','weight':'normal','size':12}
    for i in range(1,10):
        pareto=np.loadtxt(par_path_dic[i])
        phy=np.loadtxt(phy_path_dic[i])

        pareto = pareto[pareto[:,5].argsort()] #按照第6列对行排序 ,角度 
        res=[]
        for j in range(0,10):
            
                # print('phy',phy[:,[2,3,4]])
                # print(Rep)
            helper=pareto[0:int(len(pareto)*(1-j/10))+1]
            Rep=get_Rep(helper[:,[2,3,4]], phy[:,[2,3,4]])

            res.append(Rep)
        plt.plot(x, res, marker='o', mec=colordic[i], mfc='w', c=colordic[i],label='Test NO'+str(i))
    plt.margins(0)
    plt.legend(prop=font1)
    plt.subplots_adjust(bottom=0.10)
    plt.title('Selected by '+'$\\mathregular{F_{angle}}$(°)',font)
    plt.xlabel('Select rate(%)',font) #X轴标签
    pyplot.xticks([100,90,80,70,60,50,40,30,20,10])

    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.tick_params(labelsize=16)

    plt.ylabel("Overlap rate(%)",font)
    plt.savefig(r'E:\thesis_task\thesis2\3Dircadb_download\res\Rep_angel.png',dpi = 300)
    plt.show()
    

def Rep_dist():
    x=[100,90,80,70,60,50,40,30,20,10]
    fig,ax = plt.subplots(figsize=(8,8))
    font = {'family':'Times New Roman','weight':'normal','size':22}
    font1 = {'family':'Times New Roman','weight':'normal','size':12}
    for i in range(1,10):
        pareto=np.loadtxt(par_path_dic[i])
        phy=np.loadtxt(phy_path_dic[i])

        pareto = pareto[pareto[:,6].argsort()] #按照第6列对行排序 ,角度 
        res=[]
        for j in range(0,10):
            helper=pareto[0:int(len(pareto)*(1-j/10))+1]
            Rep=get_Rep(helper[:,[2,3,4]], phy[:,[2,3,4]])
            res.append(Rep)
        plt.plot(x, res, marker='o', mec=colordic[i], mfc='w', c=colordic[i],label='Test NO'+str(i))
    plt.margins(0)
    plt.legend(prop=font1)
    plt.subplots_adjust(bottom=0.10)
    plt.title('Selected by '+'$\\mathregular{F_{distance}}$(mm)',font)
    plt.xlabel('Select rate(%)',font) #X轴标签
    pyplot.xticks([100,90,80,70,60,50,40,30,20,10])

    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.tick_params(labelsize=16)


    plt.ylabel("Overlap rate(%)",font)
    plt.savefig(r'E:\thesis_task\thesis2\3Dircadb_download\res\Rep_dist.png',dpi = 300)
    plt.show()
    

def get_Rep(pareto,phy):
    thres=10
    repe_pareto=[]
    for ele1 in pareto:
        for ele2 in phy:
            dist=((ele1[0]-ele2[0])**2+(ele1[1]-ele2[1])**2+(ele1[2]-ele2[2])**2)**0.5
            #print(ele1[2:5],ele2,dist)
            if dist<10:
                repe_pareto.append(ele1)
                break
    repe_ratio=len(repe_pareto)/len(pareto)
    return repe_ratio*100

if not os.path.exists(r'E:\thesis_task\thesis2\3Dircadb_download\res'):
    os.makedirs(r'E:\thesis_task\thesis2\3Dircadb_download\res')
# Hdistance_angel()
# Hdistance_dist()
Rep_angel()
Rep_dist()
