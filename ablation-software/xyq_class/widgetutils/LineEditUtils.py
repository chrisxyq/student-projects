"""
# @author chrisxu
# @create 2020-08-26 10:12
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""

import src.GlobalVar as gl


class LineEditUtils():
    """
    Label的工具类
    用于更新整个页面的所有的label
    """

    @staticmethod
    def update_lineEdit_abnum_auto2():
        """
        更新消融次数
        :return:
        """
        md = gl.get_value('md')
        md.lineEdit_abnum_auto2.setText(str(len(md.centroidsRes.centroids)))

    @staticmethod
    def update_lineEdit_pnum_auto2():
        """
        更新进针次数
        :return:
        """
        md = gl.get_value('md')
        md.lineEdit_pnum_auto2.setText(str(len(md.auto2Fixed.fixed)))

    @staticmethod
    def clearall():
        md = gl.get_value('md')
        md.lineEdit_abnum_auto2.setText("")
        md.lineEdit_pnum_auto2.setText("")
        md.lineEdit_abnum_auto2.setEnabled(False)
        md.lineEdit_pnum_auto2.setEnabled(False)
