# ---------------------画图子窗口的类----------------------------------
import copy

from PyQt5.QtWidgets import *
import src.GlobalVar as gl
from objutils.DBUtils import DBUtils
from paint.PaintUi import Ui_Form


import cv2

from agent.CvToQtAgent import CvToQtAgent


class Paint(QMainWindow, Ui_Form):
    """
    画图子界面和槽函数
    """

    def __init__(self, img):
        super(Paint, self).__init__()
        self.setupUi(self)
        self.baseimg = img
        self.pixmap = None  # 初始化为该图片最新标记结果

        self.init_vars()
        self.init_connect()
        self.init_pixmap()

    def init_vars(self):
        """
        初始化paint的属性
        :return:
        """
        # ------------------------------参数----------------------------------
        self.setFixedSize(522, 592)
        md = gl.get_value('md')
        self.page_png.setText(md.Page_T.text())  # 页码和主窗口保持一致
        self.pixel_x = -1
        self.pixel_y = -1
        self.kind = -1
        self.txt = None  # 进针点/靶点的标号，保存在数据库中
        self.paint_list = []
        self.undo_list = []
        self.pre_isclear = 0

    def init_connect(self):
        self.comboBox_target.activated.connect(lambda: self.ptchange(0))
        self.comboBox_skin.activated.connect(lambda: self.ptchange(1))
        self.btn_clear.clicked.connect(self.on_clear)
        self.btn_undo.clicked.connect(self.on_undo)
        self.btn_redo.clicked.connect(self.on_redo)

    def init_pixmap(self):
        """
        初始化pixmap
        使用self.baseimg的原因是为了快速获取无数据库标记的img
        节省耗时
        mycopy是为了不让方法修改self.baseimg
        :return:
        """

        def draw_img(dao, img):
            """
            根据数据库的数据，依次绘制pat.img
            dao的每个元素为row
            row的每个元素为kind,num , X , Y
            :param dao:list(row)
            :return:
            """
            for row in dao:
                point_color = (0, 255, 0) if row[0] == 0 else (255, 0, 0)
                cv2.circle(img, (row[2], row[3]), 2, point_color, -1)
                if row[1] != '0':
                    # 输入图像、添加文字、左上角坐标、字体类型、字体大小、文字颜色、字体粗细
                    cv2.putText(img, row[1], (row[2] - 6, row[3] - 6), cv2.FONT_HERSHEY_PLAIN, 1.0, point_color, 1)
            return img
        # 从数据库中获取dao数据
        dao = DBUtils.query_points_from_slice()
        # 使用dao数据和img初始化self.img和self.pixmap
        mycopy = copy.deepcopy(self.baseimg)
        img = draw_img(dao, mycopy)
        self.pixmap = CvToQtAgent.cvtoqt(img)
        self.label_png.setPixmap(self.pixmap)  # 把图片贴上，再显示
        self.label_png.setScaledContents(True)

    def on_clear(self):
        """
        btn_clear清除该页标记的槽函数
        :return:
        """
        try:
            DBUtils.del_points_from_slice()
            # 2.将label_png.setPixmap设置为主窗口的对应图片md.img
            self.pixmap = CvToQtAgent.cvtoqt(self.baseimg)
            self.label_png.setPixmap(self.pixmap)  # 把图片贴上，再显示
            self.label_png.setScaledContents(True)
            self.kind = -1  # 要再按标记下拉框才能继续标记
        except Exception as res:
            QMessageBox.information(self, "提示", str(res), QMessageBox.Yes)

    def ptchange(self, kind):
        """
        标记靶点和进针点的comboBox的槽函数
        功能：
        主要是根据comboBox确定点的类型参数，和初始化鼠标位置
        :param kind:0为靶点、1为进针点
        :return:
        """
        try:
            # 每次重新选择comboBox之后，记得再次初始化鼠标位置，防止直接把上次保存的点给画出来
            self.pixel_x, self.pixel_y = -1, -1
            self.kind = kind  # 初始化赋值绘制点的类型，0为靶点、1为进针点，-1为不画
        except Exception as res:
            QMessageBox.information(self, "提示", str(res), QMessageBox.Yes)

    def on_undo(self):
        """
        撤销操作
        :return:
        """
        try:
            #print('操作列表和撤销列表', len(self.paint_list), len(self.undo_list))
            # md = gl.get_value('md')
            if len(self.paint_list) > 0:
                DBUtils.del_lastone()  # 更新数据库database.delete(self.paint_list[-1])
                self.undo_list.append(self.paint_list.pop(-1))  # 更新paint_list和undo_list
                self.init_pixmap()  # 更新画图板
        except Exception as res:
            QMessageBox.information(self, "提示", str(res), QMessageBox.Yes)

    def on_redo(self):
        """
        重做操作
        :return:
        """
        try:
            #print('操作列表和撤销列表', len(self.paint_list), len(self.undo_list))
            if len(self.undo_list) > 0:
                self.paint_list.append(self.undo_list.pop(-1))  # 更新paint_list和undo_list
                DBUtils.insert(self.paint_list[-1])  # 更新数据库datdbase.write(self.paint_list[-1])
                self.init_pixmap()  # 更新画图板 opencv.draw(paint_list[-1])
        except Exception as res:
            QMessageBox.information(self, "提示", str(res), QMessageBox.Yes)

    def mousePressEvent(self, mouseEvent):
        '''
        鼠标按下事件：
        当self.kind=0或者1的时候，记录按下时候的点的坐标
        '''
        try:
            if self.kind == -1:
                QMessageBox.information(self, "提示", "请先在标记下拉框选择标记点类型。", QMessageBox.Yes)
            else:
                # 当self.kind=0或者1的时候，即当combox被按下之后才能记录鼠标点击的位置
                self.pixel_x = mouseEvent.x()
                self.pixel_y = mouseEvent.y()
                self.txt = self.comboBox_target.currentText() if self.kind == 0 else self.comboBox_skin.currentText()
        except Exception as res:
            QMessageBox.information(self, "提示", str(res), QMessageBox.Yes)

    def mouseReleaseEvent(self, mouseEvent):
        '''
        鼠标释放事件：画图！！！！！
        0709防止重复画图
        功能：仅在鼠标释放时候画点→保存标记图片到md.labelledselfh→保存到数据库！
        →→→→→→仅在鼠标释放时候画点→保存标记图片到md.labelledselfh→保存到数据库！
        如此循环
        '''
        try:
            if self.kind != -1:
                if self.txt == "不带标记":
                    self.txt = 0
                row = [self.kind, self.txt, self.pixel_x, self.pixel_y]
                DBUtils.insert(row)
                self.paint_list.append(row)
                self.init_pixmap()  # 更新画图板
        except Exception as res:
            QMessageBox.information(self, "提示", str(res), QMessageBox.Yes)
