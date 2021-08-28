"""
# @author chrisxu
# @create 2020-08-23 15:50
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from step3agent.FixedUpdater import FixedUpdater


class Pareto(object):
    """
    方法2得到的单个帕累托解的类
    """

    def __init__(self, auto2Fixed, index, phen, objv):
        super().__init__()
        self.auto2Fixed = auto2Fixed
        self.index = index  # 帕累托点索引编号
        self.phen = phen  # 优化得到的可行域的索引列表
        self.objv = objv  # 在目标函数上的表现
        self.effi = 0

    def update_auto2Fixed(self):
        """
        根据帕累托点，更新auto2Fixed的进针以及消融椭球
        :return:
        """
        for feaindex, indexinfea in enumerate(self.phen):
            fixedUpdater = FixedUpdater(self.auto2Fixed.fixed[feaindex])
            fixedUpdater.update(int(indexinfea))

    def get_effi(self):
        """
        求解消融效率
        :return:
        """
        self.auto2Fixed.get_effi()
