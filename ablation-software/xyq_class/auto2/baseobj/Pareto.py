"""
# @author chrisxu
# @create 2020-08-23 15:50
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import numpy as np
from PyQt5.QtWidgets import QMessageBox

import src.GlobalVar as gl


class Pareto(object):
    """
    方法2得到的单个帕累托解的类
    """

    def __init__(self, index, phen, objv):
        super().__init__()
        self.index = index  # 帕累托点索引编号
        self.phen = phen  # 优化得到的可行域的索引列表
        self.objv = objv  # 在目标函数上的表现
        self.effi = 0

    def update_auto2Fixed(self):
        """
        根据用户选择的Auto2Pareto的index
        更新所有fixed的vtk
        根据帕累托点，更新auto2Fixed的进针以及消融椭球
        :return:
        """
        md = gl.get_value('md')
        for feaindex, indexinfea in enumerate(self.phen):
            fixed = md.auto2Fixed.fixed[feaindex]
            indexinfea = int(indexinfea)
            # 更新固定点的皮肤交点
            fixed.skinintersect = fixed.feavtk.points()[indexinfea]
            if fixed.ispush:
                # 为推拉式固定点更新求解两个靶点
                extension = 2 * np.array(fixed.pos) - np.array(fixed.skinintersect)
                tars = md.omegaCore.vtk.intersectWithLine(fixed.skinintersect, extension)
                #print("推拉式固定点与核心靶点区域交点", tars)
                #print("推拉式固定点与核心靶点区域交点个数", len(tars))
                if len(tars) != 2:
                    QMessageBox.information(md, "提示", "请换一个进针方案！", QMessageBox.Yes)
                    return
                fixed.centroidpos = [tars[0], tars[-1]]
            print("第", str(feaindex), "个固定点更新完成")


