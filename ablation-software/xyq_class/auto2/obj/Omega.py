"""
# @author chrisxu
# @create 2020-08-19 21:41
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl

from vtkplotter import *
import os

from auto2.objagent.OmegaAgent import OmegaAgent
from objutils.BaseVTKUtils import BaseVTKUtils


class Omega(object):
    """
    ====step1/2:待消融区域求解
    规划方法2的待消融区域类
    """

    def __init__(self):
        super().__init__()
        md = gl.get_value('md')
        casename = md.comboBox_patient.currentText()
        tmrname = md.comboBox_tmrs_auto2.currentText()
        self.tmr = BaseVTKUtils.basedic[BaseVTKUtils.namemap[tmrname]]
        self.c = BaseVTKUtils.c[BaseVTKUtils.namemap[tmrname]]
        self.alpha = BaseVTKUtils.alpha[BaseVTKUtils.namemap[tmrname]]

        self.vtk = load(os.path.join(md.rootdir, casename, "MESHES_VTK", tmrname + ".vtk"), c=self.c, alpha=self.alpha)
        self.scale = 1
        self.delta = 0.03
        self.bodypts = []
        self.boundingpoints = []
        self.Vbpt = 0

    def get_vtk(self):
        """
        预处理步骤：获取肿瘤的待消融区域的vtk
        不停增加self.scale
        直到self.vtk.averageSize()>self.tmr.averageSize()+5mm
        tmr.averageSize()
        根据scale确定self.vtk的位置
        :return:
        """
        # print("父类方法")
        subscale = 1
        tmrpos = self.tmr.centerOfMass()
        while self.vtk.averageSize() < self.tmr.averageSize() + 2:
            subscale += self.delta
            self.vtk = self.vtk.scale(subscale)
            self.scale *= subscale
            vtkpos = [tmrpos[0] * (1 - self.scale), tmrpos[1] * (1 - self.scale),
                      tmrpos[2] * (1 - self.scale)]
            self.vtk.pos(vtkpos)
            self.delta /= 2

        self.vtk.alpha(0.2)
        print("====待消融区域膨胀因子求解完成====")
        # print("肿瘤形心", self.tmr.centerOfMass())
        # print("待消融区域形心", self.vtk.centerOfMass())
        print("肿瘤体积", round(self.tmr.volume() / 1000, 2), "ml")
        print("肿瘤平均尺寸", round(self.tmr.averageSize(), 2), "mm")
        print("待消融区域体积", round(self.vtk.volume() / 1000, 2), "ml")
        print("待消融区域平均尺寸", round(self.vtk.averageSize(), 2), "mm")

    def get_bodypts(self):
        """
        预处理步骤：计算肿瘤的待消融区域的体点云
        :return:
        """
        OmegaAgent(self).get_bodypts()
        print("====step1/2:待消融区域体点云求解完成====")

    def show(self):
        """
        添加到场景
        :return:
        """
        md = gl.get_value('md')
        md.ren.AddActor(self.vtk)

    def remove(self):
        """
        从场景移除
        :return:
        """
        md = gl.get_value('md')
        if md.omega != None:
            md.ren.RemoveActor(self.vtk)
            md.omega = None
