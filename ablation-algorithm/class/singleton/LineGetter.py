"""
# @author chrisxu
# @create 2020-08-20 22:17
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from singleton.Auto2Para import Auto2Para
from math import acos
from vtkplotter import *


class LineGetter(object):
    """
    生成进针的vtk的工具类
    多次被调用
    单例
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            #print("构造LineGetter进针生成工具")
        return cls.instance

    def __init__(self):
        if not LineGetter.init_flag:
            #print("初始化LineGetter进针生成工具")
            super().__init__()
            self.c = (152, 251, 152)
            self.len = 150
            self.lw = 5
            LineGetter.init_flag = True

    def get_line_vtk(self, P, T):
        """
        :param P:P未必是真的进针点，需要插补得到150mm的进针点
        :param T:
        :param r:
        :return:
        """
        REALPUN = self.get_REALPUN(T, P)
        line_actor = Line(REALPUN, T, c=self.c, lw=self.lw)

        return line_actor

    def get_REALPUN(self, TAR, PUN):
        """
        获得150mm真实进针点
        :param TAR:
        :param PUN:
        :return:
        """
        #print(TAR, PUN)
        dist = self.get_dist(TAR, PUN)
        REALPUN = TAR + (PUN - TAR) * 150 / dist
        return REALPUN

    def get_dist(self, p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5
