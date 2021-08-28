"""
# @author chrisxu
# @create 2020-08-16 12:17
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
场景参数模块的槽函数
"""
from PyQt5.QtWidgets import QMessageBox, QColorDialog

import src.GlobalVar as gl
from objutils.BaseVTKUtils import BaseVTKUtils
from widgetutils.ComboBoxUtils import ComboBoxUtils
from scrollct.Scroller import Scroller
from objutils.ElliListUtils import ElliListUtils
from objutils.NdlListUtils import NdlListUtils
from widgetutils.LabelUtils import LabelUtils




def on_btn_clear_hand():
    """
    清空手动规划结果
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.init3D:
            NdlListUtils.remove(0)
            ElliListUtils.remove(0)
            md.iren.Initialize()
            Scroller.scroll_all()
            on_comboBox_farobj()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_btn_delobj():
    """
    在场景中删除针对象
    相应的椭球也被删除
    :return:
    """
    md = gl.get_value('md')
    try:
        objname = md.comboBox_sonobj.currentText()
        farname = md.comboBox_farobj.currentText()
        if objname != "":
            if farname == "消融针":
                for ndlobj in md.needlelist:
                    if ndlobj.name == objname:
                        ndlobj.remove()  # 析构针和相应的椭球对象
                md.iren.Initialize()  # 刷新三维场景
                Scroller.scroll_all()  # 刷新CT窗口
                on_comboBox_farobj()  # 刷新下拉框
            elif objname == "坐标系":
                BaseVTKUtils.del_axplane()
            else:
                QMessageBox.information(md, "提示", "对象不支持删除", QMessageBox.Yes)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_K_Slider():
    """
    # 调整消融长短轴比
    :return:
    """
    md = gl.get_value('md')
    name = md.comboBox_sonobj.currentText()

    LabelUtils.update_label_KNOW()
    if name != "":
        try:
            farname = md.comboBox_farobj.currentText()
            if farname == "消融椭球":
                for elliobj in md.ellilist:
                    if elliobj.name == name:
                        elliobj.update_K()
                md.iren.Initialize()
            else:
                QMessageBox.information(md, "提示", "调整对象类型需为消融椭球", QMessageBox.Yes)
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_R_Slider():
    """
    调整消融短轴半径
    :return:
    """
    md = gl.get_value('md')
    name = md.comboBox_sonobj.currentText()
    LabelUtils.update_label_RNOW()
    if name != "":
        try:
            farname = md.comboBox_farobj.currentText()
            if farname == "消融椭球":
                for elliobj in md.ellilist:
                    if elliobj.name == name:
                        elliobj.update_R()
                md.iren.Initialize()
            else:
                QMessageBox.information(md, "提示", "调整对象类型需为消融椭球", QMessageBox.Yes)
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_T_Slider():
    """
    调整透明度
    :return:
    """
    md = gl.get_value('md')
    name = md.comboBox_sonobj.currentText()
    LabelUtils.update_label_TNOW()
    if name != "":
        try:
            farname = md.comboBox_farobj.currentText()
            if farname == "基本对象":
                BaseVTKUtils.change_alpha(name)
            elif farname == "消融椭球":
                for elliobj in md.ellilist:
                    if elliobj.name == name:
                        elliobj.change_alpha()
            elif farname == "可行域":
                md.fea.change_alpha(name)
                if md.fea.alpha == 0:
                    Scroller.scroll_all()
            elif farname == "帕累托点":
                md.par.change_alpha()
                if md.par.alpha == 0:
                    Scroller.scroll_all()
            else:
                QMessageBox.information(md, "提示", "对象透明度暂不支持修改", QMessageBox.Yes)

            md.iren.Initialize()

        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_btn_chosecolor():
    """
    修改对象列表的对象颜色
    调用调色板
    :return:
    """

    def get_color():
        """
        调用调色板,返回颜色
        16进制颜色代码转rgb
        :return:
        """
        col = QColorDialog.getColor()  # 16进制颜色代码
        hex = col.name()
        r = int(hex[1:3], 16)
        g = int(hex[3:5], 16)
        b = int(hex[5:7], 16)
        return [r, g, b]

    md = gl.get_value('md')
    name = md.comboBox_sonobj.currentText()
    if name != "":
        try:
            farname = md.comboBox_farobj.currentText()
            if farname == "基本对象" and name != "坐标系":
                color = get_color()  # 返回的是255颜色
                BaseVTKUtils.change_color(name, color)
            elif farname == "消融针":
                # 消融针和椭球的颜色绑定修改
                color = get_color()  # 返回的是255颜色
                for ndlobj in md.needlelist:
                    if ndlobj.name == name:
                        ndlobj.change_color(color)
            else:
                QMessageBox.information(md, "提示", "对象颜色暂不支持修改", QMessageBox.Yes)
            md.iren.Initialize()
            Scroller.scroll_all()
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_comboBox_farobj():
    """
    当父对象类型下拉框改变时，更改子对象类型下拉框的内容
    :return:
    """
    md = gl.get_value('md')
    try:
        ComboBoxUtils.update_comboBox_sonobj()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_default_scene():
    """
    恢复默认的基本场景
    baseVTKUtils.basedic里的所有对象恢复原样
    :return:
    """
    md = gl.get_value('md')
    try:
        BaseVTKUtils.reset_base()
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)
