"""
# @author chrisxu
# @create 2020-08-23 15:59
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""


class Auto2Pareto(object):
    """
    方法2得到的所有的帕累托进针方案的类
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            print("构造Auto2Pareto所有的帕累托进针方案")
        return cls.instance

    def __init__(self, auto2Fixed):
        if Auto2Pareto.init_flag:
            return
        print("初始化Auto2Pareto所有的帕累托进针方案")
        super().__init__()
        self.pareto = []  # 里面存储帕累托对象的列表
        self.chosenindex = 0
        self.auto2Fixed = auto2Fixed
        self.init_flag = True

    def update_auto2Fixed(self):
        """
        根据用户选择的Auto2Pareto的index
        更新所有fixed的vtk
        由Auto2FixedUpdater()代理类完成
        传入pareto，即feasible的index索引列表
        :return:
        """
        print("将显示第", self.chosenindex + 1, "个帕累托进针方案")
        pareto = self.pareto[self.chosenindex]
        pareto.update_auto2Fixed()

    def get_effi(self):
        """
        根据用户选择的Auto2Pareto的index
        求解消融效率
        :return:
        """
        pareto = self.pareto[self.chosenindex]
        pareto.get_effi()
