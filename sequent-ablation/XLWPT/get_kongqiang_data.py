from vtkplotter import *
from sys import path
import numpy as np
import os
head=r'E:\thesis_task\thesis2\3Dircadb_download\liverdist'
test_index=8
showlist=[]
skin= np.loadtxt(os.path.join(head,'liverdist'+str(test_index)+'.txt'))
# a=Points(skin[:,[0,1,2]],c=colorMap(skin[:,-2], name='hot', vmin=min(skin[:,-2]), vmax=max(skin[:,-2])),r=2, alpha=0.2)
# #showlist.append(a)
# a.addScalarBar(title='Signed\nDistance')
# showlist.append(a)
# # show(showlist)
liverdist_rate_dic={0:3, 1:3, 2:5, 3:4, 4:3, 5:3, 6:3, 7:3, 8:3}
rll_list=skin[:,4]
depth_list=skin[:,3]
index=np.argmin(depth_list)
print(index)
pt_liver=skin[index][5]#最近穿刺点到肝脏点的距离
rll=skin[index][4]#最近穿刺点的空腔比
aver=np.mean(rll_list)
cnt=0
for ele in rll_list:
    if ele>liverdist_rate_dic[test_index]:
        cnt+=1

print(pt_liver,rll,aver,liverdist_rate_dic[test_index],cnt/len(rll_list))