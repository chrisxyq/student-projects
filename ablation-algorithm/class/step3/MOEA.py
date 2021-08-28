"""
# @author chrisxu
# @create 2020-08-23 11:28
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
# -*- coding: utf-8 -*-
import geatpy as ea  # import geatpy

from step3.MyProblem import MyProblem
from step3base.Auto2Pareto import Auto2Pareto
from step3base.Pareto import Pareto


class MOEA(object):
    """
    ====step7:多目标优化
    方法2多目标优化类
    集成了NSGA-II模板多目标优化算法
    """

    def __init__(self, auto2Fixed):
        super().__init__()
        self.auto2Fixed = auto2Fixed
        """================================实例化问题对象==========================="""
        self.problem = MyProblem(self.auto2Fixed)  # 生成问题对象
        """==================================种群设置==============================="""
        self.Encoding = 'BG'  # 编码方式
        self.NIND = 50  # 种群规模
        self.Field = ea.crtfld(self.Encoding, self.problem.varTypes, self.problem.ranges,
                               self.problem.borders)  # 创建区域描述器
        self.population = ea.Population(self.Encoding, self.Field, self.NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
        """================================算法参数设置============================="""
        self.algorithm = ea.moea_NSGA2_templet(self.problem, self.population)  # 实例化一个算法模板对象
        self.algorithm.mutOper.Pm = 0.2  # 修改变异算子的变异概率
        self.algorithm.recOper.XOVR = 0.9  # 修改交叉算子的交叉概率
        self.algorithm.MAXGEN = 200  # 最大进化代数

    def run(self):
        """==========================调用算法模板进行种群进化========================"""
        NDSet = self.algorithm.run()  # 执行算法模板，得到帕累托最优解集NDSet
        print('====step8:多目标优化用时：%s 秒' % round(self.algorithm.passTime, 2))
        print('非支配个体数：%s 个' % len(NDSet.Phen))
        print('单位时间找到帕累托前沿点个数：%s 个' % (int(len(NDSet.Phen) / self.algorithm.passTime)))
        return NDSet.Phen, NDSet.ObjV
