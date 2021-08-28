import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import MultipleLocator
import numpy as np
import os
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')

from setpara import *
def plot_gradient():

    pareto = np.loadtxt(os.path.join(otxt_violentpath,'three_goal','ndl_'+str(order)+'violent_pareto.txt')) 
    fullresult= np.loadtxt(os.path.join(otxt_violentpath,'three_goal', 'ndl_'+str(order)+'violent_fullresult.txt')) 

    # get_targetstxt()
    # targetpos=gl.get_value('targetpos')
    
    # verse=gl.get_value('verse')
    # chosen=get_spheretf(gl.get_value('inpts')[:,[0,1,2]])

    xita=fullresult[:,0]
    phi=fullresult[:,1]   
    angle=fullresult[:,5] 
    depth=fullresult[:,6] 

    #risk=1/fullresult[:,7]#这个是1/Frisk，即最近距离
    risk=fullresult[:,7]#这个是Frisk，不好看
    #risk=fullresult[:,7]/1000000#试试Frisk/10，发现即使是Frisk/1000也没用

    #print(np.where(risk==np.max(risk))[0][0])
    """1.四个目标函数着色图"""
    fig=plt.figure(figsize=(8,4))  
    #fig=plt.figure() 
    #fig.add_subplot(1,3,1)
    angle_plt=plt.scatter( phi, xita,c=angle,  s=20, cmap=plt.cm.get_cmap('Oranges_r'))
    plt.scatter(pareto[:,1], pareto[:,0], s=5,c='#00FF00')

    # plt.scatter(np.rint(chosen[:,2]), np.rint(chosen[:,1]), s=5,c='#FF00FF')

    plt.colorbar(angle_plt)

    #设置横纵坐标的名称以及对应字体格式
    # font2 = {'family' : 'Times New Roman',
    # 'weight' : 'normal',
    # 'size'   : 30,
    # }

    ax=plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.yaxis.set_major_locator(MultipleLocator(20))

    plt.ylabel('θ')
    plt.xlabel('φ') 
    plt.title('$\\mathregular{F_{angle}}$(°)')


    # if not os.path.exists(os.path.join(head,'resfig','hardcolorpic',verse)):
    #     os.makedirs(os.path.join(head,'resfig','hardcolorpic',verse))


    # plt.savefig(os.path.join(head, 'resfig','hardcolorpic',verse,verse+'_gdient1.jpg'))
    plt.show()
    

    #fig.add_subplot(1,3,2)
    fig=plt.figure(figsize=(8,4))  
    depth_plt=plt.scatter( phi,xita, c=depth,  s=20, cmap=plt.cm.get_cmap('Oranges_r'))    
    plt.scatter(pareto[:,1], pareto[:,0], s=5,c='#00FF00')

    #plt.scatter(np.rint(chosen[:,2]), np.rint(chosen[:,1]), s=5,c='#FF00FF')

    plt.colorbar(depth_plt)
    plt.ylabel('θ')
    plt.xlabel('φ')
    plt.title('$\\mathregular{F_{depth}}$(mm)')
    # plt.savefig(os.path.join(head, 'resfig','hardcolorpic',verse,verse+'_gdient2.jpg'))
    plt.show()

    #fig.add_subplot(1,3,3)
    fig=plt.figure(figsize=(8,4)) 

    #risk_plt=plt.scatter( phi, xita,c=risk,  s=20, cmap=plt.cm.get_cmap('Oranges'))    
    risk_plt=plt.scatter( phi, xita,c=risk,  s=10, cmap=plt.cm.get_cmap('Oranges_r'))#不好看

    plt.scatter(pareto[:,1], pareto[:,0], s=5,c='#00FF00')

    # plt.scatter(np.rint(chosen[:,2]), np.rint(chosen[:,1]), s=5,c='#FF00FF')

    plt.colorbar(risk_plt)
    plt.ylabel('θ')
    plt.xlabel('φ')

    
    plt.title('$\\mathregular{{F_{risk}}^{-1}}$($\\mathregular{mm}}$)')
    #plt.title('$\\mathregular{F_{risk}}$($\\mathregular{mm^{-1}}$)')
    #plt.title('$\\mathregular{{F_{risk}}/10}$($\\mathregular{mm^{-1}}$)')


    #plt.xlabel('a/$\mathregular{m^2}$',fontdict={'weight': 'normal', 'size': 15})


    # plt.savefig(os.path.join(head, 'resfig','hardcolorpic',verse,verse+'_gdient3.jpg'))
    plt.show()
plot_gradient()