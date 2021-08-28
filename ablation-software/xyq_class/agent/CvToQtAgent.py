"""
# @author chrisxu
# @create 2020-08-13 16:48
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from PyQt5.QtGui import QImage, QPixmap
import src.GlobalVar as gl


class CvToQtAgent(object):
    @staticmethod
    def cvtoqt(img):
        """
        opencv图像转成Qimage图像
        :param img:
        :return:
        """
        md = gl.get_value('md')
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        img = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # print(md.label_S.width(), md.label_S.height())
        scale = min(md.label_S.width(), md.label_S.height())
        if height == 512:
            newimg = QPixmap.fromImage(img).scaled(scale, scale)
        else:
            # 比例因子：层厚*层数/512*像素尺寸
            newimg = QPixmap.fromImage(img).scaled(scale, scale * md.caseInfo.st * md.caseInfo.len / (512 * md.caseInfo.ps))

        return newimg










