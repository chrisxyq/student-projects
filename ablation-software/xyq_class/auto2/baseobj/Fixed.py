"""
# @author chrisxu
# @create 2020-08-03 14:18
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""

import numpy as np
from vtkplotter import *
import os
import src.GlobalVar as gl
from agent.ElliVTKAgent import ElliVTKAgent
from auto2.ObjToString import obj_to_string
from auto2.objagent.FixedChecker import FixedChecker
from auto2.objagent.FixedFeaAgent import FixedFeaAgent
from auto2.objagent.FixedRegister import FixedRegister
from objutils.BaseVTKUtils import BaseVTKUtils
from objutils.NeedleUtils import NeedleUtils


class Fixed(object):
    """
    单个固定点的类
    """

    def __init__(self, index, isvalid, ispush, pos, centroidpos, direct, subomega):
        """
        当定义一个有着多个构造函数的类时，
        应该让__init__()尽量简单，只用来做属性的赋值，其余什么都不做。
        属性按顺序排列
        :param ispush:
        :param pos:
        :param initdirect:
        :param subomega:
        """
        super().__init__()
        self.colordic = {0: (220, 20, 60), 1: (46, 139, 87), 2: (0, 191, 255), 3: (255, 215, 0),
                         4: (255, 0, 255)}  # 不同固定点的颜色
        self.index = index
        self.color = self.colordic[self.index]
        # self.posvtk = None
        # self.linevtk = []
        # self.ellivtk = []
        # self.subomegavtk = None
        self.R = 26  # 最大短轴半径
        self.K = 1.3  # 长短轴比例
        # self.mycolor = (152, 251, 152)
        self.alpha = 0.7
        self.lw = 5
        self.isvalid = isvalid  # 为了判断是否能推拉
        self.ispush = ispush  # 是否是推拉固定点
        self.pos = pos  # 固定点的位置
        self.centroidpos = centroidpos  # 构成固定点的聚类中心点的位置
        self.direct = direct  # 固定点的初始进针方向
        self.skinintersect = []  # 沿着初始进针方向与皮肤的交点
        self.get_skinintersect()  # 在初始化时就求解

        self.elli = None  # 初始的椭球,是一个List，是为了判断self.covervalid
        if self.skinintersect != []:
            self.get_elli()  # 在初始化时就创造椭球vtk
        self.subomega = subomega  # 管辖的子肿瘤的体点云

        # self.covervalid = True  # 默认沿着初始进针方向，可以完全覆盖消融椭球

        self.feavtk = None  # 固定点的可行域vtk初始化为None

    @classmethod
    def by_twocen(cls, cen1, cen2, index):
        """
        类方法的主要用途就是为了定义其他可选的构造函数。
        类方法的一个关键特性就是把类作为其接受的第一个参数（cls）
        使用两个聚类中心初始化固定点
        :param cen1:
        :param cen2:
        :return:
        """
        isvalid = False  # 有效性初始化为False
        ispush = True
        pos = (np.array(cen1.pos) + np.array(cen2.pos)) / 2  # 固定点位置为两个聚类中心的中点
        centroidpos = [cen1.pos, cen2.pos]
        direct = np.array(cen1.pos) - np.array(cen2.pos)  # 初始进针方向为两个聚类中心的连线
        subomega = cen1.cluster + cen2.cluster  # 管辖子肿瘤体点云为两个聚类点云之和
        return cls(index, isvalid, ispush, pos, centroidpos, direct, subomega)  # 调用当前类的__init__(),并且将创建的对象返回

    @classmethod
    def by_onecen(cls, cen, index):
        """
        使用单个聚类中心初始化固定点
        :param cen1:
        :param cen2:
        :return:
        """
        md = gl.get_value('md')
        isvalid = True  # 有效性一定为True
        ispush = False
        pos = np.array(cen.pos)  # 固定点位置为聚类中心
        centroidpos = cen.pos
        # 初始进针方向为质心可行域与聚类中心的连线
        direct = np.array(md.fcom.vtk.centerOfMass()) - np.array(cen.pos)
        subomega = cen.cluster  # 管辖子肿瘤体点云为聚类点云
        return cls(index, isvalid, ispush, pos, centroidpos, direct, subomega)  # 调用当前类的__init__(),并且将创建的对象返回

    def check_validity(self):
        """
        检验两个聚类中心初始化的推拉固定点是否有效
        若有效，则self.isvalid改为True
        :return:
        """
        FixedChecker(self).check_validity()

    def get_feasible(self):
        """
        求解可行域
        使用FeasibleAgent()代理完成计算
        #使用deletePoints方法修改skin.vtk直接得到质心可行域的三维模型
        可行域求解成功，则feavtk不为none
        :return:
        """
        md = gl.get_value('md')
        casename = md.comboBox_patient.currentText()

        skin = load(os.path.join(md.rootdir, casename, "MESHES_VTK", "skin.vtk"), alpha=0.5)
        del_index = FixedFeaAgent(self).get_del()
        if len(del_index) < len(skin.points()):
            self.feavtk = skin.deletePoints(del_index, renamePoints=True)
            print("====step7:固定点self.ispush=", self.ispush, "的可行域存在", "可行域点数", len(self.feavtk.points()))
        else:
            print("====step7:固定点self.ispush=", self.ispush, "可行域不存在====")

    def get_skinintersect(self):
        """
        获取固定点沿着初始进针方向与皮肤的交点
        以完成initintersect的初始化
        为了求解可行域时使用
        要在get_feasible之前调用
        :return:
        """
        md = gl.get_value('md')
        if self.ispush:
            extension1 = np.array(self.pos) + 200 * np.array(self.direct)
            extension2 = np.array(self.pos) - 200 * np.array(self.direct)
            skin = BaseVTKUtils.basedic["皮肤"]
            intersects = skin.intersectWithLine(extension1, extension2)
            if len(intersects) == 1:
                # print("一个交点")
                self.skinintersect = intersects[0]
            elif len(intersects) == 2:
                # print("两个交点")
                if NeedleUtils.get_dist(intersects[0], self.pos) < NeedleUtils.get_dist(intersects[1], self.pos):
                    self.skinintersect = intersects[0]
                else:
                    self.skinintersect = intersects[1]
            else:
                pass
                #print("推拉式进针与皮肤没有交点")
        else:
            self.skinintersect = md.fcom.vtk.centerOfMass()

    def get_elli(self):
        """
        获得初始的椭球
        :return:
        """
        if self.ispush:
            elli1 = ElliVTKAgent.get_vtk(self.skinintersect, self.centroidpos[0], self.R, self.K, self.color,
                                         self.alpha)
            elli2 = ElliVTKAgent.get_vtk(self.skinintersect, self.centroidpos[1], self.R, self.K, self.color,
                                         self.alpha)
            self.elli = [elli1, elli2]
        else:
            #print(self.skinintersect, self.pos, self.R, self.K, self.color, self.alpha)
            elli = ElliVTKAgent.get_vtk(self.skinintersect, self.pos, self.R, self.K, self.color, self.alpha)

            self.elli = [elli]

    def update_by_subomega(self):
        """
        在subomega变了之后
        1.以形心作为self.fixed.pos
        2.#更新elli
        :return:
        """
        # print("调整前的固定点的位置", self.pos)
        subomega = np.array(self.subomega)
        self.pos = [np.mean(subomega[:, 0]), np.mean(subomega[:, 1]), np.mean(subomega[:, 2])]
        # print("调整后的固定点的位置", self.pos)
        self.get_skinintersect()
        # self.get_elli()

    def show_subomega(self):
        """
        显示fixed的聚类子点云
        仅在获取进针次数被调用
        :return:
        """
        md = gl.get_value('md')
        self.subomegavtk = Points(self.subomega, c=self.color)
        md.ren.AddActor(self.subomegavtk)

    def remove_subomega(self):
        """
        移除fixed的聚类子点云
        :return:
        """
        md = gl.get_value('md')
        md.ren.RemoveActor(self.subomegavtk)

    def show_fea(self):
        """
        显示fixed的可行域
        仅在求解可行域被调用
        :return:
        """
        md = gl.get_value('md')
        if self.feavtk is not None:
            self.feavtk.color(self.color)
            md.ren.AddActor(self.feavtk)

    def remove_fea(self):
        """
        移除fixed的可行域
        :return:
        """
        md = gl.get_value('md')
        if self.feavtk is not None:
            self.feavtk.color(self.color)
            md.ren.RemoveActor(self.feavtk)


    def __str__(self):
        return obj_to_string(Fixed, self)
