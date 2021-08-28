"""
# @author chrisxu
# @create 2020-08-19 22:27
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from vtkplotter import show, load

from singleton.Auto2BaseVtk import Auto2BaseVtk
from singleton.Auto2Para import Auto2Para
from singleton.TimeMe import time_me
from step1.CentroidsRes import CentroidsRes
from step1.Fcom import Fcom
from step1.Omega import Omega
# from step2.Auto2Fixed import Auto2Fixed
import os


class OmegaCore(object):
    """
    方法2得到的核心靶点区域
    在得到固定点结果之后
    且存在推拉式固定点
    需要计算
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造OmegaCore核心靶点区域求解的代理类")
        return cls.instance

    def __init__(self, auto2Fixed):
        if not OmegaCore.init_flag:
            super().__init__()
            self.tmr = Auto2BaseVtk().tumor
            para = Auto2Para()
            head = para.vtkpath
            self.vtk = load(os.path.join(head, para.tmrname + ".vtk"),
                            c=Auto2BaseVtk().c_dic[para.tmrname],
                            alpha=Auto2BaseVtk().alpha_dic[para.tmrname])
            self.scale = 1
            self.delta = 0.03

            self.exist = False  # 若不存在推拉式固定点，则为False
            self.include = True  # 当前OmegaCore包含所有的推拉式固定点
            self.auto2Fixed = auto2Fixed
            OmegaCore.init_flag = True

    @time_me
    def get_vtk(self):
        """
        根据传入的所有的固定点对象
        确定核心靶点区域
        不停降低self.scale
        直到不满足如下两个条件的任何一个
        self.vtk.averageSize()>self.tmr.averageSize()-10mm
        self.vtk.isInside(推拉式固定点)

        根据scale确定self.vtk的位置
        :param auto2Fixed:
        :return:
        """
        # print("子类方法")
        # step1：先判断是否存在推拉式固定点
        for fixed in self.auto2Fixed.fixed:
            if fixed.ispush:
                self.exist = True
                break
        # step2:计算
        if self.exist:
            subscale = 1
            tmrpos = self.tmr.centerOfMass()

            while self.vtk.averageSize() > self.tmr.averageSize() - 10 and self.include:
                subscale -= self.delta
                self.vtk = self.vtk.scale(subscale)
                self.scale *= subscale
                vtkpos = [tmrpos[0] * (1 - self.scale), tmrpos[1] * (1 - self.scale),
                          tmrpos[2] * (1 - self.scale)]
                self.vtk.pos(vtkpos)
                self.delta /= 2
                self.bool_include()  # 更新self.vtk.isInside(推拉式固定点)包含信息

            self.vtk.alpha(0.8)
            print("核心靶点区域平均尺寸", self.vtk.averageSize())
            print("肿瘤平均尺寸", self.tmr.averageSize())
            print("核心靶点区域包含所有固定点为", self.include)
            print("====step6:核心靶点区域求解完成====")
        else:
            print("====step6:不存在推拉式固定点，无需求解核心靶点区域====")

    def bool_include(self):
        """
        self.vtk.isInside(推拉式固定点)
        :return:
        """
        for fixed in self.auto2Fixed.fixed:
            if fixed.ispush and self.vtk.isInside(fixed.pos) == False:
                self.include = False

    def show(self):
        omegaCoreshowlist = []
        if self.exist:
            omegaCoreshowlist.append(self.vtk)
        return omegaCoreshowlist

#
# if __name__ == '__main__':
#     """
#     flag==0:核心靶点区域求解完成
#     flag==1:固定点的可行域求解完成
#     """
#     flag = 1
#
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
#     if flag == 0:
#         showlist.extend(auto2Fixed.show())
#     elif flag == 1:
#         omegaCore = OmegaCore()
#         omegaCore.get_vtk()  # 根据固定点结果得到核心靶点区域
#         showlist.extend(omegaCore.show())
#         auto2Fixed.get_feasibles()
#         showlist.extend(auto2Fixed.show())
#         show(showlist)
