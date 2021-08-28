"""
# @author chrisxu
# @create 2020-08-20 13:07
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import numpy as np
from math import pi

class OmegaAgent(object):
    """
    规划方法2的待消融区域对象的代理类
    用于代理获取体点云的方法
    """

    def __init__(self, omega):
        """
        传入omega对象
        :param omega:
        """

        super().__init__()
        self.omega = omega
        self.ptnum = 5000
        self.r = self.omega.vtk.averageSize() + 15

    def get_bodypts(self):
        """
        代理方法
        为omega初始化体点云
        :return:
        """
        self.omega.boundingpoints = self.get_boundingSphere()
        self.omega.Vbpt = 4 / 3 * pi * self.r ** 3 / 1000
        for pt in self.omega.boundingpoints:
            if self.omega.vtk.isInside(pt):
                self.omega.bodypts.append(pt)

    def get_boundingSphere(self):
        """
        生成原点在肿瘤质心
        点云数量为self.ptnum
        半径为self.omega.averageSize()+20的球体点云
        :return:
        """
        cen = np.array(self.omega.vtk.centerOfMass())
        norm = np.random.normal
        U = norm(size=(3, self.ptnum))  # 随机生成3维空间中的N个坐标点
        dev = np.sqrt(np.sum(U ** 2, axis=0))
        # 对N个坐标点分别随机生成一个半径
        radius = self.r * np.power(np.random.random(size=(1, self.ptnum)), 1 / 3)
        X = np.multiply(radius, U) / dev
        X = X.T
        for ele in X:
            ele += cen
        return X
