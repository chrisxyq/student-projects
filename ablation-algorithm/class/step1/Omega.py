"""
# @author chrisxu
# @create 2020-08-19 21:41
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import threading

from vtkplotter import *
from singleton.Auto2BaseVtk import Auto2BaseVtk
import os

from singleton.Auto2Para import Auto2Para
from singleton.TimeMe import time_me
from step1agent.OmegaAgent import OmegaAgent


class Omega(object):
    """
    ====step1/2:待消融区域求解
    规划方法2的待消融区域类
    """
    _instance_lock = threading.Lock()

    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        """
        可被继承的单例模式
        :param args:
        :param kwargs:
        :return:
        """
        if not hasattr(cls, 'instance_dict'):
            Omega.instance_dict = {}

        if str(cls) not in Omega.instance_dict.keys():
            with Omega._instance_lock:
                _instance = super().__new__(cls)
                Omega.instance_dict[str(cls)] = _instance

        return Omega.instance_dict[str(cls)]

    def __init__(self):
        """
        仅初始化一次，
        因此子类继承时，不会调用父类的初始化方法
        子类无法继承父类的属性
        """
        if not Omega.init_flag:
            # print("初始化Omega待消融区域")
            super().__init__()
            self.tmr = Auto2BaseVtk().tumor
            para = Auto2Para()
            head = para.vtkpath
            self.vtk = load(os.path.join(head, para.tmrname + ".vtk"),
                            c=Auto2BaseVtk().c_dic[para.tmrname],
                            alpha=Auto2BaseVtk().alpha_dic[para.tmrname])
            self.scale = 1
            self.delta = 0.03
            self.bodypts = []
            self.boundingpoints = []
            self.Vbpt = 0
            Omega.init_flag = True

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

    @time_me
    def get_bodypts(self):
        """
        预处理步骤：计算肿瘤的待消融区域的体点云
        :return:
        """
        OmegaAgent(self).get_bodypts()
        print("====step1/2:待消融区域体点云求解完成====")

    def show(self):
        omegashowlist = []
        omegashowlist.append(self.vtk)
        return omegashowlist

# if __name__ == '__main__':
#     omega = Omega()
#     show(omega.vtk, Points(omega.bodypts))
