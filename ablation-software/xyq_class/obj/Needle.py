"""
# @author chrisxu
# @create 2020-08-17 16:54
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from collections import defaultdict

import src.GlobalVar as gl

from vtkplotter import *

from objutils.NeedleUtils import NeedleUtils


class Needle(object):
    """
    针对象
    """

    def __init__(self, flag):
        """
        使用flag构造对象
        :param flag: 0：手动规划、1：逐针规划、2：并行规划
        """
        super().__init__()
        if flag == 0 or flag == 1:
            # 初始化对象属性
            self.flag = flag
            self.name = self.init_name(flag)
            self.Tnum_to_ctpts, self.Snum_to_ctpts, self.Cnum_to_ctpts = self.get_TSCnum_to_ctpts()
            self.color = (152, 251, 152)
            self.alpha = 1
            self.lw = 4
            self.vtk = self.get_vtk()
        else:
            self.flag = flag[0]
            self.name = flag[1]
            self.Tnum_to_ctpts, self.Snum_to_ctpts, self.Cnum_to_ctpts = self.get_TSCnum_to_ctpts()
            self.color = flag[2]
            self.alpha = flag[3]
            self.lw = flag[4]
            self.vtk = self.get_vtk()

    def init_name(self, flag):
        """
        初始化针名
        :return:
        """
        md = gl.get_value('md')
        if flag == 0:
            # 标记类型-层数-(像素坐标)
            return md.comboBox_targets_hand.currentText() + '-' + md.comboBox_inpts_hand.currentText()
        elif flag == 1:
            return md.comboBox_targets_auto1.currentText() + '-' + md.comboBox_pareto_auto1.currentText()
        else:
            return 0

    def get_vtk(self):
        """
        根据针名得到vtk
        :return:
        """
        realin, tar = NeedleUtils.ndlname_parser(self.name)
        return NeedleUtils.get_vtk(realin, tar, self.color, self.alpha, self.lw)

    def get_TSCnum_to_ctpts(self):
        """
        针在TSC面的层数到TSC面CT图像坐标点的映射
        :return:
        """
        Tnum_to_ctpts = defaultdict(list)
        Snum_to_ctpts = defaultdict(list)
        Cnum_to_ctpts = defaultdict(list)
        tarinct, ctptnum, nvec = NeedleUtils.get_ctptnum(self.name)
        for j in range(ctptnum):
            ctpt = [int(tarinct[0] + nvec[0] * j), int(tarinct[1] + nvec[1] * j), int(tarinct[2] + nvec[2] * j)]
            Tnum_to_ctpts[ctpt[0]].append([ctpt[1], ctpt[2]])
            Snum_to_ctpts[ctpt[1]].append([ctpt[2], ctpt[0]])
            Cnum_to_ctpts[ctpt[2]].append([ctpt[1], ctpt[0]])
        return Tnum_to_ctpts, Snum_to_ctpts, Cnum_to_ctpts

    def register(self):
        """
        md.objdic是为了分类管理对象，以及调整对象可见性透明度的时候方便写逻辑判断
        1.将针对象注册到md.objdic["消融针"]：为了加入到combox_sonobj
        md.needlelist是为了便于显示针的ct点，而且也是便于从该list里面遍历去除要删除的类型的消融针
        2.将针对象添加到md.needlelist:
        3.将针对象的vtk添加到三维环境
        :return:
        """
        md = gl.get_value('md')
        md.objdic["消融针"].append(self.name)
        md.needlelist.append(self)
        # 将针对象的vtk添加到三维环境
        self.vtk.GetProperty().SetColor(self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)
        self.vtk.GetProperty().SetOpacity(self.alpha)
        md.ren.AddActor(self.vtk)
        md.iren.Initialize()

    def change_color(self, color):
        """
        修改针对象的颜色
        配套调用elli的修改颜色方法
        :param color:
        :return:
        """
        md = gl.get_value('md')
        self.color = (color[0], color[1], color[2])
        self.vtk.GetProperty().SetColor(self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)
        # 配套调用elli的修改颜色方法
        # 如果是auto2的针，那个和椭球的绑定标准为针的后缀autoX，否则根据针名绑定椭球
        standard = self.name.split('-')[-1] if self.flag == 2 else self.name

        for elliobj in md.ellilist:
            if standard in elliobj.name:
                elliobj.change_color(color)

    def remove(self):
        """
        1.将针对象的vtk从三维环境删除
        2.将针对象从md.needlelist删除
        3.将针对象从md.objdic["消融针"]删除：为了从combox_sonobj删除
        1.配套调用elli的remove

        :return:
        """
        md = gl.get_value('md')
        md.ren.RemoveActor(self.vtk)
        md.needlelist.remove(self)
        md.objdic["消融针"].remove(self.name)
        # 配套调用elli的remove
        standard = self.name.split('-')[-1] if self.flag == 2 else self.name
        # 边遍历边删除防止漏删
        for i in range(len(md.ellilist) - 1, -1, -1):
            if standard in md.ellilist[i].name:
                md.ellilist[i].remove()
