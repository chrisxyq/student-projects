"""
# @author chrisxu
# @create 2020-08-20 23:23
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from singleton.Auto2BaseVtk import Auto2BaseVtk
from singleton.Auto2Para import Auto2Para
from math import degrees, atan, acos

from singleton.ElliGetter import ElliGetter
from singleton.LineGetter import LineGetter
from singleton.TimeMe import time_me
from step1agent.FcomAgent import FcomAgent
from step2.OmegaCore import OmegaCore
import numpy as np


class FixedFeaAgent(FcomAgent):
    """
    step6:固定点可行域求解
    规划方法2的求解可行域的代理类
    继承求解可行域的代理类
    该代理类虽然是单例
    但是可以根据传入的fixed对象初始化多次
    """

    def __init__(self, fixed, omegaCore):

        # print("初始化FixedFeaAgent可行域求解的代理类")
        super().__init__()
        self.fixed = fixed
        self.omegaCore = omegaCore
        self.feasibler = 50
        # self.threshold = 0.93

    def get_del(self):
        """
        重写父类的方法
        求解约束
        获取不符合分区约束、避障约束、空腔约束、完全消融约束的del_index
        :return:
        """
        if Auto2Para.isBig_dic[Auto2Para().index]==1:
            # print("子类方法")
            skinpts = Auto2BaseVtk().skin.points()
            target = self.fixed.pos
            del_index = []
            cnt1, cnt2, cnt3, cnt4 = 0, 0, 0, 0

            for index, skinpt in enumerate(skinpts):
                if LineGetter().get_dist(skinpt, self.fixed.skinintersect) > self.feasibler:
                    cnt1 += 1
                    del_index.append(index)
                # 避障约束
                elif self.bool_safe(skinpt, target) == 1:
                    cnt2 += 1
                    del_index.append(index)
                # 空腔约束
                elif self.bool_cavity(skinpt, target) == 1:
                    cnt3 += 1
                    del_index.append(index)
                # 完全消融约束(只有推拉进针才需要计算
                # elif self.fixed.ispush and self.bool_coverage(skinpt) == 1:
                #     cnt4 += 1
                #     del_index.append(index)

            print("角度约束排除点数", cnt1)
            print("避障约束排除点数", cnt2)
            print("空腔约束排除点数", cnt3)
            #print("完全消融排除点数", cnt4)
            # return np.array(del_index).astype('int64')
            return del_index
        else:
            return FcomAgent().get_del()

    # def bool_coverage(self, skinpt):
    #     """
    #     传入皮肤点，
    #     判断与self.fixed.pos连线
    #     实时计算形成的椭球是否满足完全消融约束
    #     如果代理的是非推拉式的固定点，直接计算椭球即可
    #     如果代理的是推拉式的固定点，还需要实现计算好核心靶点区域
    #     :param skinpt:
    #     :return:不满足覆盖条件，则返回1
    #     """
    #     if self.fixed.ispush:
    #         return self.bool_coverage_for_push(skinpt)
    #     else:
    #         return self.bool_coverage_for_unpush(skinpt)
    #
    # def bool_coverage_for_push(self, skinpt):
    #     tar1, tar2 = self.get_tars_for_push(skinpt)
    #     elli1 = ElliGetter().get_elli_vtk(skinpt, tar1, Auto2Para().MAXABR)
    #     elli2 = ElliGetter().get_elli_vtk(skinpt, tar2, Auto2Para().MAXABR)
    #     allnum, coverednum = len(self.fixed.subomega), 0
    #     for omegapt in self.fixed.subomega:
    #         if elli1.isInside(omegapt) or elli2.isInside(omegapt):
    #             coverednum += 1
    #     return 1 if coverednum / allnum < self.threshold else 0
    #
    # def bool_coverage_for_unpush(self, skinpt):
    #     elli = ElliGetter().get_elli_vtk(skinpt, self.fixed.pos, Auto2Para().MAXABR)
    #     allnum, coverednum = len(self.fixed.subomega), 0
    #     for omegapt in self.fixed.subomega:
    #         if elli.isInside(omegapt):
    #             coverednum += 1
    #     return 1 if coverednum / allnum < self.threshold else 0
    #
    # def get_tars_for_push(self, skinpt):
    #     """
    #     为推拉式固定点求解两个靶点
    #     :return:
    #     """
    #     extension = 2 * np.array(self.fixed.pos) - np.array(skinpt)
    #     # tars = OmegaCore().vtk.intersectWithLine(skinpt, extension)
    #     tars = self.omegaCore.vtk.intersectWithLine(skinpt, extension)
    #     # print("迭代进针路径与核心靶点区域交点为",tars)
    #     return tars[0], tars[-1]
