"""
# @author chrisxu
# @create 2020-08-25 15:49
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from math import acos

from vtkplotter import Ellipsoid

from objutils.NeedleUtils import NeedleUtils


class ElliVTKAgent(object):
    """
    代理类
    代理生成椭球的vtk
    """

    @classmethod
    def get_vtk(cls, inpt, tar, R, K, color, alpha):
        (zhou, jiao) = cls.get_Rodriguez(inpt, tar)
        actor = Ellipsoid(pos=tar, axis1=[2 * R/K, 0, 0],
                          axis2=[0, 2 * R, 0],
                          axis3=[0, 0, 2 * R/K],
                          c=color,
                          alpha=alpha)
        actor.rotate(jiao, axis=zhou, axis_point=tar, rad=True)
        return actor

    @classmethod
    def get_Rodriguez(cls, P, T):
        """
        # 罗德里格斯公式
        :param P:
        :param T:
        :return:
        """
        newy = cls.get_newy(P, T)
        jiao = acos(newy[1])
        zhou = (newy[2], 0, -newy[0])
        return zhou, jiao

    @classmethod
    def get_newy(cls, P, T):
        """
        # step1:获得旋转矩阵
        # 输入进针单位向量，输出的单位矩阵每一列分别为椭球坐标系的xyz轴
        :param P:
        :param T:
        :return:
        """
        lenth = NeedleUtils.get_dist(P, T)
        alpha = (T[0] - P[0]) / lenth
        beta = (T[1] - P[1]) / lenth
        gama = (T[2] - P[2]) / lenth
        # print(alpha,beta,gama)
        return [alpha, beta, gama]
