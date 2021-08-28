"""
# @author chrisxu
# @create 2020-08-21 12:02
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法



"""
from vtkplotter import Cylinder
from singleton.LineGetter import LineGetter
from step1.Fcom import Fcom
import numpy as np


class FixedChecker(object):
    """
    step4:根据聚类结果求解固定点
    用于检查生成的临时的固定点的有效性
    代理类
    单例、但是可以初始化多次
    """
    instance = None  # 记录第一个被创建对象的引用

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造FixedChecker固定点检查器")
        return cls.instance

    def __init__(self, fixed):
        """
        在初始化时，需要传入fixed对象作为属性
        """
        super().__init__()
        self.fixed = fixed
        # self.threshold = 0.98

    def check_validity(self):
        """
        若代理的fixed满足两个条件
        条件1：进针路径与质心可行域相交
        条件2：固定点满足完全消融条件
        则将fixed的isvalid属性设为true
        :return:
        """
        if self.bool_intersect_with_fcom() == 1:
            self.fixed.isvalid = True

    def bool_intersect_with_fcom(self):
        """
        条件1：进针路径与质心可行域相交
        若返回值为1，则说明相交
        满足条件
        :return:
        """
        END1 = self.fixed.pos + 100 * self.fixed.direct
        END2 = self.fixed.pos - 100 * self.fixed.direct
        fcomintersects = Fcom().vtk.intersectWithLine(END1, END2)
        if len(fcomintersects) > 0:
            return 1
        else:
            cylinder = Cylinder(pos=self.fixed.pos, r=1, height=LineGetter().get_dist(END1, END2),
                                axis=self.fixed.direct)
            Fcom().vtk.distanceToMesh(cylinder, signed=True, negate=False)
            dists = Fcom().vtk.getPointArray("Distance")
            mindist = np.min(dists)
            if mindist < 5:
                print('推拉路径到可行域的最近距离', np.min(dists))
                return 1
            else:
                return 0

    # def check_cover_validity(self):
    #     """
    #     判断代理固定点的初始进针方向
    #     对于管辖子肿瘤的覆盖有效性
    #     :return:
    #     """
    #     allnum = len(self.fixed.subomega)
    #     insidenum = 0
    #     for omegapt in self.fixed.subomega:
    #         for elli in self.fixed.initelli:
    #             if elli.isInside(omegapt):
    #                 insidenum += 1
    #                 break
    #     print("固定点初始进针方向的消融覆盖率为", round(insidenum / allnum * 100, 1), "%")
    #     if insidenum / allnum < self.threshold:
    #         self.fixed.covervalid = False
