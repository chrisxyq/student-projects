"""
# @author chrisxu
# @create 2020-08-11 20:35
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import os
import vtk
from vtkplotter import *
import src.GlobalVar as gl


class BaseVTKUtils(object):
    """
    规划软件三维窗口显示的：基础VTK的管家类
    """

    basedic = {"坐标系": []}

    namemap = {'artery': "动脉", 'bone': "骨",
               'gallbladder': "胆囊", 'liver': "肝脏",
               'livertumor': "肝脏肿瘤", 'livertumor1': "肝脏肿瘤1",
               'livertumor2': "肝脏肿瘤2", 'portalvein': "门静脉",
               'skin': "皮肤", 'venoussystem': "静脉系统"}
    c = {namemap['artery']: (165, 42, 42),
         namemap['bone']: (189, 183, 107),
         namemap['gallbladder']: (255, 182, 193),
         namemap['liver']: (255, 160, 122),
         namemap['livertumor']: (105, 105, 105),
         namemap['livertumor1']: (105, 105, 105),
         namemap['livertumor2']: (105, 105, 105),
         namemap['portalvein']: (32, 178, 170),
         namemap['skin']: (255, 255, 255),
         namemap['venoussystem']: (32, 178, 170)}

    alpha = {namemap['artery']: 1, namemap['bone']: 1,
             namemap['gallbladder']: 1, namemap['liver']: 0.3,
             namemap['livertumor']: 0.6, namemap['livertumor1']: 0.6,
             namemap['livertumor2']: 0.6, namemap['portalvein']: 1,
             namemap['skin']: 0.3, namemap['venoussystem']: 1}

    @classmethod
    def change_color(cls, name, color):
        """
        根据传入的name修改对象颜色
        :return:
        """
        md = gl.get_value('md')
        [R, G, B] = color
        if name == "坐标系":
            pass
        elif name == "背景颜色":
            md.ren.SetBackground(R / 255, G / 255, B / 255)
        else:
            actor = cls.basedic[name]
            actor.GetProperty().SetColor(R / 255, G / 255, B / 255)

    @classmethod
    def change_alpha(cls, name):
        """
        根据传入的name修改对象透明度
        :return:
        """
        md = gl.get_value('md')
        alpha = round(md.T_Slider.value() / 100, 2)
        if name == "坐标系" or name == "背景颜色":
            pass
        else:
            actor = cls.basedic[name]
            actor.GetProperty().SetOpacity(alpha)

    @classmethod
    def add_base(cls):
        """
        添加基本的vtk到basedic
        添加基本的vtk到md.ren
        添加基本的vtk到combox
        :return:
        """
        md = gl.get_value('md')
        path = os.path.join(md.rootdir, md.comboBox_patient.currentText(), 'MESHES_VTK')
        vtk_files = os.listdir(path)
        for vtk in vtk_files:
            vtkname = os.path.splitext(vtk)[0]
            actor = load(os.path.join(path, vtkname + ".vtk"))
            # 添加到vtkdict
            cls.basedic[cls.namemap[vtkname]] = actor
            # 显示vtk的颜色必须归一化，而ndl的颜色都可以
            R = cls.c[cls.namemap[vtkname]][0] / 255
            G = cls.c[cls.namemap[vtkname]][1] / 255
            B = cls.c[cls.namemap[vtkname]][2] / 255
            T = cls.alpha[cls.namemap[vtkname]]
            actor.GetProperty().SetColor(R, G, B)
            actor.GetProperty().SetOpacity(T)
            # print(vtkname,"已添加")
            md.objdic["基本对象"].append(cls.namemap[vtkname])

            md.ren.AddActor(actor)
        md.iren.Initialize()

    @classmethod
    def reload_base(cls):
        """
        切换病例时调用
        :return:
        """
        md = gl.get_value('md')
        md.objdic["基本对象"] = []
        cls.add_ax()
        cls.add_plane()
        cls.add_base()
        md.init3D = True
        md.ren.ResetCamera()
        md.iren.Initialize()

    @classmethod
    def reset_base(cls):
        """
        恢复所有的基本对象为默认显示
        坐标系、基本对象、背景
        :return:
        """
        md = gl.get_value('md')
        if md.init3D:
            for name in cls.basedic:
                # " is" 是用来比较 a 和 b 是不是指向同一个内存单元
                # 而"=="是用来比较 a 和 b指向的内存单元中的值是不是相等
                if name == "坐标系":
                    # 坐标系透明度设为1
                    if cls.basedic["坐标系"] == []:
                        cls.add_ax()
                        cls.add_plane()
                else:
                    # 基本三维对象参数设置为默认场景
                    R = cls.c[name][0] / 255
                    G = cls.c[name][1] / 255
                    B = cls.c[name][2] / 255
                    T = cls.alpha[name]
                    actor = cls.basedic[name]
                    actor.GetProperty().SetColor(R, G, B)
                    actor.GetProperty().SetOpacity(T)
            md.ren.SetBackground(0, 0, 0)
            md.iren.Initialize()

    @classmethod
    def del_axplane(cls):
        """
        删除坐标系
        :return:
        """
        md = gl.get_value('md')
        if cls.basedic["坐标系"] != []:
            for actor in cls.basedic["坐标系"]:
                md.ren.RemoveActor(actor)
        cls.basedic["坐标系"] = []
        md.iren.Initialize()

    @classmethod
    def add_ax(cls):
        """
        创建xyz坐标轴
        :return:
        """
        md = gl.get_value('md')
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(100, 100, 100)
        axes.SetShaftType(0)
        axes.SetCylinderRadius(0.02)
        axes.GetXAxisCaptionActor2D().SetWidth(0.02)
        axes.GetYAxisCaptionActor2D().SetWidth(0.02)
        axes.GetZAxisCaptionActor2D().SetWidth(0.02)
        # 添加到vtkdict
        cls.basedic["坐标系"].append(axes)
        md.ren.AddActor(axes)
        style = vtk.vtkInteractorStyleTrackballCamera()
        style.SetDefaultRenderer(md.ren)
        md.iren.SetInteractorStyle(style)

    @classmethod
    def add_plane(cls):
        """
        添加三个平面
        :return:
        """
        md = gl.get_value('md')
        actor = Lines([(50, 0, 0), (50, 50, 0)],
                      [(50, 50, 0), (0, 50, 0)],
                      c=(1, 1, 0), alpha=1, lw=2)
        md.ren.AddActor(actor)
        cls.basedic["坐标系"].append(actor)

        actor = Text('T', pos=[50, 48, 0], s=20, c=(1, 1, 0), justify='top-left')
        actor.orientation([0, 0, 1])
        actor.rotate(180, axis=(0, 0, 1), axis_point=(50, 50, 0), rad=False)
        md.ren.AddActor(actor)
        cls.basedic["坐标系"].append(actor)

        # 添加xZ平面(x横，Z纵)
        actor = Lines([(50, 0, 0), (50, 0, 50)],
                      [(50, 0, 50), (0, 0, 50)],
                      c=(1, 0, 1), alpha=1, lw=2)
        md.ren.AddActor(actor)
        cls.basedic["坐标系"].append(actor)

        actor = Text('C', pos=[50, 0, 50], s=20, c=(1, 0, 1), justify='top-left')
        actor.orientation([0, 1, 0])
        md.ren.AddActor(actor)
        cls.basedic["坐标系"].append(actor)

        # 添加YZ平面(y横，Z纵)
        actor = Lines([(0, 50, 0), (0, 50, 50)],
                      [(0, 50, 50), (0, 0, 50)],
                      c=(0, 1, 1), alpha=1, lw=2)
        md.ren.AddActor(actor)
        cls.basedic["坐标系"].append(actor)

        actor = Text('S', pos=[0, 50, 50], s=20, c=(0, 1, 1), justify='top-left')
        actor.orientation([-1, 0, 0])
        actor.rotate(90, axis=(0, 0, 1), axis_point=(0, 50, 50), rad=False)
        md.ren.AddActor(actor)
        cls.basedic["坐标系"].append(actor)
        # 父combox与子combox的映射关系
        if "坐标系" not in md.objdic["基本对象"]:
            md.objdic["基本对象"].append("坐标系")
        if "背景颜色" not in md.objdic["基本对象"]:
            md.objdic["基本对象"].append("背景颜色")
