# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt



# df = pd.DataFrame(data[1])
# fig,axes = plt.subplots(331)
# df.boxplot(vert=True,sym='r*',return_type='dict',patch_artist=True,meanline=False,showmeans=False)
# df = pd.DataFrame(data[2])
# fig,axes = plt.subplots(332)
# df.boxplot(vert=True,sym='r*',return_type='dict',patch_artist=True,meanline=False,showmeans=False)
# df = pd.DataFrame(data[3])
# fig,axes = plt.subplots(333)
# df.boxplot(vert=True,sym='r*',return_type='dict',patch_artist=True,meanline=False,showmeans=False)
# df = pd.DataFrame(data[4])
# fig,axes = plt.subplots(334)
# df.boxplot(vert=True,sym='r*',return_type='dict',patch_artist=True,meanline=False,showmeans=False)
# # tips.plot(kind='box',ax=axes,subplots=True,
# #                               title='Different boxplots',color=color,sym='r+')
# # # sym参数表示异常值标记的方式

# # axes.set_ylabel('values of total_bill')
# # axes.set_ylabel('values of tip')


# fig.subplots_adjust(wspace=1,hspace=1)  # 调整子图之间的间距
# # fig.savefig('p2.png')    # 将绘制的图片保存为p2.png
# plt.show()






import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from matplotlib import pyplot
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
font = {'family':'Times New Roman','weight':'normal','size':12}
font1 = {'family':'Times New Roman','weight':'normal','size':20}
data={}
for i in range(1,10):
    helper=np.loadtxt(par_path_dic[i])[:,6]
    data[i]=pd.Series(helper)

box_1, box_2, box_3= data[1], data[2], data[3]
box_4, box_5, box_6= data[4], data[5], data[6]
box_7, box_8, box_9= data[7], data[8], data[9]
fig,ax = plt.subplots(figsize=(12,6))
plt.subplot(191)
plt.boxplot([box_1],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},widths=0.7)
# plt.xlabel("Case NO1",fontsize=12)
plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',font1)
pyplot.yticks([48,59,70,81])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')

plt.subplot(192)
plt.boxplot([box_2],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='2',widths=0.7)
# plt.xlabel("Case NO2",fontsize=12)
pyplot.yticks([47,48,49,50])
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')
# labels = ax.get_xticklabels() + ax.get_yticklabels()
# [label.set_fontname('Times New Roman') for label in labels]
# plt.tick_params(labelsize=16)

plt.subplot(193)
plt.boxplot([box_3],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='3',widths=0.7)
# plt.xlabel("Case NO3",fontsize=12)
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
pyplot.yticks([73,77,81,85])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')

plt.subplot(194)
plt.boxplot([box_4],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='4',widths=0.7)
# plt.xlabel("Case NO4",fontsize=12)
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
pyplot.yticks([66,67,68,69])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')

plt.subplot(195)
plt.boxplot([box_5],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='5',widths=0.7)
# plt.xlabel("Case NO5",fontsize=12)
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
pyplot.yticks([88,90,92,94])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')
plt.xlabel('Case NO',font1)

plt.subplot(196)
plt.boxplot([box_6],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='6',widths=0.7)
# plt.xlabel("Case NO6",fontsize=12)
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
pyplot.yticks([98,100,102,104])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')

plt.subplot(197)
plt.boxplot([box_7],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='7',widths=0.7)
# plt.xlabel("Case NO7",fontsize=12)
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
pyplot.yticks([92,97,102,107])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')

plt.subplot(198)
plt.boxplot([box_8],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='8',widths=0.7)
# plt.xlabel("Case NO8",fontsize=12)
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
pyplot.yticks([52,58,64,70])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')

plt.subplot(199)
plt.boxplot([box_9],notch=False,patch_artist = False, boxprops = {'color':'black','linewidth':'2.0'},
capprops={'color':'black','linewidth':'2.0'},labels='9',widths=0.7)
# plt.xlabel("Case NO9",fontsize=12)
# plt.ylabel('Mean '+'$\\mathregular{F_{distance}}$(mm)',fontsize=12)
pyplot.yticks([49,51,53,55])
# pyplot.yticks([48,51,54,57])
plt.xticks(fontsize=12,fontname='Times New Roman')
plt.yticks(fontsize=12,fontname='Times New Roman')
plt.subplots_adjust(wspace=1,hspace=0)  # 调整子图之间的间距
#plt.margins(0)
#plt.savefig(r'E:\thesis_task\thesis2\3Dircadb_download\res\BOX.png',dpi = 300)
plt.show()
