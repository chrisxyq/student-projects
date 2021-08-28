"""
# @author chrisxu
# @create 2020-08-18 14:29
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import copy
from collections import defaultdict

from PyQt5.QtWidgets import QMessageBox

import src.GlobalVar as gl
import os
import numpy as np
from vtkplotter import *


class Par(object):
    """
    自动方法1的帕累托对象
    """

    def __init__(self, tarname):
        super().__init__()
        self.tarname = tarname
        self.color = (0, 255, 0)
        self.alpha = 1
        self.r = 15  # 点的大小
        self.source = self.get_source()
        self.pts = copy.deepcopy(self.source)
        self.Tnum_to_ctpts, self.Snum_to_ctpts, self.Cnum_to_ctpts = \
            defaultdict(list), defaultdict(list), defaultdict(list)
        self.get_TSCnum_to_ctpts()
        self.get_vtk()
        # print("构造par")
        # 初始化各个slider的位置
        md = gl.get_value('md')
        md.angle_Slider.setValue(0)
        md.dist_Slider.setValue(0)
        md.risk_Slider.setValue(0)

    def get_source(self):
        """
        获取原始的帕累托点
        :return:
        """
        md = gl.get_value('md')
        #print(md.comboBox_targets_auto1.currentText())
        txtpath = os.path.join(md.rootdir, md.comboBox_patient.currentText(),"Auto1", md.comboBox_targets_auto1.currentText())
        source = np.loadtxt(os.path.join(txtpath, "par.txt"))
        #print(source)
        return source

    def get_TSCnum_to_ctpts(self):
        """
        根据self.pts
        为了在CT图画出帕累托点
        :return:
        """

        def car_to_ct(pt):
            """
            笛卡尔坐标系转CT坐标系
            :return:
            """
            md = gl.get_value('md')
            return [int(pt[2] / md.caseInfo.st), int(pt[0] / md.caseInfo.ps), int(pt[1] / md.caseInfo.ps)]

        self.Tnum_to_ctpts, self.Snum_to_ctpts, self.Cnum_to_ctpts = \
            defaultdict(list), defaultdict(list), defaultdict(list)
        for pt in self.pts:
            ctpt = car_to_ct(pt[2:5])
            self.Tnum_to_ctpts[ctpt[0]].append([ctpt[1], ctpt[2]])
            self.Snum_to_ctpts[ctpt[1]].append([ctpt[2], ctpt[0]])
            self.Cnum_to_ctpts[ctpt[2]].append([ctpt[1], ctpt[0]])

    def get_vtk(self):
        """
        根据self.pts得到self.vtk
        :return:
        """
        if isinstance(self.pts[0], float):
            self.vtk = Point(self.pts[:, [2, 3, 4]], c=self.color, r=self.r, alpha=self.alpha)
        else:
            self.vtk = Points(self.pts[:, [2, 3, 4]], c=self.color, r=self.r, alpha=self.alpha)

    def register(self):
        """
        md.objdic是为了分类管理对象，以及调整对象可见性透明度的时候方便写逻辑判断
        1.将par对象注册到md.objdic["帕累托点"]：为了加入到combox_sonobj
        2.将par对象添加到md.par:md.par保证窗口只显示唯一的靶点的par帕累托点对象
        3.将par对象的vtk添加到三维环境
        :return:
        """
        # 1.将par对象注册到md.objdic["帕累托点"]：为了加入到combox_sonobj
        self.register_to_objdic()
        self.register_to_par()
        self.register_to_parcombox()
        self.register_to_slider()

    def register_to_objdic(self):
        """
        1.将par对象注册到md.objdic["帕累托点"]：为了加入到combox_sonobj
        :return:
        """
        md = gl.get_value('md')
        md.objdic["帕累托点"] = ["帕累托点"]

    def register_to_par(self):
        """
        1.先在场景中清空self.par
        2.将par对象添加到md.par:md.par保证窗口只显示唯一的靶点的par帕累托点对象
        3.将par对象的vtk添加到三维环境
        :return:
        """
        md = gl.get_value('md')

        if md.par is not None:
            # print("md.par.vtk", md.par.vtk)
            md.ren.RemoveActor(md.par.vtk)
        md.par = self
        md.ren.AddActor(self.vtk)
        # print("self.vtk", self.vtk)

    def register_to_parcombox(self):
        """
        根据self.pts
        首先生成parname，然后
        更新帕累托的combox的列表值
        :return:
        """
        md = gl.get_value('md')
        md.comboBox_pareto_auto1.clear()
        for pt in self.pts:  # 为每个点生成parname
            parname = '1-' + str(int(pt[4] / md.caseInfo.st)) + "-(" + str(int(pt[2] / md.caseInfo.ps)) + "," + str(
                int(pt[3] / md.caseInfo.ps)) + ")"
            md.comboBox_pareto_auto1.addItem(parname)

    def register_to_slider(self):
        """
        567列分别为角度、深度、风险
        根据self.pts的角度深度风险范围
        来初始定位slider的标签显示值
        可用于初始定位和更新后的定位
        :return:
        """
        md = gl.get_value('md')
        md.label_anglemax.setText(str(round(max(self.source[:, 5]), 1)))
        md.label_anglenow.setText(str(round(max(self.pts[:, 5]), 1)))
        md.label_anglemin.setText(str(round(min(self.source[:, 5]), 1)))

        md.label_distmax.setText(str(round(max(self.source[:, 6]), 1)))
        md.label_distnow.setText(str(round(max(self.pts[:, 6]), 1)))
        md.label_distmin.setText(str(round(min(self.source[:, 6]), 1)))

        md.label_riskmax.setText(str(round(1 / max(self.source[:, 7]), 1)))
        md.label_risknow.setText(str(round(1 / max(self.pts[:, 7]), 1)))
        md.label_riskmin.setText(str(round(1 / min(self.source[:, 7]), 1)))

    def update(self):
        """
        根据滑块值更新par对象
        :return:
        """
        self.update_pts()
        self.get_TSCnum_to_ctpts()
        #print("self.pts", len(self.pts), "self.source", len(self.source))
        if self.pts != np.array([]):
            self.get_vtk()
            self.register_to_par()
            self.register_to_parcombox()

    def update_pts(self):
        """
        根据帕累托筛选滑条的值
        从self.source筛选出self.pts
        self.source的567列分别为角度、深度、风险
        :return:
        """
        self.pts = []
        md = gl.get_value('md')
        dist = float(md.label_distnow.text())
        risk = 1 / float(md.label_risknow.text())
        angle = float(md.label_anglenow.text())
        # print(angle, dist, risk)
        for line in self.source:
            if line[5] < angle and line[6] < dist and line[7] < risk:
                self.pts.append(line)
        if self.pts == []:
            QMessageBox.information(md, "提示", "没有符合条件的帕累托点", QMessageBox.Yes)
        self.pts = np.array(self.pts)

    def remove(self):
        """
        析构对象
        :return:
        """
        md = gl.get_value('md')
        md.ren.RemoveActor(self.vtk)
        md.objdic["帕累托点"] = []
        md.par = None

    def change_alpha(self):
        md = gl.get_value('md')
        self.alpha = round(md.T_Slider.value() / 100, 2)
        self.vtk.GetProperty().SetOpacity(self.alpha)
