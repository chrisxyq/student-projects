"""
# @author chrisxu
# @create 2020-08-19 15:02
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from collections import defaultdict
import src.GlobalVar as gl



class FeaAgent(object):
    """
    Fea的代理类
    代理get_TSCnum_to_ctpts(self)的方法
    """

    def __init__(self, fea):
        super().__init__()
        # 传入fea对象作为属性
        self.fea = fea
        # Tdic_list: [{} * 8]
        # 其中第一个元素是第一个约束的Tdic
        # 即T的层数到T图像的像素坐标的映射
        self.Tdic_list = [defaultdict(list), defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list)]
        self.Sdic_list = [defaultdict(list), defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list)]
        self.Cdic_list = [defaultdict(list), defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list), defaultdict(list),
                          defaultdict(list), defaultdict(list)]

    def get_TSCnum_to_ctpts(self):
        """
        代理方法
        根据self.fea.ptslist
        为了在CT图画出可行域
        :return:
        """
        for index, indexthfeapts in enumerate(self.fea.ptslist):
            for indexthfeapt in indexthfeapts:
                indexthfeactpt = self.car_to_ct(indexthfeapt)
                self.Tdic_list[index][indexthfeactpt[0]].append([indexthfeactpt[1], indexthfeactpt[2]])
                self.Sdic_list[index][indexthfeactpt[1]].append([indexthfeactpt[2], indexthfeactpt[0]])
                self.Cdic_list[index][indexthfeactpt[2]].append([indexthfeactpt[1], indexthfeactpt[0]])
        self.fea.Tnum_to_ctpts = self.merge_dics(self.Tdic_list)
        self.fea.Snum_to_ctpts = self.merge_dics(self.Sdic_list)
        self.fea.Cnum_to_ctpts = self.merge_dics(self.Cdic_list)

    def car_to_ct(self,pt):
        """
        笛卡尔坐标系转CT坐标系
        :return:
        """
        md = gl.get_value('md')
        return [int(pt[2] / md.caseInfo.st), int(pt[0] / md.caseInfo.ps), int(pt[1] / md.caseInfo.ps)]

    def merge_dics(self, dic_list):
        """
        合并字典{"36":[50],"40":[30]}和{"36":[22],"41":[12]}合并结果为
         {"36":[[50],[22]],"40":[[30],[]],"41":[[],[12]]}
        :param dic_list:
        :return:
        """
        merge_key = []
        res = {}
        for dic in dic_list:
            merge_key += list(dic.keys())
            merge_key = list(set(merge_key))
            # print(merge_key)
        for ele in merge_key:
            res[ele] = []
            for dic in dic_list:
                res[ele].append(dic[ele]) if ele in dic else res[ele].append([])
        return res
