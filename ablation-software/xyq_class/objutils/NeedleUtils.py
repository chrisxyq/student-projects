"""
# @author chrisxu
# @create 2020-08-17 17:10
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import re

import src.GlobalVar as gl
from vtkplotter import *


class NeedleUtils(object):


    @staticmethod
    def get_vtk(realin, tar, color, alpha, lw):
        return Line(realin, tar, c=color, alpha=alpha, lw=lw)

    @staticmethod
    def get_ctptnum(ndlname):
        """
        输出ndlname的针在CT坐标系下的点的信息
        :return:
        """
        data = re.findall(r"\d+\.?\d*", ndlname)
        tarinct = [int(data[1]), int(data[2]), int(data[3])]
        puninct = [int(data[5]), int(data[6]), int(data[7])]
        realpuninct = NeedleUtils.get_real_inpt(puninct, tarinct)
        vec = [realpuninct[0] - tarinct[0], realpuninct[1] - tarinct[1], realpuninct[2] - tarinct[2]]
        ctptnum = int(max(abs(vec[0]), abs(vec[1]), abs(vec[2])))
        nvec = [n / ctptnum for n in vec]
        return tarinct, ctptnum, nvec

    @staticmethod
    def ndlname_parser(ndlname):
        """
        用于解析ndlname
        输出笛卡尔坐标系下，真正的进针点和靶点
        :return:
        """
        md = gl.get_value('md')
        data = re.findall(r"\d+\.?\d*", ndlname)
        tar = [int(data[2]) * md.caseInfo.ps, int(data[3]) * md.caseInfo.ps,
               int(data[1]) * md.caseInfo.st]
        inpt = [int(data[6]) * md.caseInfo.ps, int(data[7]) * md.caseInfo.ps,
                int(data[5]) * md.caseInfo.st]
        realin = NeedleUtils.get_real_inpt(inpt, tar)
        return realin, tar

    @staticmethod
    def get_dist(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5

    @staticmethod
    def get_real_inpt(inpt, tar):
        dist = NeedleUtils.get_dist(inpt, tar)
        return [tar[0] + (inpt[0] - tar[0]) * 150 / dist, tar[1] + (inpt[1] - tar[1]) * 150 / dist,
                tar[2] + (inpt[2] - tar[2]) * 150 / dist]

