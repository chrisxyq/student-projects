"""
# @author chrisxu
# @create 2020-08-14 9:10
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import cv2

import numpy as np
import src.GlobalVar as gl


class CtGetter(object):
    """
    根据md.Scroll_T.value()
    获取加窗后的CT图：三个切面
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def getter_ct(flag):
        """
        返回初始的无标记点的img图像给TSC三个面
        :return:
        """
        md = gl.get_value('md')
        if flag == "T":
            img = np.array(md.caseInfo.image3D)[md.Scroll_T.value(), :, :]
        elif flag == "S":
            img = np.array(md.caseInfo.image3D)[:, :, md.Scroll_S.value()]
        else:
            img = np.array(md.caseInfo.image3D)[:, md.Scroll_C.value(), :]
        img = CtGetter.window_trans(img, 40, 200, [0, 255])  # 加窗，使dicom图像更清晰
        # print("加窗后", img.shape)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    @staticmethod
    def marker_all_ct(img, flag):
        """
        将所有针\可行域、帕累托点在CT上的投影点绘制到CT上
        :param img:
        :param flag:
        :return:
        """
        img = CtGetter.marker_ndl_ct(img, flag)
        img = CtGetter.marker_fea_ct(img, flag)
        img = CtGetter.marker_par_ct(img, flag)
        return img

    @staticmethod
    def marker_par_ct(img, flag):
        """
        将所有帕累托点在CT上的投影点绘制到CT上
        :param img:
        :param flag:
        :return:
        """
        md = gl.get_value('md')
        if md.par is not None and md.par.alpha != 0:
            if flag == "T":
                #print("md.par.Tnum_to_ctpts",md.par.Tnum_to_ctpts)
                if md.Scroll_T.value() in md.par.Tnum_to_ctpts:
                    for ctpt in md.par.Tnum_to_ctpts[md.Scroll_T.value()]:
                        #print(ctpt[0], ctpt[1])
                        cv2.circle(img, (ctpt[0], ctpt[1]), 4, md.par.color, -1)
            elif flag == "S":
                if md.Scroll_S.value() in md.par.Snum_to_ctpts:
                    for ctpt in md.par.Snum_to_ctpts[md.Scroll_S.value()]:
                        cv2.circle(img, (ctpt[0], ctpt[1]), 4, md.par.color, -1)
            else:
                if md.Scroll_C.value() in md.par.Cnum_to_ctpts:
                    for ctpt in md.par.Cnum_to_ctpts[md.Scroll_C.value()]:
                        cv2.circle(img, (ctpt[0], ctpt[1]), 4, md.par.color, -1)
        return img

    @staticmethod
    def marker_fea_ct(img, flag):
        """
        将所有可行域在CT上的投影点绘制到CT上
        :param img:
        :param flag:
        :return:
        """
        md = gl.get_value('md')
        if md.fea is not None:
            if flag == "T":
                if md.Scroll_T.value() in md.fea.Tnum_to_ctpts:
                    for index, indexthfeactpts in enumerate(md.fea.Tnum_to_ctpts[md.Scroll_T.value()]):
                        if md.fea.alpha[index] != 0:
                            for indexthfeactpt in indexthfeactpts:
                                cv2.circle(img, (indexthfeactpt[0], indexthfeactpt[1]), 2, md.fea.color[index], -1)
            elif flag == "S":
                if md.Scroll_S.value() in md.fea.Snum_to_ctpts:
                    for index, indexthfeactpts in enumerate(md.fea.Snum_to_ctpts[md.Scroll_S.value()]):
                        if md.fea.alpha[index] != 0:
                            for indexthfeactpt in indexthfeactpts:
                                cv2.circle(img, (indexthfeactpt[0], indexthfeactpt[1]), 2, md.fea.color[index], -1)
            else:
                if md.Scroll_C.value() in md.fea.Cnum_to_ctpts:
                    for index, indexthfeactpts in enumerate(md.fea.Cnum_to_ctpts[md.Scroll_C.value()]):
                        if md.fea.alpha[index] != 0:
                            for indexthfeactpt in indexthfeactpts:
                                cv2.circle(img, (indexthfeactpt[0], indexthfeactpt[1]), 2, md.fea.color[index], -1)

        return img

    @staticmethod
    def marker_ndl_ct(img, flag):
        """
        将所有针在CT上的投影点绘制到CT上
        :return:
        """
        md = gl.get_value('md')
        if len(md.needlelist) > 0:
            if flag == "T":
                for needle in md.needlelist:
                    if md.Scroll_T.value() in needle.Tnum_to_ctpts:
                        for point in needle.Tnum_to_ctpts[md.Scroll_T.value()]:
                            cv2.circle(img, (point[0], point[1]), 3, needle.color, -1)
            elif flag == "S":
                for needle in md.needlelist:
                    if md.Scroll_S.value() in needle.Snum_to_ctpts:
                        for point in needle.Snum_to_ctpts[md.Scroll_S.value()]:
                            cv2.circle(img, (point[0], point[1]), 3, needle.color, -1)
            else:
                for needle in md.needlelist:
                    if md.Scroll_C.value() in needle.Cnum_to_ctpts:
                        for point in needle.Cnum_to_ctpts[md.Scroll_C.value()]:
                            cv2.circle(img, (point[0], point[1]), 3, needle.color, -1)

        return img

    @staticmethod
    def getter_ct_forpaint():
        """
        返回初始的无标记点的img图像给paint面
        :return:
        """
        md = gl.get_value('md')
        img = np.array(md.caseInfo.image3D)[md.Scroll_T.value(), :, :]
        img = CtGetter.window_trans(img, 40, 200, [0, 255])  # 加窗，使dicom图像更清晰
        # print("加窗后", img.shape)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


    @staticmethod
    def window_trans(img, window_center, window_width, range):
        """
        加窗，使dicom图像更清晰
        :param img: numpy array,图像灰度矩阵
        :param window_center: dicom文件中定义的window_center
        :param window_width: dicom文件中定义的window_width
        :param range: [min,max],灰度范围
        :return: 处理后的图像灰度矩阵
        """

        try:
            window_min = window_center - 0.5 - (window_width - 1) / 2
            window_max = window_center - 0.5 + (window_width - 1) / 2
        except Exception:
            window_center = window_center[0]
            window_width = window_width[0]
            window_min = window_center - 0.5 - (window_width - 1) / 2
            window_max = window_center - 0.5 + (window_width - 1) / 2
        ymin = range[0]
        ymax = range[1]

        def trans(x):
            if x <= window_min:
                return ymin
            elif x > window_max:
                return ymax
            else:
                return ((x - (window_center - 0.5)) / (window_width - 1) + 0.5) * (ymax - ymin) + ymin

        return np.array(list(map(trans, img.ravel())), np.uint8).reshape(img.shape)