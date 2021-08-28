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

from vtkplotter import show, Point, Line, Points

from singleton.ObjToString import obj_to_string
from singleton.TimeMe import time_me
from step1.CentroidsRes import CentroidsRes
from step2agent.FixedMover import FixedMover

from step2base.Fixed import Fixed
from step3agent.Auto2FixedEffi import Auto2FixedEffi


class Auto2Fixed(object):
    """
    方法2得到的所有的固定点的类
    """

    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造Auto2Fixed固定点的类")
        return cls.instance

    def __init__(self):
        if not Auto2Fixed.init_flag:
            super().__init__()
            self.fixed = []
            Auto2Fixed.init_flag = True

    @time_me
    def get_fixed(self):
        """
        根据聚类结果
        为病例求解所有的固定点
        :return:
        """
        centroidsRes = CentroidsRes()
        while len(centroidsRes.centroids) > 0:
            cen1 = centroidsRes.centroids[0]
            if len(centroidsRes.centroids) == 1:
                self.fixed.append(Fixed.by_onecen(cen1))
                centroidsRes.centroids.remove(cen1)
                print("==添加一个非推拉固定点==")
                print("当前固定点", self)
                print("当前剩余聚类中心", centroidsRes)
            else:
                for index in range(1, len(centroidsRes.centroids)):
                    cen2 = centroidsRes.centroids[index]
                    tempfixed = Fixed.by_twocen(cen1, cen2)
                    tempfixed.check_validity()  # 推拉固定点有效性校验
                    # 找到匹配的固定点，将两个聚类中心构造推拉固定点
                    if tempfixed.isvalid:
                        self.fixed.append(tempfixed)
                        centroidsRes.centroids.remove(cen1)
                        centroidsRes.centroids.remove(cen2)
                        print("==添加一个推拉固定点==")
                        print("当前固定点", self)
                        print("当前剩余聚类中心", centroidsRes)
                        break
                    # 遍历结束，找不到可匹配的固定点，将该聚类中心构造非推拉固定点
                    elif index == len(centroidsRes.centroids) - 1:
                        self.fixed.append(Fixed.by_onecen(cen1))
                        centroidsRes.centroids.remove(cen1)
                        print("==添加一个非推拉固定点==")
                        print("当前固定点", self)
                        print("当前剩余聚类中心", centroidsRes)
        print("====step4:根据聚类结果求解固定点完成====")
        print("固定点求解结果", self)
        print("聚类结果", centroidsRes)

    def show(self):
        """
        显示对象内的固定点及其可行域
        :return:
        """
        auto2Fixedlist = []
        for index, fixed in enumerate(self.fixed):
            auto2Fixedlist.extend(fixed.show(index))
        return auto2Fixedlist

    def __str__(self):
        return obj_to_string(Auto2Fixed, self)

    def get_feasibles(self):
        """
        为所有的固定点对象求取可行域
        :return:
        """
        for fixed in self.fixed:
            fixed.get_feasible()

    @time_me
    def check_and_move(self):
        """
        经验表明，只需移动推拉式固定点
        :return:
        """
        for fixed in self.fixed:
            if fixed.ispush:
                # fixed.check_cover_validity()
                # if not fixed.covervalid:
                #     print("固定点ispush=", fixed.ispush, "需要移动")
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

    def get_effi(self):
        """
        获取当前auto2Fixed对象的消融效率
        :return:
        """
        Auto2FixedEffi(self).get_effi()

    def cut_elli(self):
        """
        获得不重叠椭球
        :return:
        """
        Auto2FixedEffi(self).cut_elli()

    def show_histogram(self):
        """
        显示直方图
        :return:
        """
        Auto2FixedEffi(self).show_histogram()
#
#
# if __name__ == '__main__':
#     """
#     固定点求解完成
#     """
#     showlist = []
#     showlist.extend(Auto2BaseVtk().show())
#     omega = Omega()
#     omega.get_vtk()
#     omega.get_bodypts()
#     showlist.extend(omega.show())
#     fcom = Fcom()
#     fcom.get_vtk()
#     showlist.extend(fcom.show())
#     centroidsRes = CentroidsRes()
#     centroidsRes.get()  # 得到聚类结果
#     auto2Fixed = Auto2Fixed()
#     auto2Fixed.get_fixed()  # 根据聚类结果得到固定点结果
#     showlist.extend(auto2Fixed.show())
#     show(showlist)
