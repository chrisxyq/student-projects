
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\tools')
from tf_tools import *
from hausdorff import hausdorff_distance
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import MultipleLocator
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\soft')
from myaim import *
from PIL import Image, ImageDraw

def get_real_inpts():
    #输入皮肤进针点的笛卡尔坐标
    #输出在皮肤真正的角度组合和CT上的xy
    pixel_info= gl.get_value('pixel_info')
    inpts = gl.get_value('inpts')
    skin_dic=gl.get_value('skin_dic')
    checker=Image.open(os.path.join(opic_ndlpath, 'round2.png')) if order==1 else Image.open(os.path.join(opic_ndlpath, 'round3.png'))
    
    
    phy = []
    for ele in inpts:
        sph=get_spheretf(ele)
        helper=[int(sph[1]),int(sph[2])]
        if checker.getpixel((int(sph[1]),int(sph[2])))==(255,255,255):
        #if str(helper) in skin_dic:
            phy.append([helper[0],helper[1],skin_dic[str(helper)][1][0],skin_dic[str(helper)][1][1],skin_dic[str(helper)][1][2]])
        else:
            print('不行',ele)
    np.savetxt(os.path.join(otxt_hardpath,'phy'+str(order)+'.txt'), phy, fmt='%s') 
    print('已保存')
    gl.set_value('phy',np.array(phy))
    return np.array(phy)

def get_Hdist_and_Rep(pareto):
    """
    功能：
    1.计算Hausdorff distance
    2.画Axes3D图：pareto和医生标记点的三维坐标点对比   
    """
    phy=get_real_inpts()
    inpts=np.array([ele[2:5] for ele in phy])
    Hdist=hausdorff_distance(pareto[:,[2,3,4]], inpts, distance="euclidean")
    #print('帕累托点个数为',len(pareto),'最大层数差为',max(pareto[:,5]),str(goalnum)+"个目标的Hausdorff distance = {0}".format( Hdist ))
    print('帕累托点个数为',len(pareto),'最大层数差为',max(pareto[:,5]),"Hdistance = {0}".format( Hdist ))
    
    #==========
    thres=10
    repe_pareto=[]
    for ele1 in pareto:
        for ele2 in inpts:
            dist=((ele1[2]-ele2[0])**2+(ele1[3]-ele2[1])**2+(ele1[4]-ele2[2])**2)**0.5
            #print(ele1[2:5],ele2,dist)
            if dist<10:
                repe_pareto.append(ele1)
                break
    repe_ratio=len(repe_pareto)/len(pareto)
    print('帕累托点数=',len(pareto),'在医生标记范围内的帕累托点数=',len(repe_pareto),'重复率=',repe_ratio)



    


def mark_phyandpar_2D():
    """功能：在可行域图上标'医生标记点'"""
    pareto=gl.get_value('NSGApareto') if method==0 else gl.get_value('Violent_pareto')
    chosen=gl.get_value('phy')
    path=os.path.join(opic_ndlpath, 'Final_denoise.png') 
    img = cv2.imread(path)
    # gray = np.array(cv2.cvtColor( img, cv2.COLOR_BGR2GRAY))

    composite()
    path2=os.path.join(opic_ndlpath, 'composite.png') 
    img2 = cv2.imread(path2)


    
    for i in range(len(pareto)):
        cv2.circle(img,(int(pareto[i][0]),int(pareto[i][1])), 1,RGB_pareto, -1)
        cv2.circle(img2,(int(pareto[i][0]),int(pareto[i][1])), 1,RGB_pareto, -1)
    for sph in chosen:       
        cv2.circle(img,(int(sph[0]),int(sph[1])), 1, RGB_doctor)# BGR蓝色，+10 -10意思是向着右上
        cv2.circle(img2,(int(sph[0]),int(sph[1])), 1, RGB_doctor)# BGR蓝色，+10 -10意思是向着右上
    if method==0:
        cv2.imwrite(os.path.join(opic_ndlpath, 'NSGA_Final_denoise.png'), img)
        cv2.imwrite(os.path.join(opic_ndlpath, 'NSGA_composite.png'), img2)
    if method==1:
        if goalnum==3:
            cv2.imwrite(os.path.join(opic_ndlpath, 'Violent3_Final_denoise.png'), img)
            cv2.imwrite(os.path.join(opic_ndlpath, 'Violent3_composite.png'), img2)
        if goalnum==2:
            cv2.imwrite(os.path.join(opic_ndlpath, 'Violent2_Final_denoise.png'), img)
            cv2.imwrite(os.path.join(opic_ndlpath, 'Violent2_composite.png'), img2)

    print("可行域上医生标记点和帕累托点画好了")


