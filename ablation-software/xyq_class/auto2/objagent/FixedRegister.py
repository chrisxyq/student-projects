"""
# @author chrisxu
# @create 2020-08-27 0:31
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl
from obj.Elli import Elli
from obj.Needle import Needle


class FixedRegister(object):
    """
    固定点注册成针对象或者椭球对象的代理类
    """

    def __init__(self, fixed):
        super().__init__()
        self.fixed = fixed

    def regist(self):
        """
        代理方法
        固定点注册成针对象或者椭球对象
        生成固定点的针和椭球
        并且注册到环境
        # 首先调用ndllistutils和ellilistutils的方法
        # 批量删除之前的针和椭球对象
        :return:
        """
        flag, color, alpha, lw = 2, self.fixed.color, self.fixed.alpha, 4
        if self.fixed.ispush:
            # 为防止显示误差，推拉进针仅显示一根针
            prename1 = self.get_prename(self.fixed.centroidpos[0], self.fixed.skinintersect)
            ndlname1 = prename1 + "-Fixed" + str(self.fixed.index)
            ndl1 = Needle([flag, ndlname1, color, alpha, lw])
            prename2 = self.get_prename(self.fixed.centroidpos[1], self.fixed.skinintersect)
            ndlname2 = prename2 + "-Fixed" + str(self.fixed.index)
            # ndl2 = Needle([flag, ndlname2, color, alpha, lw])
            #print("针名1", ndlname1)
            # print("针名2",ndlname2)

            elliname1 = ndlname1 + "-椭球"
            elli1 = Elli([flag, elliname1, color, alpha])
            elliname2 = ndlname2 + "-椭球"
            elli2 = Elli([flag, elliname2, color, alpha])
            #print("针和椭球的vtk对象已经产生")

            ndl1.register()
            # ndl2.register()
            elli1.register()
            elli2.register()

        else:
            prename = self.get_prename(self.fixed.pos, self.fixed.skinintersect)
            ndlname = prename + "-Fixed" + str(self.fixed.index)
            ndl = Needle([flag, ndlname, color, alpha, lw])
            elliname = ndlname + "-椭球"
            elli = Elli([flag, elliname, color, alpha])
            #print(ndl.color, ndl.alpha)
            #print("针和椭球的vtk对象已经产生")
            ndl.register()
            elli.register()

    def get_prename(self, tar, inpt):
        """
        生成针/椭球的命名前缀
        :return:
        """

        def car_to_ct(pt):
            """
            笛卡尔坐标系转CT坐标系
            :return:
            """
            md = gl.get_value('md')
            return [int(pt[2] / md.caseInfo.st), int(pt[0] / md.caseInfo.ps), int(pt[1] / md.caseInfo.ps)]

        cttar = car_to_ct(tar)
        ctinpt = car_to_ct(inpt)
        prename = "1-" + str(cttar[0]) + "-(" + str(cttar[1]) + "," + str(cttar[2]) + ")-1-" + str(
            ctinpt[0]) + "-(" + str(ctinpt[1]) + "," + str(ctinpt[2]) + ")"
        return prename
