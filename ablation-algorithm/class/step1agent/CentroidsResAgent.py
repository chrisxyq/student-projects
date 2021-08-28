"""
# @author chrisxu
# @create 2020-08-21 9:30
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from math import pi, ceil
from sklearn.cluster import KMeans
import numpy as np
from singleton.Auto2Para import Auto2Para
from singleton.LineGetter import LineGetter
from step1.Fcom import Fcom
from singleton.ElliGetter import ElliGetter
from step1.Omega import Omega
from step1base.Centroid import Centroid


class CentroidsResAgent(object):
    """
    ====step3:聚类全过程求解
    规划方法2的求解聚类结果的代理类
    负责聚类以及消融效果的验证
    """
    #threshold_dic = {1: 0.99, 5: 0.98, 6: 0.98, 7: 0.98}

    def __init__(self, centroidsRes):
        """
        传入omega对象作为属性
        以代理方法
        :param omega:
        """
        super().__init__()
        self.centroidsRes = centroidsRes  # 实时聚类结果
        self.omega = Omega()  # 待消融区域，已计算好直接调用
        self.fcom = Fcom()  # 已计算好，直接调用
        self.threshold = 0.98
        self.satisfy = False  # 聚类结果满足阈值，则为true，则完成任务

    def init_num(self):
        """
        初始化self.clusterRes.num
        :return:
        """
        VMAXELLI = 4 / 3 * pi * Auto2Para().MAXABR ** 3 / Auto2Para().K ** 2
        vomega = self.omega.vtk.volume()
        print("omega体积", round(vomega / 1000, 2), "理论最大椭球体积", round(VMAXELLI / 1000, 2))
        self.centroidsRes.num = ceil(vomega / VMAXELLI)

    def get(self):
        """
        对待消融区域的体点云omega.bodypts进行聚类
        以获得聚类结果
        :return:
        """
        self.init_num()  # 首先初始化聚类数目
        while not self.satisfy:
            self.centroidsRes.clear()  # 清除结果
            self.kmeans()
            self.get_vtk()
            self.check()

    def kmeans(self):
        """
        根据实时聚类结果
        实时赋值给cluster对象
        :return:
        """
        omegapts = self.omega.bodypts
        km = KMeans(n_clusters=self.centroidsRes.num).fit(omegapts)
        centroidspos = km.cluster_centers_
        # 以各个聚类中心位置new出来centroid对象，并添加到聚类结果
        for pos in centroidspos:
            self.centroidsRes.centroids.append(Centroid(pos))
        # 将聚类子点云传入centroid对象
        for index, label in enumerate(km.labels_):
            self.centroidsRes.centroids[label].cluster.append(omegapts[index])

    def get_vtk(self):
        """
        根据上一步kmeans得到的
        聚类中心获取各个消融椭球vtk
        注意此时质心可行域需要已经求解完成！
        :return:
        """

        Pcom = self.fcom.vtk.centerOfMass()  # 返回质心可行域的质心
        Tcom = self.omega.vtk.centerOfMass()  # 返回待消融区域的质心
        r = Auto2Para().MAXABR  # 最大消融椭球长轴半径

        for centroid in self.centroidsRes.centroids:
            P = np.array(Pcom) - np.array(Tcom) + np.array(centroid.pos)  # 该聚类中心的初始进针点
            centroid.ellivtk = ElliGetter().get_elli_vtk(P, centroid.pos, r)
            centroid.linevtk = LineGetter().get_line_vtk(P, centroid.pos)

    def check(self):
        """
        根据omega的体点云
        以及保存的消融椭球vtk
        判断体点云位于消融椭球内的比率是否满足预设阈值
        :return: 布尔类型
        """
        omegapts = self.omega.bodypts
        omegaptsnum = len(omegapts)
        cnt = 0


        for omegapt in omegapts:
            for centroid in self.centroidsRes.centroids:
                if centroid.ellivtk.isInside(omegapt):
                    cnt += 1
                    break
        print("消融数目", cnt, "待消融体点云数目", omegaptsnum)
        print("当前聚类数", self.centroidsRes.num)
        if cnt / omegaptsnum > self.threshold:
            self.satisfy = True
        else:
            self.centroidsRes.num += 1
