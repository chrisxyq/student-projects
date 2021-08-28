"""
# @author chrisxu
# @create 2020-08-14 9:48
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from PyQt5.QtWidgets import QMessageBox

import src.GlobalVar as gl
from scrollct.CtGetter import CtGetter
from agent.CvToQtAgent import CvToQtAgent


class Scroller(object):
    """
    scroll时候的槽函数
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def scroll_T():
        """
        scroll时候的槽函数,得到T面加窗后的CT图
        :return:
        """
        md = gl.get_value('md')
        try:
            if md.init3D:
                imgT = CtGetter.getter_ct("T")
                imgT = CtGetter.marker_all_ct(imgT, "T")

                imgT = CvToQtAgent.cvtoqt(imgT)
                md.label_T.setPixmap(imgT)  # 获得图片后更新显示在label
                md.label_T.setScaledContents(False)  # 图片自适应label大小

                pageT = str(md.Scroll_T.value()) + "/" + str(md.caseInfo.len - 1)
                md.Page_T.setText(pageT)  # 更新页码
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)


    @staticmethod
    def scroll_S():
        """
        scroll时候的槽函数,得到S面加窗后的CT图
        :return:
        """
        md = gl.get_value('md')
        try:
            if md.init3D:
                imgS = CtGetter.getter_ct("S")
                imgS = CtGetter.marker_all_ct(imgS, "S")

                imgS = CvToQtAgent.cvtoqt(imgS)
                md.label_S.setPixmap(imgS)  # 获得图片后更新显示在label
                md.label_S.setScaledContents(False)  # 图片自适应label大小

                pageS = str(md.Scroll_S.value()) + "/511"
                md.Page_S.setText(pageS)  # 更新页码
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

    @staticmethod
    def scroll_C():
        """
        scroll时候的槽函数,得到C面加窗后的CT图
        :return:
        """
        md = gl.get_value('md')
        try:
            if md.init3D:
                imgC = CtGetter.getter_ct("C")  # 加载更新图像
                imgC = CtGetter.marker_all_ct(imgC, "C")

                imgC = CvToQtAgent.cvtoqt(imgC)
                md.label_C.setPixmap(imgC)  # 获得图片后更新显示在label
                md.label_C.setScaledContents(False)  # 图片自适应label大小

                pageC = str(md.Scroll_C.value()) + "/511"
                md.Page_C.setText(pageC)  # 更新页码
        except Exception as res:
            QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)
    @staticmethod
    def scroll_all():
        """
        刷新页面
        :return:
        """
        Scroller.scroll_T()
        Scroller.scroll_S()
        Scroller.scroll_C()

    @staticmethod
    def scroll_locater():
        """
        初始定位到中心
        :return:
        """
        md = gl.get_value('md')
        TMAX, SMAX, CMAX = md.caseInfo.len - 1, 511, 511
        TINI, SINI, CINI = TMAX // 2, SMAX // 2, CMAX // 2

        md.Scroll_T.setMaximum(TMAX)  # 设置滚动条最大值
        md.Scroll_T.setValue(TINI)  # 把Scroll_png滚动条定位为中间
        md.Scroll_T.setEnabled(True)

        md.Scroll_S.setMaximum(SMAX)  # 设置滚动条最大值
        md.Scroll_S.setValue(SINI)  # 把Scroll_png滚动条定位为中间
        md.Scroll_S.setEnabled(True)

        md.Scroll_C.setMaximum(CMAX)  # 设置滚动条最大值
        md.Scroll_C.setValue(CINI)  # 把Scroll_png滚动条定位为中间
        md.Scroll_C.setEnabled(True)
