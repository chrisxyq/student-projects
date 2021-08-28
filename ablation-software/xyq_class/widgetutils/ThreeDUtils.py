"""
# @author chrisxu
# @create 2020-08-15 10:03
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import vtk
import src.GlobalVar as gl
from objutils.BaseVTKUtils import BaseVTKUtils
from objutils.ElliListUtils import ElliListUtils
from objutils.NdlListUtils import NdlListUtils


class ThreeDUtils():
    """
    3D窗口的工具类
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def initer():
        """
        初始化3D窗口
        :return:
        """
        md = gl.get_value('md')
        md.ren = vtk.vtkRenderer()
        md.ren.SetBackground(0, 0, 0)
        md.vtkWidget.GetRenderWindow().AddRenderer(md.ren)
        md.iren = md.vtkWidget.GetRenderWindow().GetInteractor()
        md.iren.Initialize()


    @staticmethod
    def init_3D():
        """
        切换病例时使用
        为3D场景加上基本显示对象
        :return:
        """
        md = gl.get_value('md')

        NdlListUtils.remove_all()  # 注销场景中规划的所有的针和椭球
        ElliListUtils.remove_all()
        #print("md.needlelist", md.needlelist, "md.ellilist", md.ellilist)
        # print("md.par", md.par, "md.fea", md.fea)
        if md.par is not None:
            md.par.remove()
        if md.fea is not None:
            md.fea.remove()

        ThreeDUtils.initer()
        BaseVTKUtils.reload_base()


