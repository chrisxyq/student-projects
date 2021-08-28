import sys

from PyQt5.QtCore import QVersionNumber, QT_VERSION_STR, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from QCandyUi import CandyWindow

import mainui
from xyq_class.obj.CaseInfo import CaseInfo

sys.path.append("./xyq_class")

from src.Auto1Slots import *
from src.Auto2Slots import on_getabnum_auto2, on_getpnum_auto2, on_getfea_auto2, on_clear_auto2, schemes_auto2_change
from src.HandSlots import *
from src.OpenAndLoad import *
from src.ParaSlots import *
import pydicom
import sqlite3
import matplotlib
from sklearn.cluster import KMeans
import cv2
import vtk
import vtkplotter

# from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainCode(QMainWindow, mainui.Ui_MainWindow, QWidget):
    def __init__(self):
        QMainWindow.__init__(self)
        mainui.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.init_connect()
        self.setMinimumSize(1300, 663)
        self.rootdir = None
        self.caseInfo = CaseInfo()  # 自定义的对象，用于保存病例信息
        self.init_vars()

    def init_vars(self):

        self.image3D = []  # 预加载的三维数组，用于TSC三个层面的显示
        self.init3D = False
        # self.objdic的值为list，list的每个元素为一个自定义类型的对象的对象名，并显示在对象列表中
        self.objdic = {"基本对象": [], "消融针": [], "消融椭球": [], "可行域": [], "帕累托点": []}
        self.needlelist = []  # 用于存储md对象当前拥有的所有的自定义needle类型的对象
        self.ellilist = []  # 用于存储md对象当前拥有的所有的自定义elli类型的对象
        self.fea = None  # 逐针规划的可行域的对象
        self.par = None  # 逐针规划的帕累托解的对象
        # ====并行规划的对象====
        self.omega = None  # 待消融区域
        self.fcom = None  # 质心可行域
        self.centroidsRes = None  # 聚类结果

        self.auto2Fixed = None  # 固定点结果
        self.omegaCore = None  # 核心靶点区域
        self.auto2Pareto = None  # 帕累托列表

    def init_connect(self):
        """------------载入DICOM文件"""
        self.btn_openfile.clicked.connect(on_openfile)
        self.btn_load.clicked.connect(on_load)
        self.Scroll_T.valueChanged.connect(Scroller.scroll_T)
        self.Scroll_S.valueChanged.connect(Scroller.scroll_S)
        self.Scroll_C.valueChanged.connect(Scroller.scroll_C)
        # print(self.label_S.width(), self.label_S.height())
        """------------场景参数设置"""
        self.comboBox_farobj.currentIndexChanged.connect(on_comboBox_farobj)
        self.btn_default_scene.clicked.connect(on_default_scene)  # 恢复默认场景
        self.btn_chosecolor.clicked.connect(on_btn_chosecolor)  # 修改颜色
        self.T_Slider.valueChanged.connect(on_T_Slider)  # 调整透明度
        self.R_Slider.valueChanged.connect(on_R_Slider)  # 调整消融短轴半径
        self.K_Slider.valueChanged.connect(on_K_Slider)  # 调整消融长短轴比
        self.btn_delobj.clicked.connect(on_btn_delobj)  # 删除针对象

        """------------手动规划"""
        self.btn_mark.clicked.connect(on_mark)  # 标记当前层，调用标记窗口
        self.btn_searchlabelled.clicked.connect(on_searchlabelled)  # 查询当前已标记病例
        self.comboBox_labelled_case.activated.connect(labelled_case_change)  # 已标记病例下拉框更改
        self.btn_del_target.clicked.connect(lambda: on_del_tarin(self.comboBox_targets_hand))
        self.btn_del_inpt.clicked.connect(lambda: on_del_tarin(self.comboBox_inpts_hand))  # 删除靶点/进针点
        self.btn_addto_path.clicked.connect(on_addto_path)  # 组合靶点和进针点，加到进针方案
        self.btn_clear_hand.clicked.connect(on_btn_clear_hand)  # 清空手动规划结果
        """------------逐针规划"""
        self.btn_assign_target.clicked.connect(on_assign_target)  # 添加靶点
        self.btn_del_tars_auto1.clicked.connect(on_del_tars_auto1)  # 删除靶点
        self.btn_get_feasible_auto1.clicked.connect(on_get_feasible_auto1)  # 求解可行域
        self.btn_NSGA.clicked.connect(on_NSGA)  # 优化得到帕累托点
        self.btn_chose_pareto.clicked.connect(on_chose_pareto)  # 选择帕累托点，生成进针路径
        self.dist_Slider.valueChanged.connect(on_pareto_Slider)  # 根据到靶点距离筛选帕累托点
        self.angle_Slider.valueChanged.connect(on_pareto_Slider)  # 根据与靶点角度差筛选帕累托点
        self.risk_Slider.valueChanged.connect(on_pareto_Slider)  # 根据风险水平筛选帕累托点
        self.btn_fresh_pareto.clicked.connect(on_fresh_pareto)  # 更新帕累托点显示
        self.btn_clear_auto1.clicked.connect(on_clear_auto1)  # 清空逐针规划的规划结果
        """------------并行规划"""
        self.btn_getabnum_auto2.clicked.connect(on_getabnum_auto2)  # 获得消融次数和聚类结果
        self.btn_getpnum_auto2.clicked.connect(on_getpnum_auto2)  # 获得进针次数/确定的固定点结果/
        self.btn_getfea_auto2.clicked.connect(on_getfea_auto2)  # 为固定点求解可行域并优化得到多种进针方案
        self.comboBox_schemes_auto2.activated.connect(schemes_auto2_change)  # auto2进针方案下拉框更改
        self.btn_clear_auto2.clicked.connect(on_clear_auto2)  # 清空并行规划的规划结果





if __name__ == '__main__':
    gl._init()
    app = QApplication(sys.argv)
    md = MainCode()  # 创建主窗体对象
    gl.set_value('md', md)
    ThreeDUtils.initer()
    md = CandyWindow.createWindow(md, 'blue')
    md.setWindowTitle('计算机辅助热消融手术规划软件')
    md.showFullScreen()
    sys.exit(app.exec_())
