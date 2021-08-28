"""
# @author chrisxu
# @create 2020-08-21 9:25
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from vtkplotter import Point, show

from singleton.Auto2BaseVtk import Auto2BaseVtk
from singleton.ObjToString import obj_to_string
from singleton.TimeMe import time_me
from step1.Fcom import Fcom
from step1.Omega import Omega
from step1agent.CentroidsResAgent import CentroidsResAgent


class CentroidsRes(object):
    """
    规划方法2的聚类结果类
    """
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造ClusterRes聚类结果")
        return cls.instance

    def __init__(self):
        """
        传入omega对象作为属性
        以初始化聚类数目self.num
        :param omega:
        """
        if not CentroidsRes.init_flag:
            # print("初始化ClusterRes聚类结果")
            super().__init__()
            self.num = 0  # 聚类数目
            self.centroids = []  # 聚类中心对象

            CentroidsRes.init_flag = True

    def __str__(self):
        return obj_to_string(CentroidsRes, self)

    def clear(self):
        """
        在迭代聚类结果时候
        清除对象
        :return:
        """
        self.centroids = []

    @time_me
    def get(self):
        """
        直接获取最终聚类结果
        具体方法由代理实现
        :return:
        """
        CentroidsResAgent(self).get()
        print("====step3:聚类全过程求解完成====")

    def show(self):
        """
        显示聚类结果
        :return:
        """
        centroidsreslist = []
        for centroid in self.centroids:
            centroidsreslist.extend([centroid.ellivtk, centroid.linevtk, Point(centroid.pos)])

        print("最大消融椭球vtk的体积为", round(self.centroids[0].ellivtk.volume() / 1000, 2))
        return centroidsreslist


# if __name__ == '__main__':
#     """
#     初始聚类完成
#     """
#     showlist = []
#     showlist.extend(Auto2BaseVtk().show())
#     omega = Omega()
#     omega.get_vtk()
#     omega.get_bodypts()
#     showlist.extend(omega.show())
#     fcom = Fcom()
#     fcom.get_vtk()
#     showlist.extend(fcom.show())
#     centroidsRes = CentroidsRes()
#     centroidsRes.get()
#     showlist.extend(centroidsRes.show())
#     show(showlist)
