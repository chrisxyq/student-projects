"""
# @author chrisxu
# @create 2020-08-19 21:39
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法

step1：计算质心可行域
"""
from singleton.Auto2Para import Auto2Para

from singleton.TimeMe import time_me
import os
from vtkplotter import *

from step1agent.FcomAgent import FcomAgent


class Fcom(object):
    """
    ====step1/2:质心可行域求解
    规划方法2的质心可行域类
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造Fcom质心可行域")
        return cls.instance

    def __init__(self):
        if not Fcom.init_flag:
            # print("初始化Fcom质心可行域")
            super().__init__()
            self.color = (255, 165, 0)
            self.alpha = 0.6
            self.vtk = None
            Fcom.init_flag = True

    @time_me
    def get_vtk(self):
        """
        step1：计算质心可行域
        使用FeasibleAgent()代理完成计算
        #使用deletePoints方法修改skin.vtk直接得到质心可行域的三维模型
        :return:
        """
        para = Auto2Para()
        head = para.vtkpath
        skin = load(os.path.join(head, "skin.vtk"), c=self.color,
                    alpha=self.alpha)

        del_index = FcomAgent().get_del()

        # renamePoints：是否修改skin_vtk和a的具体的points
        self.vtk = skin.deletePoints(del_index, renamePoints=True)
        print("====step1/2:质心可行域求解完成====")

    def show(self):
        Fcomlist = []
        Fcomlist.append(self.vtk)
        return Fcomlist

# if __name__ == '__main__':
#     showlist=[]
#     fcom = Fcom()  # 创建质心可行域对象
#     fcom.get_vtk()  # 求解质心可行域
#     showlist.extend(fcom.show())
#     showlist.extend(Auto2BaseVtk().show())
#     show(showlist)
