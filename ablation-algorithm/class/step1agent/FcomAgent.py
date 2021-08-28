"""
# @author chrisxu
# @create 2020-08-21 15:18
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import threading

from singleton.Auto2BaseVtk import Auto2BaseVtk
from singleton.Auto2Para import Auto2Para
from math import degrees, atan, acos

from singleton.LineGetter import LineGetter
from singleton.TimeMe import time_me


class FcomAgent(object):
    """
    规划方法2的求解质心可行域的代理类
    """
    instance = None  # 记录第一个被创建对象的引用
    _instance_lock = threading.Lock()

    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        """
        可被继承的单例模式
        :param args:
        :param kwargs:
        :return:
        """
        if not hasattr(cls, 'instance_dict'):
            FcomAgent.instance_dict = {}

        if str(cls) not in FcomAgent.instance_dict.keys():
            with FcomAgent._instance_lock:
                # print("新建FcomAgent可行域求解的代理类")
                _instance = super().__new__(cls)
                FcomAgent.instance_dict[str(cls)] = _instance

        return FcomAgent.instance_dict[str(cls)]

    def __init__(self):
        if not FcomAgent.init_flag:
            # print("初始化FcomAgent可行域求解的代理类")
            super().__init__()
            FcomAgent.init_flag = True

    def get_del(self):
        """
        求解质心可行域的约束
        :return:
        """
        target = Auto2BaseVtk().tumor.centerOfMass()
        skinpts = Auto2BaseVtk().skin.points()
        # print("皮肤点共有", len(skinpts))
        del_index = []

        for index, skinpt in enumerate(skinpts):
            sph = self.get_spheretf(skinpt, target)
            # 横向/纵向角度约束
            if self.bool_region(sph) == 1:
                del_index.append(index)
            # 避障约束
            elif self.bool_safe(skinpt, target) == 1:
                del_index.append(index)
            elif self.bool_cavity(skinpt, target) == 1:
                del_index.append(index)
        print("删除皮肤点数", len(del_index), "质心可行域点数", len(skinpts) - len(del_index))

        return del_index

    def bool_region(self, sph):
        """
        第一步，区域约束
        输入：皮肤点的球面角度
        不满足则返回1
        :return:
        """
        if Auto2Para().phi[0] > sph[2] or sph[2] > Auto2Para().phi[1] or abs(sph[1] - 90) > Auto2Para().mz or sph[
            0] > 120:
            return 1
        else:
            return 0

    def bool_safe(self, PUN, TAR):
        """
        第二步：避障约束
        使用intersectWithLine检测碰撞
        判断路径与障碍点是否相交
        :param PUN:
        :param TAR:
        :return: 0安全、1相交
        """
        baseVtk = Auto2BaseVtk()
        for ob in baseVtk.ob:
            pts = ob.intersectWithLine(PUN, TAR)
            if len(pts) > 0:
                return 1
        return 0

    def bool_cavity(self, PUN, TAR):
        """
        空腔约束
        """
        liver = Auto2BaseVtk().liver
        intersect = liver.intersectWithLine(PUN, TAR)
        if Auto2Para.index == 2:
            return 0
        else:
            if LineGetter().get_dist(PUN, TAR) / LineGetter().get_dist(intersect[0], TAR) > 3:
                return 1
            else:
                return 0

    def get_spheretf(self, pt, target):
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
#
# if __name__ == '__main__':
#     a=FcomAgent()
#     b=FcomAgent()
#     print(a is b)
#     print([1,2]+[3,4]+[5,6])
