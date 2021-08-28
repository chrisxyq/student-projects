"""
# @author chrisxu
# @create 2020-08-17 16:38
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl


class ObjdicManager(object):
    """
    用于管理md.objdic
    """


    def __init__(self):
        super().__init__()

    @staticmethod
    def add_ndl_elli(ndlname,ellinames):
        """
        一个针名和多个椭球名
        :return:
        """
        md = gl.get_value('md')
        md.objdic["消融针"].append(ndlname)
        md.objdic["消融椭球"].extend(ellinames)
