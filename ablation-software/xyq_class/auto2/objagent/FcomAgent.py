"""
# @author chrisxu
# @create 2020-08-21 15:18
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl
from math import degrees, atan, acos

from objutils.BaseVTKUtils import BaseVTKUtils
from objutils.NeedleUtils import NeedleUtils


class FcomAgent(object):
    """
    规划方法2的求解质心可行域的代理类
    """
    obList_dic = {"3Dircadb1.9livertumor1": ['artery', 'bone', 'gallbladder', 'portalvein', 'venoussystem'],
                  "3Dircadb1.15livertumor1": ['bone', 'portalvein', 'venoussystem'],
                  "3Dircadb1.15livertumor2": ['bone', 'portalvein', 'venoussystem'],
                  "3Dircadb1.16livertumor1": ['bone', 'portalvein', 'venoussystem'],
                  "3Dircadb1.17livertumor1": ['bone', 'portalvein', 'venoussystem'],
                  "3Dircadb1.17livertumor2": ['artery', 'bone', 'portalvein', 'venoussystem']
                  }
    phi_dic = {
        "3Dircadb1.9livertumor1": [180, 300], "3Dircadb1.15livertumor1": [180, 360],
        "3Dircadb1.15livertumor2": [180, 360], "3Dircadb1.16livertumor1": [180, 230],
        "3Dircadb1.17livertumor1": [220, 350], "3Dircadb1.17livertumor2": [180, 290]
    }
    mz = 30

    @classmethod
    def get_del(cls):
        """
        求解质心可行域的约束
        :return:
        """
        md = gl.get_value('md')
        tmrname = md.comboBox_tmrs_auto2.currentText()
        target = BaseVTKUtils.basedic[BaseVTKUtils.namemap[tmrname]].centerOfMass()
        skinpts = BaseVTKUtils.basedic["皮肤"].points()
        # print("皮肤点共有", len(skinpts))
        del_index = []

        for index, skinpt in enumerate(skinpts):
            sph = cls.get_spheretf(skinpt, target)
            # 横向/纵向角度约束
            if cls.bool_region(sph) == 1:
                del_index.append(index)
            # 避障约束
            elif cls.bool_safe(skinpt, target) == 1:
                del_index.append(index)
            elif cls.bool_cavity(skinpt, target) == 1:
                del_index.append(index)
        #print("删除皮肤点数", len(del_index), "质心可行域点数", len(skinpts) - len(del_index))

        return del_index

    @classmethod
    def bool_region(cls, sph):
        """
        第一步，区域约束
        输入：皮肤点的球面角度
        不满足则返回1
        :return:
        """
        md = gl.get_value('md')
        phi = cls.phi_dic[md.comboBox_patient.currentText() + md.comboBox_tmrs_auto2.currentText()]
        if phi[0] > sph[2] or sph[2] > phi[1] or abs(sph[1] - 90) > cls.mz or sph[0] > 120:
            return 1
        else:
            return 0

    @classmethod
    def bool_safe(cls, PUN, TAR):
        """
        第二步：避障约束
        使用intersectWithLine检测碰撞
        判断路径与障碍点是否相交
        :param PUN:
        :param TAR:
        :return: 0安全、1相交
        """
        md = gl.get_value('md')
        obnamelist = cls.obList_dic[md.comboBox_patient.currentText() + md.comboBox_tmrs_auto2.currentText()]
        for obname in obnamelist:
            ob = BaseVTKUtils.basedic[BaseVTKUtils.namemap[obname]]
            pts = ob.intersectWithLine(PUN, TAR)
            if len(pts) > 0:
                return 1
        return 0

    @classmethod
    def bool_cavity(cls, PUN, TAR):
        """
        空腔约束
        """
        md = gl.get_value('md')
        liver = BaseVTKUtils.basedic[BaseVTKUtils.namemap["liver"]]
        intersect = liver.intersectWithLine(PUN, TAR)
        if md.comboBox_patient.currentText() + md.comboBox_tmrs_auto2.currentText() == "3Dircadb1.15livertumor1":
            return 0
        else:
            if NeedleUtils.get_dist(PUN, TAR) / NeedleUtils.get_dist(intersect[0], TAR) > 3:
                return 1
            else:
                return 0

    @classmethod
    def get_spheretf(cls, pt, target):
        """
        功能：直角坐标点(如：皮肤、肿瘤表面、肝脏表面、障碍物表面)
        →→→→→→→→→real球坐标点(θ∈[0, π]， φ∈[0,2π] )
        """
        pt_SPH = [0, 0, 0]
        pt_SPH[0] = ((pt[0] - target[0]) ** 2 + (pt[1] - target[1]) ** 2 + (pt[2] - target[2]) ** 2) ** 0.5
        # 对的，参照arccosx的图像，x在[-1,0]时，y属于[90,180]，x在[0,1]时，y属于[0,90]，这部分相当于确定了上部分/下部分
        pt_SPH[1] = degrees(acos((pt[2] - target[2]) / pt_SPH[0]))
        if pt[0] - target[0] > 0 and pt[1] - target[1] > 0:
            pt_SPH[2] = degrees(atan((pt[1] - target[1]) / (pt[0] - target[0])))
        elif pt[0] - target[0] < 0:  # 第二/第三象限
            pt_SPH[2] = degrees(atan((pt[1] - target[1]) / (pt[0] - target[0]))) + 180
        elif pt[0] - target[0] > 0 and pt[1] - target[1] < 0:  # 第四象限
            # 0823bug:不一定满足这个条件导致角度大于360
            # print(pt[0]-target[0]>0 and pt[1]-target[1]<0)
            pt_SPH[2] = degrees(atan((pt[1] - target[1]) / (pt[0] - target[0]))) + 360
        if pt[0] - target[0] == 0 and pt[1] - target[1] > 0:
            pt_SPH[2] = 90
        if pt[0] - target[0] < 0 and pt[1] - target[1] == 0:
            pt_SPH[2] = 180
        if pt[0] - target[0] == 0 and pt[1] - target[1] < 0:
            pt_SPH[2] = 270
        return pt_SPH