def NewQuan_analysis():

    if (method==1 and goalnum==2):
        if method==1:
            pareto=np.loadtxt(os.path.join(otxt_violentpath,'two_goal','ndl_'+str(order)+'violent_pareto.txt'))
        else:
            pareto=np.loadtxt(os.path.join(otxt_NSGApath,'ndl_'+str(order)+'NSGA_pareto.txt'))
        phyres=gl.get_value('phyres')

        fig = plt.figure(figsize=(8,8))
        ax = Axes3D(fig)


        font1 = {'family':'Times New Roman','weight':'normal','size':16}
        font2 = {'family':'Times New Roman','weight':'normal','size':22}
        #深度风险角度xyz
        A=ax.scatter(pareto[:,6], pareto[:,7],pareto[:,5],s=90,c='#00FF00')#帕累托

        B=ax.scatter(phyres[:,5], phyres[:,6],np.zeros(len(phyres)),color='white', marker='o', edgecolors='#FF00FF', s=90)#医生
        #legend = plt.legend(handles=[A,B],prop=font1)

        
        ax.set_xlabel('$\\mathregular{F_{distance}}$(mm)',font1)
        ax.set_ylabel('$\\mathregular{{F_{risk}}}$($\\mathregular{mm}^{-1}}$)',font1)
        ax.set_zlabel('$\\mathregular{F_{angle}}$(mm)',font1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.grid(False)
        ax.xaxis.pane.set_edgecolor("w")
        ax.yaxis.pane.set_edgecolor("w")
        ax.zaxis.pane.set_edgecolor("w")
        ax.xaxis.pane.fill=False
        ax.yaxis.pane.fill=False
        ax.zaxis.pane.fill=False
        ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        plt.tick_params(labelsize=12)

        labels = ax.get_xticklabels() + ax.get_yticklabels()+ ax.get_zticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        plt.title(verse,font2) 
        plt.savefig(os.path.join(opic_ndlpath, 'Quan_analysis.png'))
        plt.show()



def Quan_analysis():

    if (method==1 and goalnum==2) or method==0:
        if method==1:
            pareto=np.loadtxt(os.path.join(otxt_violentpath,'two_goal','ndl_'+str(order)+'violent_pareto.txt'))
        else:
            pareto=np.loadtxt(os.path.join(otxt_NSGApath,'ndl_'+str(order)+'NSGA_pareto.txt'))
        phyres=gl.get_value('phyres')
        

        figsize = 10,10
        fig, ax = plt.subplots(figsize=figsize)
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        font1 = {'family':'Times New Roman','weight':'normal','size':20}
        A=plt.scatter(pareto[:,6], pareto[:,7],s=60,c='#00FF00')#帕累托

        B=plt.scatter(phyres[:,5], phyres[:,6],color='', marker='o', edgecolors='#FF00FF', s=60)#医生
        #legend = plt.legend(handles=[A,B],prop=font1)

        
        plt.xlabel('$\\mathregular{F_{depth}}$(mm)',font1)
        plt.ylabel('$\\mathregular{{F_{risk}}}$($\\mathregular{mm}^{-1}}$)',font1)

        plt.tick_params(labelsize=20)

        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        plt.title(verse,font1) 
        plt.savefig(os.path.join(opic_ndlpath, 'Quan_analysis.png'))
        plt.show()

    
def composite():
    bg = Image.open(os.path.join(head,"bg.png"))
    H1=Image.open(os.path.join(opic_ndlpath, 'H1_back.png'))
    H2=Image.open(os.path.join(opic_ndlpath, 'H2_back.png'))
    H3=Image.open(os.path.join(opic_ndlpath, 'H3_back.png'))
    H4=Image.open(os.path.join(opic_ndlpath, 'H4.png'))
    H5=Image.open(os.path.join(opic_ndlpath, 'H5_back.png'))
    H6=Image.open(os.path.join(opic_ndlpath, 'H6_back.png'))
    
    F=Image.open(os.path.join(opic_ndlpath, 'round2.png')) if order==1 else Image.open(os.path.join(opic_ndlpath, 'round3.png'))
    for x in range(181):
        for y in range(361):
            if H3.getpixel((x,y))!=(0,0,0):
                bg.putpixel([x,y],color_dic[3])
                #break
            elif H1.getpixel((x,y))!=(0,0,0):
                bg.putpixel([x,y],color_dic[1])
                #break
            elif H2.getpixel((x,y))!=(0,0,0):
                bg.putpixel([x,y],color_dic[2])
                #break
            elif H4.getpixel((x,y))!=(0,0,0):
                bg.putpixel([x,y],color_dic[4])
                #break
            elif H5.getpixel((x,y))!=(0,0,0):
                bg.putpixel([x,y],color_dic[5])
                #break
            elif H6.getpixel((x,y))!=(0,0,0):
                bg.putpixel([x,y],color_dic[6])
            elif F.getpixel((x,y))!=(0,0,0):
                bg.putpixel([x,y],RGB_feasible)
                #break
    if order==2:
        H7=Image.open(os.path.join(opic_ndlpath, 'H7_back.png'))
        for x in range(181):
            for y in range(361):
                if H7.getpixel((x,y))!=(0,0,0):
                    bg.putpixel([x,y],color_dic[7])
    bg.save(os.path.join(opic_ndlpath, 'composite.png'))

