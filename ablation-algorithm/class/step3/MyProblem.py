"""
# @author chrisxu
# @create 2020-08-23 11:20
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

from singleton.LineGetter import LineGetter


class MyProblem(ea.Problem):  # 继承Problem父类
    """
    根据greatpy库
    写的多目标优化类
    该类具有两个优化目标
    进针深度和进针角度
    """
    def __init__(self, auto2Fixed, M=2):
        self.auto2Fixed = auto2Fixed
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        Dim = len(self.auto2Fixed.fixed)  # 初始化Dim（决策变量维数）
        # Dim = 5
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界
        # ub = [10] * Dim  # 决策变量上界
        ub = [len(fixed.feavtk.points()) - 1 for fixed in self.auto2Fixed.fixed]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        punishflag = True if Vars.shape[0] == 1 else  False
        f1 = self.f1(Vars, punishflag)
        f2 = self.f2(Vars, punishflag)

        pop.ObjV = np.hstack([f1, f2])  # 把求得的目标函数值赋值给种群pop的ObjV

    def punish(self, var):
        """
        单个进针方案的惩罚函数
        :param var:
        :return:
        """
        for feaindex, indexinfea in enumerate(var):
            if self.auto2Fixed.fixed[feaindex].feavtk.points()[indexinfea] ==self.auto2Fixed.fixed[feaindex + 1].feavtk.points()[var[feaindex + 1]]:
                return True
        return False

    def f2(self, Vars, punishflag):
        """
        进针角度
        :param Vars:
        :return:
        """
        deltazs = []
        for var in Vars:
            deltazs.append(self.get_mean_deltaz(var, punishflag))
        return np.array(deltazs).reshape((-1, 1))

    def get_mean_deltaz(self, var, punishflag):
        """
        得到单个进针方案的平均deltaz
        :param var:
        :return:
        """
        if punishflag:
            if self.punish(var):
                print("两进针路径进针点重合")
                return 10000
        deltazs = []
        for feaindex, indexinfea in enumerate(var):
            indexinfea = int(indexinfea)
            ztar = self.auto2Fixed.fixed[feaindex].pos[2]
            zpun = self.auto2Fixed.fixed[feaindex].feavtk.points()[indexinfea][2]
            deltazs.append(abs(zpun - ztar))
        return np.mean(np.array(deltazs))

    def get_mean_depth(self, var, punishflag):
        """
        单个个体求解,
        得到单个进针方案的平均进针深度
        :param var:
        :return:
        """
        if punishflag:
            if self.punish(var):
                return 10000
        depths = []
        for feaindex, indexinfea in enumerate(var):
            indexinfea = int(indexinfea)
            feaindexthdepth = LineGetter().get_dist(self.auto2Fixed.fixed[feaindex].pos,
                                                    self.auto2Fixed.fixed[feaindex].feavtk.points()[indexinfea])
            depths.append(feaindexthdepth)
        return np.mean(np.array(depths))

    def f1(self, Vars, punishflag):
        """
        进针深度
        :param Vars:
        :return:
        """
        depths = []
        for var in Vars:
            depths.append(self.get_mean_depth(var, punishflag))
        return np.array(depths).reshape((-1, 1))
