"""
# @author chrisxu
# @create 2020-08-22 22:35
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""

import numpy as np


class FixedMover(object):
    """
    step5:初步调整固定点
    用于移动固定点的代理类
    单例、但是可以初始化多次
    """
    instance = None  # 记录第一个被创建对象的引用

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造FixedMover固定点移动器")
        return cls.instance

    def __init__(self, auto2Fixed):
        """
        在初始化时，需要传入fixed对象作为属性
        """
        super().__init__()
        self.auto2Fixed = auto2Fixed

    def move(self, fixed):
        """
        移动代理的fixed的对象的位置
        :return:
        """
        # 首先获取在auto2fixed列表中，除fixed之外的其余所有的fixed对象的椭球vtk
        otherellis = self.get_other_ellis(fixed)
        if otherellis != []:
            # 然后遍历self.fixed.subomega的点，若位于step1的椭球列表内，则删除
            for i in range(len(fixed.subomega) - 1, -1, -1):
                for elli in otherellis:
                    if elli.isInside(fixed.subomega[i]):
                        np.delete(fixed.subomega,i)
                        # print(fixed.subomega[i].all())
                        # fixed.subomega.remove(fixed.subomega[i].all())
                        break
            # 更新self.fixed.subomega之后，以形心作为self.fixed.pos\更新elli
            fixed.update_by_subomega()

    def get_other_ellis(self, fixed):
        """
        首先获取在auto2fixed列表中，除fixed之外的其余所有的fixed对象的椭球vtk
        :param fixed:
        :return:
        """
        otherellis = []
        for traversefixed in self.auto2Fixed.fixed:
            if traversefixed != fixed:
                otherellis.extend(traversefixed.elli)
        return otherellis
