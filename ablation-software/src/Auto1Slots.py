"""
# @author chrisxu
# @create 2020-08-18 14:01
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
逐针规划模块的所有槽函数
"""
import src.GlobalVar as gl
from obj.Elli import Elli
from obj.Fea import Fea
from obj.Needle import Needle
from obj.Par import Par
from objutils.ElliListUtils import ElliListUtils
from objutils.NdlListUtils import NdlListUtils
from paint.Paint import QMessageBox
from scrollct.Scroller import Scroller
from src.ParaSlots import on_comboBox_farobj

from widgetutils.ComboBoxUtils import ComboBoxUtils
from widgetutils.LabelUtils import LabelUtils
from widgetutils.SliderUtils import SliderUtils


def on_clear_auto1():
    """
    删除auto1规划场景
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.init3D:
            NdlListUtils.remove(1)
            ElliListUtils.remove(1)
            if md.fea is not None:
                md.fea.remove()
            if md.par is not None:
                md.par.remove()

            SliderUtils.reset_auto1_slider()
            ComboBoxUtils.clear_comboBox_auto1()
            md.iren.Initialize()
            Scroller.scroll_all()
            on_comboBox_farobj()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_fresh_pareto():
    """
    根据风险水平/靶点角度差/到靶点距离筛选帕累托点
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.par is not None:
            md.ren.RemoveActor(md.par.vtk)
            md.par.update()
            md.iren.Initialize()
            Scroller.scroll_all()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

def on_pareto_Slider():
    """
    实时更新slider的label标签值
    dist/angle/risk
    :return:
    """
    md = gl.get_value('md')
    try:
        LabelUtils.update_pareto_label_by_slider()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)



def on_chose_pareto():
    """
    由靶点和帕累托点组成进针方案
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.comboBox_targets_auto1.currentText() and md.comboBox_pareto_auto1.currentText():
            needlename = md.comboBox_targets_auto1.currentText() + "-" + md.comboBox_pareto_auto1.currentText()
            if needlename not in md.objdic["消融针"]:
                newneedle = Needle(1)
                newneedle.register()
                newelli = Elli(1)
                newelli.register()
                Scroller.scroll_all()  # 更新CT页
                on_comboBox_farobj()  # 对象列表
            else:
                QMessageBox.information(md, "提示", "该进针已添加到进针方案！", QMessageBox.Yes)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_NSGA():
    """
    创建帕累托对象
    并初始化帕累托滑条的值
    :return:
    """
    md = gl.get_value('md')
    try:
        tarname = md.comboBox_targets_auto1.currentText()
        if tarname:
            if md.fea is not None:  # 只有该靶点的可行域已经计算才继续
                if md.fea.tarname == tarname:
                    if md.par is not None:
                        if md.par.tarname == tarname:  # 帕累托对象存在，且属于当前规划对象
                            QMessageBox.information(md, "提示", "该靶点的帕累托点已经计算", QMessageBox.Yes)
                            return
                        else:  # 帕累托对象存在，但不属于当前规划对象
                            md.par.remove()
                    # 计算得到帕累托对象
                    Par(tarname).register()
                    on_comboBox_farobj()
                    md.iren.Initialize()
                    Scroller.scroll_all()
                else:
                    QMessageBox.information(md, "提示", "优化前需重新计算可行域！", QMessageBox.Yes)
            else:
                QMessageBox.information(md, "提示", "优化前需计算可行域！", QMessageBox.Yes)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

def on_get_feasible_auto1():
    """
    创建fea对象
    :return:
    """
    md = gl.get_value('md')
    try:
        tarname = md.comboBox_targets_auto1.currentText()
        if tarname:
            if md.fea is not None and md.fea.tarname == tarname:
                QMessageBox.information(md, "提示", "该靶点的可行域已经计算", QMessageBox.Yes)
            else:
                Fea(tarname).register()  # 创建fea对象，并且注册到md.objdic["可行域"]和md.fea
                on_comboBox_farobj()
                md.iren.Initialize()
                Scroller.scroll_all()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_del_tars_auto1():
    """
    删除靶点列表当前靶点
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.comboBox_targets_auto1.currentText():
            md.comboBox_targets_auto1.removeItem(md.comboBox_targets_auto1.currentIndex())
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_assign_target():
    """
    手动标记靶点
    :return:
    """
    md = gl.get_value('md')
    try:
        ComboBoxUtils.addTarToCombox()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

