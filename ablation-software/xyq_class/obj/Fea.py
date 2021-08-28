"""
# @author chrisxu
# @create 2020-08-18 14:29
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl
import os
import numpy as np
from vtkplotter import *

from agent.FeaAgent import FeaAgent



class Fea(object):
    """
    用于存储自动方法1的可行域和不可行域的对象
    """

    def __init__(self, tarname):
        super().__init__()
        self.tarname = tarname
        self.color = {0: (200, 200, 169), 1: (131, 175, 155),
                      2: (249, 205, 173), 3: (240, 230, 140),
                      4: (255, 99, 71), 5: (0, 255, 255),
                      6: (0, 0, 128), 7: (255, 165, 0)}
        self.alpha = {0: 0.4, 1: 0.4, 2: 0.4, 3: 0.4,
                      4: 0.4, 5: 0.4, 6: 0.4, 7: 0.4}
        self.indextoname = {0: "仰卧姿态约束不可行域",
                            1: "针长约束不可行域",
                            2: "空腔约束不可行域",
                            3: "避障约束不可行域",
                            4: "切角约束不可行域",
                            5: "肝脏距离约束不可行域",
                            6: "针干涉约束不可行域",
                            7: "可行域"}

        self.nametoindex = {"仰卧姿态约束不可行域": 0,
                            "针长约束不可行域": 1,
                            "空腔约束不可行域": 2,
                            "避障约束不可行域": 3,
                            "切角约束不可行域": 4,
                            "肝脏距离约束不可行域": 5,
                            "针干涉约束不可行域": 6,
                            "可行域": 7}
        self.r = 5  # 点的大小
        self.ptslist = self.get_ptslist()
        self.Tnum_to_ctpts, self.Snum_to_ctpts, self.Cnum_to_ctpts = None, None, None
        self.get_TSCnum_to_ctpts()
        self.vtk = self.get_vtk()

    def get_TSCnum_to_ctpts(self):
        """
        根据self.ptslist
        为了在CT图画出可行域
        :return:
        """
        agent = FeaAgent(self)
        agent.get_TSCnum_to_ctpts()

    def change_alpha(self, name):
        """
        给定名字
        修改相应的vtk的透明度
        :param alpha:
        :return:
        """
        md = gl.get_value('md')
        index = self.nametoindex[name]
        vtk = self.vtk[index]
        self.alpha[index] = round(md.T_Slider.value() / 100, 2)
        vtk.GetProperty().SetOpacity(self.alpha[index])

    def get_ptslist(self):
        """
        求解约束得到ptlist
        :return: 长度为8的数组，每个数组为相应的可行域的点
        """
        md = gl.get_value('md')
        ptslist = []
        txtpath = os.path.join(md.rootdir, md.comboBox_patient.currentText(),
                               "Auto1", md.comboBox_targets_auto1.currentText())
        for i in range(7):
            ptslist.append(np.loadtxt(os.path.join(txtpath, str(i) + ".txt")))
        ptslist.append(np.loadtxt(os.path.join(txtpath, "7.txt"))[:, [2, 3, 4]])
        return ptslist

    def get_vtk(self):
        """
        根据self.ptlist初始化vtk对象
        若self.ptlist的元素为[]，则vtk对象为null
        :return:
        """
        vtklist = []
        for i, pts in enumerate(self.ptslist):
            if len(pts) != 0:
                vtklist.append(Points(pts, c=self.color[i], r=self.r, alpha=self.alpha[i]))
            else:
                vtklist.append(None)
        return vtklist

    def register(self):
        """
        md.objdic是为了分类管理对象，以及调整对象可见性透明度的时候方便写逻辑判断
        1.将fea对象注册到md.objdic["可行域"]：为了加入到combox_sonobj
        2.将fea对象添加到md.fea:md.fea保证窗口只显示唯一的靶点的fea可行域对象
        3.将fea对象的vtk添加到三维环境
        :return:
        """
        # 1.将fea对象注册到md.objdic["可行域"]：为了加入到combox_sonobj
        self.register_to_objdic()
        self.register_to_fea()

    def register_to_objdic(self):
        """
        1.将fea对象注册到md.objdic["可行域"]：为了加入到combox_sonobj
        :return:
        """
        md = gl.get_value('md')
        md.objdic["可行域"] = []
        for i, vtkobj in enumerate(self.vtk):
            if vtkobj is not None:
                md.objdic["可行域"].append(self.indextoname[i])

    def register_to_fea(self):
        """
        1.先在场景中清空self.fea
        2.将fea对象添加到md.fea:md.fea保证窗口只显示唯一的靶点的fea可行域对象
        3.将fea对象的vtk添加到三维环境
        :return:
        """
        md = gl.get_value('md')
        if md.fea is not None:
            md.fea.del_vtk_from_ren()
        md.fea = self
        md.fea.add_vtk_to_ren()

    def del_vtk_from_ren(self):
        """
        从场景中删除fea对象的vtk文件
        :return:
        """
        md = gl.get_value('md')
        for vtkobj in self.vtk:
            if vtkobj is not None:
                md.ren.RemoveActor(vtkobj)

    def add_vtk_to_ren(self):
        """
        从场景中添加fea对象的vtk文件
        :return:
        """
        md = gl.get_value('md')
        for vtkobj in self.vtk:
            if vtkobj is not None:
                md.ren.AddActor(vtkobj)

    def remove(self):
        """
        析构
        :return:
        """
        md = gl.get_value('md')
        self.del_vtk_from_ren()
        md.objdic["可行域"] = []
        md.fea = None
