"""
# @author chrisxu
# @create 2020-08-23 18:45
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from singleton.TimeMe import time_me
from step1.Omega import Omega
from vtkplotter import *
import matplotlib.pyplot as plt
import numpy as np


class Auto2FixedEffi(object):
    """
    方法2计算消融效率的代理类
    同时具有切割消融椭球
    以及统计消融距离直方图的功能
    """

    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造Auto2FixedEffi消融效率的代理类")
        return cls.instance

    def __init__(self, auto2Fixed):
        if not Auto2FixedEffi.init_flag:
            super().__init__()
            self.auto2Fixed = auto2Fixed
            Auto2FixedEffi.init_flag = True
            self.dists = []

    @time_me
    def get_effi(self):
        cnt = 0
        omega = Omega()
        boundingpoints = omega.boundingpoints
        allnum = len(boundingpoints)
        allelli = self.get_allelli()
        for bpt in boundingpoints:
            for elli in allelli:
                if elli.isInside(bpt):
                    cnt += 1
                    break
        effi = omega.vtk.volume() / 1000 / (cnt / allnum * omega.Vbpt)
        print("omega的体积为", round(omega.vtk.volume() / 1000, 2), "ml")
        print("omega的包围球体积为", round(omega.Vbpt, 2), "ml")
        print("cnt为", cnt, "allnum为", allnum)
        print("消融效率为", round(effi * 100, 2), "%")

    def get_allelli(self):
        """
        获取代理auto2Fixed的所有椭球
        :return:
        """
        allelli = []
        for fixed in self.auto2Fixed.fixed:
            allelli.extend(fixed.elli)
        return allelli

    def cut_elli(self):
        """
        通过切割vtk
        获取不重叠的椭球vtk
        :return:
        """
        allelli = self.get_allelli()
        indexdic = {}

        def get_index(elli, others):
            """
            获取s1在其他椭球内部的索引
            :param s1:
            :param s2:
            :return:
            """
            index = []
            for other in others:
                """要重新读取，distanceToMesh距离才不为空"""
                elli.write("elli.vtk")
                elli = load("elli.vtk")

                elli.distanceToMesh(other, signed=True, negate=False)
                dists = elli.getPointArray("Distance")
                for i in range(len(dists)):
                    if dists[i] < -3:
                        index.append(i)
            return list(set(index))

        for index, elli in enumerate(allelli):
            indexdic[index] = get_index(elli, [ele for ele in allelli if ele != elli])
        for index, elli in enumerate(allelli):
            elli.deletePoints(indexdic[index], renamePoints=True)
            """要重新读取，distanceToMesh距离才不为空"""
            elli.write("elli.vtk")
            elli = load("elli.vtk")
            elli.distanceToMesh(Omega().vtk, signed=True, negate=True)
            elli.addScalarBar(title='')
            subdists = elli.getPointArray("Distance")
            self.dists.extend(subdists)
        self.dists = [ele for ele in self.dists if ele > 0]

    def show_histogram(self):
        """
        显示消融距离的直方统计图
        :return:
        """
        bins = np.linspace(min(self.dists), max(self.dists), 10)
        plt.figure(figsize=(7, 7))
        plt.hist(self.dists, bins, density=1, edgecolor='black', linewidth=1)

        # 设置坐标刻度值的大小以及刻度值的字体
        plt.rcParams['font.sans-serif'] = ['SimSun']
        plt.rcParams['axes.unicode_minus'] = False
        plt.tick_params(labelsize=15)
        ax = plt.gca()
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]

        plt.xlabel(u'消融边界距离(mm)', size=20)
        plt.ylabel(u'频率', size=20)
        print('平均消融距离', round(np.mean(self.dists), 1), 'mm')
        res = np.percentile(self.dists, (25, 75), interpolation='midpoint')
        print('第一第三分位数', res, 'mm')
        plt.show()
