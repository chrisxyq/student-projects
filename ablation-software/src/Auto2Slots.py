"""
# @author chrisxu
# @create 2020-08-25 10:49
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from PyQt5.QtWidgets import QMessageBox

import src.GlobalVar as gl
from auto2.baseobj.Pareto import Pareto
from auto2.obj.Auto2Fixed import Auto2Fixed
from auto2.obj.Auto2Pareto import Auto2Pareto
from auto2.obj.CentroidsRes import CentroidsRes
from auto2.obj.Fcom import Fcom
from auto2.obj.Omega import Omega
from auto2.obj.OmegaCore import OmegaCore
from auto2.optimize.MOEA import MOEA
from objutils.ElliListUtils import ElliListUtils
from objutils.NdlListUtils import NdlListUtils
from scrollct.Scroller import Scroller
from src.ParaSlots import on_comboBox_farobj
from widgetutils.LineEditUtils import LineEditUtils


def on_getabnum_auto2():
    """
    获取消融次数的槽函数
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.init3D:
            if md.omega is None:
                md.omega = Omega()
                md.omega.get_vtk()
                md.omega.get_bodypts()  # step1/2:得到待消融区域
                md.fcom = Fcom()
                md.fcom.get_vtk()  # step1/2:得到质心可行域
                md.centroidsRes = CentroidsRes()
                md.centroidsRes.get()  # step3:得到聚类结果
                md.omega.show()
                md.fcom.show()
                md.iren.Initialize()
                LineEditUtils.update_lineEdit_abnum_auto2()
            else:
                QMessageBox.information(md, "提示", "消融次数已计算或上个肿瘤规划结果未清空", QMessageBox.Yes)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

def on_getpnum_auto2():
    """
    获取进针次数的槽函数
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.init3D:
            if md.centroidsRes is not None:
                if md.auto2Fixed is None:
                    md.auto2Fixed = Auto2Fixed()
                    md.auto2Fixed.get_fixed()  # step4:根据聚类结果得到固定点结果
                    md.auto2Fixed.check_and_move()  # step5:初步调整推拉式固定点
                    md.omegaCore = OmegaCore()
                    md.omegaCore.get_vtk()  # step6:根据固定点结果得到核心靶点区域
                    md.omegaCore.show()
                    md.fcom.remove()
                    md.auto2Fixed.show_subomega()
                    md.iren.Initialize()
                    LineEditUtils.update_lineEdit_pnum_auto2()

                    print("ok")
                else:
                    QMessageBox.information(md, "提示", "进针次数已计算或上个肿瘤规划结果未清空", QMessageBox.Yes)
            else:
                QMessageBox.information(md, "提示", "请先确定消融次数！", QMessageBox.Yes)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

def on_getfea_auto2():
    """
    为固定点求解可行域的槽函数
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.init3D:
            if md.auto2Fixed is not None:  # 进针数已经确定
                if md.auto2Pareto is None:  # 且尚未求解可行域和优化
                    # step7:为固定点求解可行域
                    md.auto2Fixed.get_feasibles()
                    # 优化并得到md.auto2Pareto对象
                    moea = MOEA(md.auto2Fixed)  # 根据可行域得到优化变量的范围
                    Phen, ObjV = moea.run()  # step8:使用NSGA-II优化，将优化得到的数据装配到pareto对象
                    #print("====算法主流程结束====")
                    md.auto2Pareto = Auto2Pareto(Phen, ObjV)
                    # 对象显示以及控件初始化
                    md.auto2Fixed.show_fea()
                    md.auto2Pareto.register()
                    md.iren.Initialize()
                    print("结束")

                else:  # 已求解可行域和优化
                    QMessageBox.information(md, "提示", "可行域已计算或上个肿瘤可行域计算结果未清空", QMessageBox.Yes)
            else:  # 进针数还未确定
                QMessageBox.information(md, "提示", "请先确定进针次数！", QMessageBox.Yes)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

def schemes_auto2_change():
    """
    进针方案的下拉框更改
    :return:
    """
    md = gl.get_value('md')
    try:
        # 场景中删除之前所有的针和椭球
        NdlListUtils.remove(2)
        ElliListUtils.remove(2)
        # 选择的帕累托对象的索引
        chosenparindex = md.comboBox_schemes_auto2.currentIndex()

        # 使用帕累托对象，更新所有的固定点
        md.auto2Pareto.pareto[chosenparindex].update_auto2Fixed()
        print("固定点的皮肤交点和靶点更新完成")
        # 在三维窗口中显示
        md.auto2Fixed.regist()
        md.iren.Initialize()
        # Scroller.scroll_all()
        on_comboBox_farobj()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

def on_clear_auto2():
    """
    清空并行规划规划结果的槽函数
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.init3D:
            if md.omega is not None:
                if md.auto2Fixed is None:  # 仅确定了消融次数
                    md.fcom.remove()
                    LineEditUtils.clearall()  # 清空进针数和消融数显示
                    md.iren.Initialize()
                    return
                elif md.auto2Pareto is None:  # 仅确定了消融次数和进针次数
                    pass
                else:  # 全部规划完成
                    md.auto2Fixed.remove_fea()
                    NdlListUtils.remove(2)
                    ElliListUtils.remove(2)

                    md.auto2Pareto.remove()
                md.omega.remove()
                md.omegaCore.remove()
                md.auto2Fixed.remove_subomega()
                md.auto2Fixed = None

                md.centroidsRes = None
            LineEditUtils.clearall()  # 清空进针数和消融数显示
            md.comboBox_schemes_auto2.clear()
            md.iren.Initialize()
            Scroller.scroll_all()
            on_comboBox_farobj()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)