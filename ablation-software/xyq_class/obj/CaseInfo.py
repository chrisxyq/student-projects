"""
# @author chrisxu
# @create 2020-08-13 22:22
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import pydicom

import src.GlobalVar as gl
import os


class CaseInfo(object):
    """
    病例的信息
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not CaseInfo.init_flag:
            super().__init__()
            self.ps = None  # 像素间距
            self.st = None  # 层厚
            self.len = None  # 图像数目
            self.name = None  # 病例名
            self.image3D = []
            CaseInfo.init_flag = True

    def get_value(self):
        """
        获取病例的信息
        :return:
        """
        md = gl.get_value('md')
        # try:
        filePath = os.path.join(md.rootdir, md.comboBox_patient.currentText(), 'PATIENT_DICOM')
        dcm_files = os.listdir(filePath)
        dcm_tag = pydicom.read_file(os.path.join(filePath, dcm_files[0]))
        self.ps = dcm_tag.PixelSpacing[0]  # 像素间距
        self.st = dcm_tag.SliceThickness  # 层厚
        self.len = len(dcm_files)  # 图像数目
        self.name = md.comboBox_patient.currentText()
        self.get_image3D()
        # except Exception as res:
        #     QMessageBox.information(md, "提示", str(res), QMessageBox.Yes)

    def get_image3D(self):
        """
        获得加窗前的所有的dicom图像的三维矩阵
        :return:
        """
        md = gl.get_value('md')
        self.image3D = []
        path = os.path.join(md.rootdir,
                            md.comboBox_patient.currentText(), 'PATIENT_DICOM')
        for i in range(self.len):
            rdpath = os.path.join(path, 'image_' + str(i) + '.dcm')
            readDCM = pydicom.read_file(rdpath)  # 是dicom的各个标签
            # print(readDCM)
            img = self.rescale_trans(readDCM)  # 512*512的-1024矩阵，等于readDCM.pixel_array
            self.image3D.append(img)  # RdImage即为所有dicom图像的像素矩阵，为层数*(512*dicom.x)*(512*dicom.x)

    def rescale_trans(self, ds):
        """
        输入：pydicom.read_file(rdpath)  # 是dicom的各个标签
        :param ds:
        :return: 512*512的-1024矩阵
        """
        rescale_intercept = ds.RescaleIntercept
        rescale_slope = ds.RescaleSlope
        img = ds.pixel_array
        # print("ds.pixel_array", ds.pixel_array.shape)
        img = img * rescale_slope + rescale_intercept
        # print("rescale_slope", rescale_slope)
        # print("rescale_intercept", rescale_intercept)
        return img
