"""
# @author chrisxu
# @create 2020-08-23 15:59
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl
from auto2.baseobj.Pareto import Pareto
from widgetutils.ComboBoxUtils import ComboBoxUtils


class Auto2Pareto(object):
    """
    方法2得到的所有的帕累托进针方案的类
    """

    def __init__(self, Phen, ObjV):
        super().__init__()
        self.pareto = []  # 里面存储帕累托对象的列表
        self.init_flag = True
        # 初始化pareto成员
        for index in range(len(Phen)):
            pareto = Pareto(index, Phen[index], ObjV[index])
            self.pareto.append(pareto)



    def register(self):
        """
        注册到可选进针方案列表中
        :return:
        """
        ComboBoxUtils.add_to_comboBox_schemes_auto2(self)

    def remove(self):
        """
        析构对象
        :return:
        """
        md = gl.get_value('md')
        md.comboBox_schemes_auto2.clear()
        md.auto2Pareto = None
