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

tar_dic={1:[96.0351693630219, 185.95900976657876, 72.0],
2:[84.68555843830113, 200.8008086681367, 72.0],
3:[218.1780014634133, 143.88800096511844, 169.60000252723694],
4:[110.26200073957446, 173.6040011644364, 169.60000252723694],
5:[93.53200185298925, 169.61400336027157, 94.40000140666962],
6:[193.92299240827552, 132.25399482250208, 139.20000207424164],
7:[213.98399162292472, 127.79599499702448, 139.20000207424164],
8:[108.47799575328823, 127.05299502611155, 160.0000023841858],
9:[95.84699624776836, 148.5999941825866, 160.0000023841858]}


def get_meanphy():
    mean_phy=[]
    for i in range(1,10):
        phy=np.loadtxt(phy_path_dic[i])
        phy=phy[:,[2,3,4]]
        tar=tar_dic[i]
        mean_phy.append(helper(phy,tar))
    print(mean_phy)
    return mean_phy

def helper(phy,tar):
    #输入一个phy数组
    #输出一个平均值
    mylist=[]
    for i in range(len(phy)):
        dist=((phy[i][0]-tar[0])**2+(phy[i][1]-tar[1])**2+(phy[i][2]-tar[2])**2)**0.5
        mylist.append(dist)
    return np.mean(np.array(mylist))


def draw_meandist():
    fig,ax = plt.subplots(figsize=(8,8))
    index=[1,2,3,4,5,6,7,8,9]
    mean_par=[]
    mean_phy=get_meanphy()
    for i in range(1,10):
        pareto=np.loadtxt(par_path_dic[i])
        phy=np.loadtxt(phy_path_dic[i])
        mean=np.mean(pareto[:,6])
        mean_par.append(mean)
        # mean_phy.append(10)

    # 柱子的宽度
    width = 0.45
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色

    plt.bar(index, mean_phy, width, color=(1,0,1))
    plt.bar(index, mean_par, width, color=(0,1,0))
    # 设置横轴标签
    plt.xlabel('Case NO')
    # 设置纵轴标签
    plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)')
    # 添加纵横轴的刻度
    plt.xticks(index)
    plt.show()

def draw_meanangle():
    fig,ax = plt.subplots(figsize=(8,8))
    index=[1,2,3,4,5,6,7,8,9]
    mean_par=[]
    for i in range(1,10):
        pareto=np.loadtxt(par_path_dic[i])
        phy=np.loadtxt(phy_path_dic[i])
        mean=np.mean(pareto[:,5])
        mean_par.append(mean)
        # mean_phy.append(10)

    # 柱子的宽度
    width = 0.45
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色

    plt.bar(index, mean_par, width, color=(0,1,0))
    # 设置横轴标签
    plt.xlabel('Case NO')
    # 设置纵轴标签
    plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)')
    # 添加纵横轴的刻度
    plt.xticks(index)
    plt.show()

# draw_meanangle()
get_meanphy()