"""
# @author chrisxu
# @create 2020-08-19 21:39
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法

step1：计算质心可行域
"""

import os
from vtkplotter import *
import src.GlobalVar as gl
from auto2.objagent.FcomAgent import FcomAgent


class Fcom(object):
    """
    ====step1/2:质心可行域求解
    规划方法2的质心可行域类
    """

    def __init__(self):
        # print("初始化Fcom质心可行域")
        super().__init__()
        self.color = (255, 165, 0)
        self.alpha = 0.6
        self.vtk = None

    def get_vtk(self):
        """
        step1：计算质心可行域
        使用FeasibleAgent()代理完成计算
        #使用deletePoints方法修改skin.vtk直接得到质心可行域的三维模型
        :return:
        """
        md = gl.get_value('md')
        casename = md.comboBox_patient.currentText()
        skin = load(os.path.join(md.rootdir, casename, "MESHES_VTK", "skin.vtk"), c=self.color, alpha=self.alpha)

        del_index = FcomAgent().get_del()

        # renamePoints：是否修改skin_vtk和a的具体的points
        self.vtk = skin.deletePoints(del_index, renamePoints=True)
        print("====step1/2:质心可行域求解完成====")

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
        if md.fcom != None:
            md.ren.RemoveActor(self.vtk)
            md.fcom = None
