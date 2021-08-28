"""
# @author chrisxu
# @create 2020-08-19 21:13
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from singleton.Auto2Para import Auto2Para
from vtkplotter import *
import os


class Auto2BaseVtk(object):
    """
    单例模式
    用于存储规划方法2的基本环境vtk
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    c_dic = {'artery': (165, 42, 42),
             'bone': (189, 183, 107),
             'gallbladder': (255, 182, 193),
             'liver': (255, 160, 122),
             'portalvein': (32, 178, 170),
             'skin': (255, 255, 255),
             'venoussystem': (32, 178, 170),
             'livertumor1': (105, 105, 105),
             'livertumor2': (105, 105, 105),
             'livertumor5': (105, 105, 105),
             'leftkidney': (255, 160, 122),
             'rightkidney': (255, 160, 122),
             'leftlung': (255, 160, 122),
             'rightlung': (255, 160, 122),
             'spleen': (255, 160, 122)
             }

    alpha_dic = {'artery': 1,
                 'bone': 1,
                 'gallbladder': 1,
                 'liver': 0.8,
                 'portalvein': 1,
                 'skin': 0.3,
                 'venoussystem': 1,
                 'livertumor1': 0.6,
                 'livertumor2': 0.6,
                 'livertumor5': 0.6,
                 'leftkidney': 0.8,
                 'rightkidney': 0.8,
                 'leftlung': 0.8,
                 'rightlung': 0.8,
                 'spleen': 0.8
                 }

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            #print("构造Auto2BaseVtk")
        return cls.instance

    def __init__(self):
        if not Auto2BaseVtk.init_flag:
            #print("初始化Auto2BaseVtk")
            super().__init__()
            self.tumor = None
            self.ob = []
            self.skin = None
            self.liver = None
            self.init_vtk()
            Auto2BaseVtk.init_flag = True


    def init_vtk(self):
        """
        初始化所有的vtk对象
        :return:
        """
        para = Auto2Para()
        head = para.vtkpath
        self.tumor = load(os.path.join(head, para.tmrname + ".vtk"), c=self.c_dic[para.tmrname],
                          alpha=self.alpha_dic[para.tmrname])
        for obname in para.oblist:
            self.ob.append(load(os.path.join(head, obname + ".vtk"), c=self.c_dic[obname],
                                alpha=self.alpha_dic[obname]))
        self.skin = load(os.path.join(head, "skin.vtk"), c=self.c_dic["skin"],
                         alpha=self.alpha_dic["skin"])
        self.liver = load(os.path.join(head, "liver.vtk"), c=self.c_dic["liver"],
                          alpha=self.alpha_dic["liver"])



    def show(self):
        """
        显示对象
        :return:
        """
        basevtklist=[]
        basevtklist.append(self.skin)
        basevtklist.append(self.liver)
        basevtklist.extend(self.ob)
        return basevtklist


    # c_dic = {'artery.vtk': (165, 42, 42),
    #          'bone.vtk': (189, 183, 107),
    #          'gallbladder.vtk': (255, 182, 193),
    #          'liver.vtk': (255, 160, 122),
    #          'portalvein.vtk': (32, 178, 170),
    #          'skin.vtk': (255, 255, 255),
    #          'venoussystem.vtk': (32, 178, 170),
    #          'livertumor1.vtk': (105, 105, 105),
    #          'livertumor2.vtk': (105, 105, 105),
    #          'omega.vtk': (105, 105, 105),
    #          'preTAR.vtk': (105, 105, 105),
    #          'prePUN.vtk': (255, 165, 0),
    #          'elli.vtk': (152, 251, 152)
    #          }
    #
    # alpha_dic = {'artery.vtk': 1,
    #              'bone.vtk': 1,
    #              'gallbladder.vtk': 1,
    #              'liver.vtk': 0.8,
    #              'portalvein.vtk': 1,
    #              'skin.vtk': 0.3,
    #              'venoussystem.vtk': 1,
    #              'livertumor1.vtk': 0.6,
    #              'livertumor2.vtk': 0.6,
    #              'omega.vtk': 0.6,
    #              'preTAR.vtk': 0.6,
    #              'prePUN.vtk': 0.6,
    #              'elli.vtk': 0.7
    #              }
