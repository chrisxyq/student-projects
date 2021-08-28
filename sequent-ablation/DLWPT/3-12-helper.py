from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import os
head=r'E:\thesis_task\thesis2\3Dircadb_download\3Dircadb1.9\livertumor1_ALLDATA\livertumor1_output_txt\ndl_2\NSGA-II'
def get_Violent_pareto(result):

    a = result[:, [5, 6, 7]]
    pareto = []
    i = 0  # i是被考核的，j是考验的
    while i < len(a):
        # 上一个i打到最后一个，由于此时i新+1，vi很陌生，不确定前i-1个数与vi的强弱关系，因此从第一个数开始考验
        j = 0
        while j < len(a):
            if i != j:
                vj1, vj2, vj3 = a[j][0], a[j][1],a[j][2]
                vi1, vi2, vi3 = a[i][0], a[i][1],a[i][2]
                if (vj1 <= vi1 and vj2 <= vi2 and vj3 <= vi3):
                    i += 1
                    break
                else:
                    j += 1
                if j == len(a):
                    pareto.append(result[i])
                    i += 1
                    break
            else:
                # 上一个i是很快死的，j只要从i+1开始考验即可
                j += 1
                if i == len(a) - 1 and j == len(a):
                    pareto.append(result[i])
                    # 需要i+1来跳出最外层的while i < len(a)
                    i += 1
    
    np.savetxt(os.path.join(head,'tst.txt'), pareto, fmt='%s')    



raw=np.loadtxt(os.path.join(head,'test.txt')) 
get_Violent_pareto(raw)
x=raw[:,5]
y=raw[:,6]
z=raw[:,7]
pareto=np.loadtxt(os.path.join(head,'PARETO_data.txt'))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
a=pareto[:,5]
b=pareto[:,6]
c=pareto[:,7]
ax.scatter(x, y, z, c='r', marker='o')
ax.scatter(a,b,c, c='g', marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
 
plt.show()