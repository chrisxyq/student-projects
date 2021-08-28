"""
# @author chrisxu
# @create 2020-08-19 22:47
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import time

from singleton.Auto2BaseVtk import Auto2BaseVtk
from singleton.TimeMe import time_me
from step1.CentroidsRes import CentroidsRes
from step1.Fcom import Fcom
from step1.Omega import Omega
from step2.Auto2Fixed import Auto2Fixed
from step2.OmegaCore import OmegaCore
from vtkplotter import *

from step3.MOEA import MOEA
from step3base.Auto2Pareto import Auto2Pareto
from step3base.Pareto import Pareto


@time_me
def main_process():
    """
    算法主流程
    :return:
    """
    omega = Omega()
    omega.get_vtk()
    omega.get_bodypts()  # step1/2:得到待消融区域
    fcom = Fcom()
    fcom.get_vtk()  # step1/2:得到质心可行域
    centroidsRes = CentroidsRes()
    centroidsRes.get()  # step3:得到聚类结果
    auto2Fixed = Auto2Fixed()
    auto2Fixed.get_fixed()  # step4:根据聚类结果得到固定点结果
    auto2Fixed.check_and_move()  # step5:初步调整推拉式固定点
    omegaCore = OmegaCore(auto2Fixed)
    omegaCore.get_vtk()  # step6:根据固定点结果得到核心靶点区域
    auto2Fixed.get_feasibles()  # step7:为固定点求解可行域

    moea = MOEA(auto2Fixed)
    Phen, ObjV = moea.run()  # step8:使用NSGA-II优化，将优化得到的数据装配到pareto对象
    print("====算法主流程结束====")
    return Phen, ObjV


def myshow(Phen, ObjV):
    """
    用于显示
    :param Phen:
    :param ObjV:
    :return:
    """
    # 将优化得到的数据装配到pareto对象
    auto2Pareto = Auto2Pareto(Auto2Fixed())
    for index in range(len(Phen)):
        pareto = Pareto(Auto2Fixed(), index, Phen[index], ObjV[index])
        auto2Pareto.pareto.append(pareto)
    showlist = []
    showlist.extend(Auto2BaseVtk().show())  # 基本场景
    showlist.extend(Omega().show())  # 待消融区域
    # showlist.extend(Fcom().show())#质心可行域
    # showlist.extend(OmegaCore().show())#核心靶点区域
    auto2Pareto.update_auto2Fixed()  # 根据pareto对象，更新auto2fixed的针和椭球的vtk
    auto2Pareto.get_effi()  # 为所选帕累托点计算消融效率
    showlist.extend(Auto2Fixed().show())  # 显示优化的进针方案
    show(showlist)


if __name__ == '__main__':
    Phen, ObjV = main_process()
    myshow(Phen, ObjV)
