"""
# @author chrisxu
# @create 2020-08-20 16:15
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from singleton.Auto2Para import Auto2Para
from math import acos
from vtkplotter import *


class ElliGetter(object):
    """
    生成消融椭球的vtk的工具类
    多次被调用
    单例
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            #print("构造ElliGetter椭球生成工具")
        return cls.instance

    def __init__(self):
        if not ElliGetter.init_flag:
            #print("初始化ElliGetter椭球生成工具")
            super().__init__()
            self.c = (152, 251, 152)
            self.alpha = 0.7
            ElliGetter.init_flag = True

    def get_elli_vtk(self, P, T, r):
        """
        # 苍白绿
        # 产生elli_actor
        :param P:
        :param T:
        :param r:
        :return:
        """
        k = Auto2Para().K
        (zhou, jiao) = self.get_Rodriguez(P, T)
        elli_actor = Ellipsoid(pos=T,
                               axis1=[2 * r / k, 0, 0],
                               axis2=[0, 2 * r, 0],
                               axis3=[0, 0, 2 * r / k],
                               c=self.c,
                               alpha=self.alpha)
        elli_actor.rotate(jiao, axis=zhou, axis_point=T, rad=True)
        return elli_actor

    def get_Rodriguez(self, P, T):
        """
        # 罗德里格斯公式
        :param P:
        :param T:
        :return:
        """
        newy = self.get_newy(P, T)
        jiao = acos(newy[1])
        zhou = (newy[2], 0, -newy[0])
        return zhou, jiao

    def get_newy(self, P, T):
        """
        # step1:获得旋转矩阵
        # 输入进针单位向量，输出的单位矩阵每一列分别为椭球坐标系的xyz轴
        :param P:
        :param T:
        :return:
        """
        lenth = self.get_dist(P, T)
        # lenth = ((T[0] - P[0]) ** 2 + (T[1] - P[1]) ** 2 + (T[2] - P[2]) ** 2) ** 0.5
        alpha = (T[0] - P[0]) / lenth
        beta = (T[1] - P[1]) / lenth
        gama = (T[2] - P[2]) / lenth
        # print(alpha,beta,gama)
        return [alpha, beta, gama]

    def get_dist(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5
