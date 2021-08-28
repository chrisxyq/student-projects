"""
# @author chrisxu
# @create 2020-08-18 12:53
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl


class NdlListUtils(object):
    """
    md.needlelist的管家类
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def remove(flag):
        """
        删除指定flag类型的针
        :param self:
        :param flag:
        :return:
        """
        md = gl.get_value('md')
        for ndlobj in md.needlelist:
            if ndlobj.flag == flag:
                md.ren.RemoveActor(ndlobj.vtk)
                md.objdic["消融针"].remove(ndlobj.name)
                #print(md.objdic,md.needlelist)

        for i in range(len(md.needlelist) - 1, -1, -1):
            if md.needlelist[i].flag == flag:
                md.needlelist.remove(md.needlelist[i])

    @staticmethod
    def remove_all():
        """
        删除所有类型的针
        :return:
        """
        md = gl.get_value('md')
        # print("删除前的针列表", md.needlelist)
        for ndlobj in md.needlelist:
            # print("删除对象", ndlobj)
            md.ren.RemoveActor(ndlobj.vtk)
            md.objdic["消融针"].remove(ndlobj.name)
        md.needlelist = []
