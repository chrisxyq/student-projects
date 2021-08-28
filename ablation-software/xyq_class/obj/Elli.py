"""
# @author chrisxu
# @create 2020-08-17 17:37
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""

import src.GlobalVar as gl
from vtkplotter import *

from agent.ElliVTKAgent import ElliVTKAgent
from objutils.NeedleUtils import NeedleUtils


class Elli(object):
    """
    椭球对象
    """

    def __init__(self, flag):
        """
        使用flag构造对象
        :param flag: 0：手动规划、1：逐针规划、2：并行规划
        """
        super().__init__()
        if flag==0 or flag==1:
            # 初始化对象属性
            self.flag = flag
            self.name = self.init_name(flag)
            self.color = (152, 251, 152)
            self.alpha = 0.7
            self.R = 26  # 最大短轴半径
            self.K = 1.3
            self.vtk = self.get_vtk()
        else:
            self.flag = flag[0]
            self.name = flag[1]
            self.color = flag[2]
            self.alpha = flag[3]
            self.R = 26  # 最大短轴半径
            self.K = 1.3
            self.vtk = self.get_vtk()


    def init_name(self, flag):
        """
        初始化椭球名
        :return:
        """
        md = gl.get_value('md')
        if flag == 0:
            # 标记类型-层数-(像素坐标)
            return md.comboBox_targets_hand.currentText() + '-' + md.comboBox_inpts_hand.currentText() + '-椭球'
        elif flag == 1:
            return md.comboBox_targets_auto1.currentText() + '-' + md.comboBox_pareto_auto1.currentText() + '-椭球'
        else:
            return 0

    def get_vtk(self):
        """
        根据椭球名得到vtk
        注意：axis1中的参数应为短轴直径：2*self.R
        :return:
        """
        realin, tar = NeedleUtils.ndlname_parser(self.name)
        actor = ElliVTKAgent.get_vtk(realin, tar, self.R, self.K, self.color, self.alpha)
        return actor

    def register(self):
        """
        md.objdic是为了分类管理对象，以及调整对象可见性透明度的时候方便写逻辑判断
        1.将椭球对象注册到md.objdic["消融椭球"]：为了加入到combox_sonobj
        md.needlelist是为了便于显示针的ct点，而且也是便于从该list里面遍历去除要删除的类型的消融针
        2.将椭球对象添加到md.ellilist:
        3.将椭球对象的vtk添加到三维环境
        :return:
        """
        md = gl.get_value('md')
        md.objdic["消融椭球"].append(self.name)
        md.ellilist.append(self)
        # 将针对象的vtk添加到三维环境
        self.vtk.GetProperty().SetColor(self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)
        self.vtk.GetProperty().SetOpacity(self.alpha)
        md.ren.AddActor(self.vtk)
        md.iren.Initialize()

    def remove(self):
        """
        析构方法
        被针的remove方法调用
        :return:
        """
        md = gl.get_value('md')
        md.ren.RemoveActor(self.vtk)
        md.ellilist.remove(self)
        md.objdic["消融椭球"].remove(self.name)

    def change_color(self, color):
        """
        修改对象的颜色
        被needle.change_color调用
        :param color:
        :return:
        """
        self.color = (color[0], color[1], color[2])
        self.vtk.GetProperty().SetColor(self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)

    def change_alpha(self):
        """
        修改对象的alpha
        :param alpha:
        :return:
        """
        md = gl.get_value('md')
        self.alpha = round(md.T_Slider.value() / 100, 2)
        self.vtk.GetProperty().SetOpacity(self.alpha)

    def update_K(self):
        """
        修改长短轴比
        :return:
        """
        md = gl.get_value('md')
        md.ren.RemoveActor(self.vtk)
        md.ellilist.remove(self)
        self.K = round(md.K_Slider.value() / 100 + 1, 2)
        self.vtk = self.get_vtk()
        md.ren.AddActor(self.vtk)
        md.ellilist.append(self)

    def update_R(self):
        """
        修改短轴半径
        :return:
        """
        md = gl.get_value('md')
        md.ren.RemoveActor(self.vtk)
        md.ellilist.remove(self)
        self.R = round(md.R_Slider.value() / 100 * (26 - 13) + 13, 2)
        self.vtk = self.get_vtk()
        md.ren.AddActor(self.vtk)
        md.ellilist.append(self)
