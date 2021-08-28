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
import src.GlobalVar as gl

import os

from objutils.BaseVTKUtils import BaseVTKUtils


class OmegaCore(object):
    """
    方法2得到的核心靶点区域
    在得到固定点结果之后
    且存在推拉式固定点
    需要计算
    """

    def __init__(self):
        super().__init__()
        md = gl.get_value('md')
        self.tmrname = md.comboBox_tmrs_auto2.currentText()

        self.casename = md.comboBox_patient.currentText()
        self.c = BaseVTKUtils.c[BaseVTKUtils.namemap[self.tmrname]]
        self.tmralpha = BaseVTKUtils.alpha[BaseVTKUtils.namemap[self.tmrname]]
        self.vtk = None
        self.scale = 1
        self.delta = 0.06
        self.alpha = 0.9

        self.exist = False  # 若不存在推拉式固定点，则为False
        self.include = True  # 当前OmegaCore包含所有的推拉式固定点

    def get_vtk(self):
        """
        根据传入的所有的固定点对象
        确定核心靶点区域
        不停降低self.scale
        直到不满足如下两个条件的任何一个
        self.vtk.averageSize()>self.tmr.averageSize()-8mm
        self.vtk.isInside(推拉式固定点)

        根据scale确定self.vtk的位置
        :param auto2Fixed:
        :return:
        """
        md = gl.get_value('md')
        self.tmr = BaseVTKUtils.basedic[BaseVTKUtils.namemap[self.tmrname]]
        self.vtk = load(os.path.join(md.rootdir, self.casename, "MESHES_VTK", self.tmrname + ".vtk"), c=self.c,
                        alpha=self.tmralpha)
        # step1：先判断是否存在推拉式固定点
        for fixed in md.auto2Fixed.fixed:
            if fixed.ispush:
                self.exist = True
                break
        # step2:计算
        if self.exist:
            subscale = 1
            tmrpos = self.tmr.centerOfMass()

            while self.vtk.averageSize() > self.tmr.averageSize() - 8:
                # print(self.scale)
                # print(self.vtk.averageSize(), self.tmr.averageSize())
                subscale -= self.delta
                # print(subscale,self.delta)
                self.vtk = self.vtk.scale(subscale)
                # print(self.vtk.averageSize(), self.tmr.averageSize())
                self.scale *= subscale
                # print(self.scale)
                vtkpos = [tmrpos[0] * (1 - self.scale), tmrpos[1] * (1 - self.scale),
                          tmrpos[2] * (1 - self.scale)]
                self.vtk.pos(vtkpos)
                # self.delta /= 1.1
                # self.bool_include()  # 更新self.vtk.isInside(推拉式固定点)包含信息

            self.vtk.alpha(self.alpha)
            # print(self.vtk.averageSize())
            # show(self.vtk, self.tmr)
            print("核心靶点区域平均尺寸", self.vtk.averageSize())
            print("肿瘤平均尺寸", self.tmr.averageSize())
            #print("核心靶点区域包含所有固定点为", self.include)
            print("====step6:核心靶点区域求解完成====")
        else:
            print("====step6:不存在推拉式固定点，无需求解核心靶点区域====")

    def bool_include(self):
        """
        self.vtk.isInside(推拉式固定点)
        :return:
        """
        md = gl.get_value('md')
        for fixed in md.auto2Fixed.fixed:
            if fixed.ispush and self.vtk.isInside(fixed.pos) == False:
                self.include = False

    def show(self):
        md = gl.get_value('md')
        md.ren.AddActor(self.vtk)

    def remove(self):
        md = gl.get_value('md')
        md.ren.RemoveActor(self.vtk)
        md.omegaCore = None
