"""
# @author chrisxu
# @create 2020-08-17 9:01
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
手动规划模块的槽函数
"""
import re

import src.GlobalVar as gl
from objutils.DBUtils import DBUtils
from widgetutils.ComboBoxUtils import ComboBoxUtils

from obj.Elli import Elli
from obj.Needle import Needle
from paint.Paint import Paint, QMessageBox
from scrollct.CtGetter import CtGetter
from scrollct.Scroller import Scroller
from src.ParaSlots import on_comboBox_farobj


def on_mark():
    """
    手动规划入口：标记当前层btn
    :return:
    """
    md = gl.get_value('md')
    if md.init3D:
        try:
            img = CtGetter.getter_ct_forpaint()  # 返回无数据库标记的img
            pat = Paint(img)  # 使用img初始化Paint界面对象
            gl.set_value('pat', pat)
            pat.show()
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_searchlabelled():
    """
    查询已标记病例btn的槽函数
    :return:
    """
    md = gl.get_value('md')
    if md.init3D:
        try:
            # 1.先清空，再addItem
            md.comboBox_labelled_case.clear()
            md.comboBox_targets_hand.clear()
            md.comboBox_inpts_hand.clear()
            tblist = DBUtils.query_marked_table()
            if len(tblist) == 0:
                QMessageBox.information(md, "提示", "当前还没有标记记录!", QMessageBox.Yes)
            else:
                for name in tblist:
                    ComboBoxUtils.add_to_comboBox(name, md.comboBox_labelled_case)
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def labelled_case_change():
    """
    “已标记病例”comboBox下拉框改变的槽函数
    :return:
    """
    md = gl.get_value('md')
    if md.init3D:
        try:
            if md.comboBox_patient.currentText() == md.comboBox_labelled_case.currentText():
                # 1.查询comboBox_labelled_case当前显示的病例的所有tarlist,inlist
                tarlist, inlist = DBUtils.query_marked_points()
                # 2.更新各个comboBox
                md.comboBox_targets_hand.clear()
                md.comboBox_inpts_hand.clear()
                for tarname in tarlist:
                    ComboBoxUtils.add_to_comboBox(tarname, md.comboBox_targets_hand)
                for inname in inlist:
                    ComboBoxUtils.add_to_comboBox(inname, md.comboBox_inpts_hand)
            else:
                QMessageBox.information(md, "提示", "查询病例与当前病例不一致!", QMessageBox.Yes)
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_del_tarin(widget):
    """
    从combox和数据库中删除靶点/进针点
    :return:
    """
    md = gl.get_value('md')
    try:
        if widget.currentText():
            row = re.findall(r"\d+\.?\d*", widget.currentText())
            DBUtils.delete(row)
            widget.removeItem(widget.currentIndex())  # 从本comboBox删除

    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_addto_path():
    """
    将进针路径和椭球加入self.objdic["消融针"]、self.objdic["消融椭球"]：为了加入到comboBox_sonobj
    将进针路径和椭球加入md.needlelist和md.ellilist：为了在三维场景中显示和"清空当前规划进针"
    self.objdic["消融针"]的值为针名
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.comboBox_targets_hand.currentText() and md.comboBox_inpts_hand.currentText():
            needlename=md.comboBox_targets_hand.currentText()+"-"+md.comboBox_inpts_hand.currentText()
            if needlename not in md.objdic["消融针"]:
                newneedle = Needle(0)
                newneedle.register()
                newelli = Elli(0)
                newelli.register()
                Scroller.scroll_all()  # 更新CT页
                on_comboBox_farobj()  # 对象列表
            else:
                QMessageBox.information(md, "提示", "该进针已添加到进针方案！", QMessageBox.Yes)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

