"""
# @author chrisxu
# @create 2020-08-20 23:23
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""

import src.GlobalVar as gl
from auto2.objagent.FcomAgent import FcomAgent
from objutils.BaseVTKUtils import BaseVTKUtils
from objutils.NeedleUtils import NeedleUtils


class FixedFeaAgent(FcomAgent):
    """
    step6:固定点可行域求解
    规划方法2的求解可行域的代理类
    继承求解可行域的代理类
    该代理类虽然是单例
    但是可以根据传入的fixed对象初始化多次
    """

    def __init__(self, fixed):
        super().__init__()
        self.fixed = fixed
        self.feasibler = 50

    def get_del(self):
        """
        重写父类的方法
        求解约束
        获取不符合分区约束、避障约束、空腔约束、完全消融约束的del_index
        :return:
        """
        md = gl.get_value('md')
        if len(md.auto2Fixed.fixed) > 1:
            skinpts = BaseVTKUtils.basedic["皮肤"].points()
            target = self.fixed.pos
            del_index = []
            cnt1, cnt2, cnt3, cnt4 = 0, 0, 0, 0

            for index, skinpt in enumerate(skinpts):
                if NeedleUtils.get_dist(skinpt, self.fixed.skinintersect) > self.feasibler:
                    cnt1 += 1
                    del_index.append(index)
                # 避障约束
                elif self.bool_safe(skinpt, target) == 1:
                    cnt2 += 1
                    del_index.append(index)
                # 空腔约束
                elif self.bool_cavity(skinpt, target) == 1:
                    cnt3 += 1
                    del_index.append(index)

            # print("角度约束排除点数", cnt1)
            # print("避障约束排除点数", cnt2)
            # print("空腔约束排除点数", cnt3)


            return del_index
        else:
            return FcomAgent.get_del()
