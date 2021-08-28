"""
# @author chrisxu
# @create 2020-08-18 12:59
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl


class ElliListUtils(object):
    """
    md.ellilist的管家类
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def remove(flag):
        md = gl.get_value('md')
        for elliobj in md.ellilist:
            if elliobj.flag == flag:
                md.ren.RemoveActor(elliobj.vtk)
                md.objdic["消融椭球"].remove(elliobj.name)
        for i in range(len(md.ellilist) - 1, -1, -1):
            if md.ellilist[i].flag == flag:
                md.ellilist.remove(md.ellilist[i])

    @staticmethod
    def remove_all():
        md = gl.get_value('md')
        for elliobj in md.ellilist:
            md.ren.RemoveActor(elliobj.vtk)
            md.objdic["消融椭球"].remove(elliobj.name)
        md.ellilist = []
