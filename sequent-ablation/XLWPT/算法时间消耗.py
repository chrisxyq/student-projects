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

def draw_meandist():
    fig,ax = plt.subplots(figsize=(8,8))
    font = {'family':'Times New Roman','weight':'normal','size':14}
    font1 = {'family':'Times New Roman','weight':'normal','size':20}
    index=['Obstacle'+'\n'+'constraint','Tangent'+'\n'+'angle'+'\n'+'constraint','Round2',
    'Liver'+'\n'+'length'+'\n'+'ratio'+'\n'+'constraint','Optimization']
    timegood=[2.58,0.61,3.91,0.43,4.25]
    timebad=[13.73,2.62,18.15,1.57,8.28]



    # 柱子的宽度
    width = 0.7
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色

    #plt.barh(index, mean_phy, width, color=(1,0,1))
    rects=plt.bar(index, timebad, width, color=(220/255,20/255,60/255))
    for rect in rects:  #rects 是三根柱子的集合
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), size=15, ha='center', va='bottom',fontsize=14,fontname='Times New Roman')

    rects=plt.bar(index, timegood, width, color=(60/255,179/255,112/255))
    for rect in rects:  #rects 是三根柱子的集合
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height),  ha='center', va='bottom',fontsize=14,fontname='Times New Roman')

    plt.ylabel('Mean time(s)',font1)
    plt.xticks(index)
    plt.xticks(fontsize=14,fontname='Times New Roman')
    plt.yticks(fontsize=14,fontname='Times New Roman')
    plt.savefig(r'E:\thesis_task\thesis2\3Dircadb_download\res\time.png',dpi = 300)
    plt.show()

draw_meandist()