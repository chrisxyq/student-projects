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
import src.GlobalVar as gl
from auto2.ObjToString import obj_to_string
from auto2.objagent.CentroidsResAgent import CentroidsResAgent


class CentroidsRes(object):
    """
    规划方法2的聚类结果类
    """

    def __init__(self):
        """
        传入omega对象作为属性
        以初始化聚类数目self.num
        :param omega:
        """
        # print("初始化ClusterRes聚类结果")
        super().__init__()
        self.num = 0  # 聚类数目
        self.centroids = []  # 聚类中心对象

    def __str__(self):
        return obj_to_string(CentroidsRes, self)

    def clear(self):
        """
        在迭代聚类结果时候
        清除对象
        :return:
        """
        self.centroids = []

    def get(self):
        """
        直接获取最终聚类结果
        具体方法由代理实现
        :return:
        """
        CentroidsResAgent(self).get()
        print("====step3:聚类全过程求解完成====")

