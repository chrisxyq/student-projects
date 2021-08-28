import numpy as np
import math
import matplotlib.pyplot as plt
def GrahamScan(S):
    """
    GrahamScan求凸包
    :param S:
    :return:
    """
    #预处理：找到S中y坐标最小的点P0，以水平为极轴求得每个点极角
    n = len(S)
    P = []

    S = S[np.argsort(S[:, 1])]
    #P.append(tuple(S[0]))
    P.append(list(S[0, 0:2]))
    PointPolar = []  # 保存(x,y,极角)
    for i in range(1, n):
        polar = math.atan2(S[i][1] - S[0][1], S[i][0] - S[0][0])
        polar = polar / math.pi * 180
        PointPolar.append([S[i][0], S[i][1], polar])
    # 将PointPolar的点按照极角从小到大排序，保存在result
    result = preProcessing(PointPolar)

    new_dict2 = remove_dup(result, P[0])
    #P.extend(new_dict2.keys())
    for key in new_dict2:
        P.append(list(key))
    #若m<=1返回凸包是空
    m=len(P)
    if m<=2:
        return
    # 将P[0],P[1],P[2]依次压栈Q
    stack = []
    stack.append(P[0])
    stack.append(P[1])
    stack.append(P[2])
    for i in range(3, m):
        while isInTriangle(P[0], P[i], stack[-2], stack[-1]):
            stack.pop()
        stack.append(P[i])
    return stack
def preProcessing(PointPolar):
    """
    当多个点的极角相同时，保留距离原点最远的点
    :param dict:
    :return:一个list,经预处理的P[0:m]，按照极角从小到大保存要处理的点集
    """
    sorted_polar=sorted(PointPolar,key=lambda d:d[2])
    return sorted_polar


def remove_dup(sorted_polar,raw):
    """
    :param sorted_dict:
    :return:
    """
    sorted_dict = {}
    for d in sorted_polar:
        sorted_dict[(d[0], d[1])] = d[2]
    new_dict = {}
    new_dict2 = {}
    for k, v in sorted_dict.items():
        new_dict.setdefault(v, []).append(k)
    for k, v in new_dict.items():
        if len(v) > 1:
            d = []
            for item in v:
                d.append((item[0]-raw[0]) * (item[0]-raw[0]) + (item[1]-raw[1]) * (item[1]-raw[1]))
            v = v[np.argmax(d)]
            new_dict2[v] = k
        else:
            new_dict2[v[0]] = k
    return new_dict2
def g(A,B,P):
    """
    判断点PA矢量在AB矢量的顺时针还是逆时针方向，
    若在逆时针方向则返回1，同向返回0，在顺时针方向返回-1
    :param A:
    :param B:
    :param P:
    :return: 1或0或-1
    """
    #使用PxQ=XpYq-XqYp,若大于0则表示Q在P的逆时针方向
    result = (P[1]-A[1])*(B[0]-A[0])-(B[1]-A[1])*(P[0]-A[0])
    if result<0:
        return -1
    elif result==0:
        return 0
    else:
        return 1
def isInTriangle(Pi,Pj,Pk,P):
    """
    判断点P是否在其他三个点组成的三角形中，是的话返回true
    :param P:
    :param Pi:
    :param Pj:
    :param Pk:
    :return:
    """
    if g(Pi,Pj,Pk)==0:
        return 0
    if g(Pi,Pj,P)*g(Pi,Pj,Pk)>=0 and g(Pj,Pk,P)*g(Pj,Pk,Pi)>=0 and g(Pk,Pi,P)*g(Pk,Pi,Pj)>=0:
        return 1
    return 0
# points = [[1.1, 3.6],
#                    [2.1, 5.4],
#                    [2.5, 1.8],
#                    [3.3, 3.98],
#                    [4.8, 6.2],
#                    [4.3, 4.1],
#                    [4.2, 2.4],
#                    [5.9, 3.5],
#                    [6.2, 5.3],
#                    [6.1, 2.56],
#                    [7.4, 3.7],
#                    [7.1, 4.3],
#                    [7, 4.1]]
# a=GrahamScan(np.array(points))
# print(a)

def test1():
    points = [[1.1, 3.6],
                       [2.1, 5.4],
                       [2.5, 1.8],
                       [3.3, 3.98],
                       [4.8, 6.2],
                       [4.3, 4.1],
                       [4.2, 2.4],
                       [5.9, 3.5],
                       [6.2, 5.3],
                       [6.1, 2.56],
                       [7.4, 3.7],
                       [7.1, 4.3],
                       [7, 4.1]]
 
    for point in points:
        plt.scatter(point[0], point[1], marker='o', c='y')
 
    result = GrahamScan(np.array(points))
 
    length = len(result)
    for i in range(0, length-1):
        plt.plot([result[i][0], result[i+1][0]], [result[i][1], result[i+1][1]], c='r')
    plt.plot([result[0][0], result[length-1][0]], [result[0][1], result[length-1][1]], c='r')
 
    plt.show()

# test1()