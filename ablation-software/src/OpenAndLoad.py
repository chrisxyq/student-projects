"""
# @author chrisxu
# @create 2020-08-13 16:46
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import src.GlobalVar as gl
from widgetutils.ComboBoxUtils import ComboBoxUtils
from widgetutils.LineEditUtils import LineEditUtils
from widgetutils.SliderUtils import SliderUtils
from widgetutils.ThreeDUtils import ThreeDUtils
from scrollct.Scroller import Scroller
from src.ParaSlots import on_comboBox_farobj
import os


def on_openfile():
    """
    btn_openfile"打开"的槽函数
    :return:
    """
    md = gl.get_value('md')

    def get_file_names(foldername):
        """
        :param foldername:
        :return: root   str   根目录
                dirs    list  包含的文件夹
                files   list  包含的文件
        """
        for root, dirs, files in os.walk(foldername):
            return root, dirs, files

    try:
        dir = QFileDialog.getExistingDirectory(md, "请选取病例DICOM图像所在文件夹", r'E:\thesis_task\thesis_software')
        # dir = QFileDialog.getExistingDirectory(md, "请选取病例DICOM图像所在文件夹", os.getcwd())
        if dir != "":  # 按"取消"则返回空
            md.rootdir = dir
            # print(md.rootdir)
            _, md.dirs, _ = get_file_names(dir)
            # ========重新加载病例，需要先清空combox========
            ComboBoxUtils.clear_all_comboBox()
            md.comboBox_patient.clear()  # 更新comboBox_patient病例名列表
            md.comboBox_patient.addItems(md.dirs)
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


def on_load():
    """
    btn_load"载入"按键的槽函数
    :return:
    """
    md = gl.get_value('md')
    try:
        if md.rootdir:
            ComboBoxUtils.clear_all_comboBox()
            LineEditUtils.clearall()
            # 由于病例重新加载了，需要为md.caseInfo的image3D等属性重新赋值
            md.caseInfo.get_value()
            md.init_vars()

            SliderUtils.reset_auto1_slider()  # 初始化帕累托点滑条

            # print(md.label_S.width(),md.label_S.height())
            ThreeDUtils.init_3D()
            Scroller.scroll_locater()  # 将scroll定位到中间
            Scroller.scroll_all()  # 更新CT窗口显示
            ComboBoxUtils.init_comboBox_farobj()  # 初始化场景对象管理下拉框
            on_comboBox_farobj()  # 当切换病例时，上一句将不起作用，使用这一句强行刷新下拉框
            ComboBoxUtils.init_comboBox_tmrs_auto2()  # 初始化并行规划的规划对象下拉框
    except Exception as res:
        QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


