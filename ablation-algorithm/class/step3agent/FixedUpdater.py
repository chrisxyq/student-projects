"""
# @author chrisxu
# @create 2020-08-23 17:42
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from step2.OmegaCore import OmegaCore
import numpy as np


class FixedUpdater(object):
    """
    代理类
    负责更新代理fixed固定点对象的进针以及消融椭球vtk
    """

    def __init__(self, fixed):
        super().__init__()
        self.fixed = fixed  # 里面存储帕累托对象的列表
        self.omegaCore = OmegaCore("_")

    def update(self, indexinfea):
        """
        根据传入的indexinfea
        更新fixed的vtk
        :return:
        """
        self.fixed.skinintersect = self.fixed.feavtk.points()[indexinfea]
        if self.fixed.ispush:
            # 为推拉式固定点求解两个靶点
            extension = 2 * np.array(self.fixed.pos) - np.array(self.fixed.skinintersect)
            tars = self.omegaCore.vtk.intersectWithLine(self.fixed.skinintersect, extension)
            self.fixed.centroidpos = [tars[0], tars[-1]]
        self.fixed.get_elli()
