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
import src.GlobalVar as gl
from agent.ElliVTKAgent import ElliVTKAgent
from auto2.baseobj.Centroid import Centroid
from objutils.NeedleUtils import NeedleUtils


class CentroidsResAgent(object):
    """
    ====step3:聚类全过程求解
    规划方法2的求解聚类结果的代理类
    负责聚类以及消融效果的验证
    """


    def __init__(self, centroidsRes):
        """
        传入omega对象作为属性
        以代理方法
        :param omega:
        """
        super().__init__()
        self.centroidsRes = centroidsRes  # 实时聚类结果
        self.threshold = 0.98
        self.satisfy = False  # 聚类结果满足阈值，则为true，则完成任务
        self.MAXABR = 26  # 最大短轴半径
        self.K = 1.3  # 长短轴比例
        self.color = (152, 251, 152)
        self.alpha = 0.7
        self.lw = 5

    def init_num(self):
        """
        初始化self.clusterRes.num
        :return:
        """
        md = gl.get_value('md')
        VMAXELLI = 4 / 3 * pi * self.MAXABR ** 3 / self.K ** 2
        vomega = md.omega.vtk.volume()
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
        md = gl.get_value('md')
        omegapts = md.omega.bodypts
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
        md = gl.get_value('md')
        Pcom = md.fcom.vtk.centerOfMass()  # 返回质心可行域的质心
        Tcom = md.omega.vtk.centerOfMass()  # 返回待消融区域的质心

        for centroid in self.centroidsRes.centroids:
            P = np.array(Pcom) - np.array(Tcom) + np.array(centroid.pos)  # 该聚类中心的初始进针点
            centroid.ellivtk = ElliVTKAgent.get_vtk(P, centroid.pos, self.MAXABR, self.K, self.color, self.alpha)
            centroid.linevtk = NeedleUtils.get_vtk(P, centroid.pos, self.color, self.alpha, self.lw)

    def check(self):
        """
        根据omega的体点云
        以及保存的消融椭球vtk
        判断体点云位于消融椭球内的比率是否满足预设阈值
        :return: 布尔类型
        """
        md = gl.get_value('md')
        omegapts = md.omega.bodypts
        omegaptsnum = len(omegapts)
        cnt = 0

        for omegapt in omegapts:
            for centroid in self.centroidsRes.centroids:
                if centroid.ellivtk.isInside(omegapt):
                    cnt += 1
                    break
        #print("消融数目", cnt, "待消融体点云数目", omegaptsnum)
        print("当前聚类数", self.centroidsRes.num)
        if cnt / omegaptsnum > self.threshold:
            self.satisfy = True
        else:
            self.centroidsRes.num += 1
