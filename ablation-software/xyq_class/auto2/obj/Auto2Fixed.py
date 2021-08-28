"""
# @author chrisxu
# @create 2020-08-19 22:00
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from collections import defaultdict
import src.GlobalVar as gl
from vtkplotter import show, Point, Line, Points

from auto2.ObjToString import obj_to_string
from auto2.baseobj.Fixed import Fixed
from auto2.objagent.FixedMover import FixedMover
from auto2.objagent.FixedRegister import FixedRegister


class Auto2Fixed(object):
    """
    方法2得到的所有的固定点的类
    """

    def __init__(self):
        super().__init__()
        self.fixed = []

    def get_fixed(self):
        """
        根据聚类结果
        为病例求解所有的固定点
        :return:
        """
        md = gl.get_value('md')
        fixedindex = 0
        while len(md.centroidsRes.centroids) > 0:
            cen1 = md.centroidsRes.centroids[0]
            if len(md.centroidsRes.centroids) == 1:
                self.fixed.append(Fixed.by_onecen(cen1, fixedindex))
                md.centroidsRes.centroids.remove(cen1)
                fixedindex += 1
                # print("==添加一个非推拉固定点==")
                # print("当前剩余聚类中心", md.centroidsRes)
            else:
                for index in range(1, len(md.centroidsRes.centroids)):
                    cen2 = md.centroidsRes.centroids[index]
                    tempfixed = Fixed.by_twocen(cen1, cen2, fixedindex)
                    tempfixed.check_validity()  # 推拉固定点有效性校验
                    # 找到匹配的固定点，将两个聚类中心构造推拉固定点
                    if tempfixed.isvalid:
                        self.fixed.append(tempfixed)
                        md.centroidsRes.centroids.remove(cen1)
                        md.centroidsRes.centroids.remove(cen2)
                        fixedindex += 1
                        # print("==添加一个推拉固定点==")
                        # print("当前固定点", self)
                        # print("当前剩余聚类中心", md.centroidsRes)
                        break
                    # 遍历结束，找不到可匹配的固定点，将该聚类中心构造非推拉固定点
                    elif index == len(md.centroidsRes.centroids) - 1:
                        self.fixed.append(Fixed.by_onecen(cen1, fixedindex))
                        md.centroidsRes.centroids.remove(cen1)
                        fixedindex += 1
                        # print("==添加一个非推拉固定点==")
                        # print("当前固定点", self)
                        # print("当前剩余聚类中心", md.centroidsRes)
        print("====step4:根据聚类结果求解固定点完成====")
        # print("固定点求解结果", self)
        # print("聚类结果", md.centroidsRes)

    def regist(self):
        """
        显示fixed的进针路径、消融椭球
        :return:
        """
        for fixed in self.fixed:
            fixedRegister = FixedRegister(fixed)
            fixedRegister.regist()

    def show_fea(self):
        """
        显示fixed的可行域
        :return:
        """
        for index, fixed in enumerate(self.fixed):
            fixed.show_fea()

    def remove_fea(self):
        """
        移除fixed的可行域
        :return:
        """
        for fixed in self.fixed:
            fixed.remove_fea()

    def show_subomega(self):
        """
        显示fixed的进针路径、消融椭球
        :return:
        """
        for index, fixed in enumerate(self.fixed):
            fixed.show_subomega()

    def remove_subomega(self):
        """
        移除fixed的聚类子点云
        :return:
        """
        for fixed in self.fixed:
            fixed.remove_subomega()

    def __str__(self):
        return obj_to_string(Auto2Fixed, self)

    def get_feasibles(self):
        """
        为所有的固定点对象求取可行域
        :return:
        """
        for fixed in self.fixed:
            fixed.get_feasible()

    def check_and_move(self):
        """
        经验表明，只需移动推拉式固定点
        :return:
        """
        for fixed in self.fixed:
            if fixed.ispush:
                self.move(fixed)
        print("====step5:初步调整固定点完成====")

    def move(self, fixed):
        """
        对于检验不合格的固定点
        self.covervalid=False
        进行移动
        :param fixed:
        :return:
        """
        FixedMover(self).move(fixed)
