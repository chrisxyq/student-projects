"""
# @author chrisxu
# @create 2020-08-19 20:56
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import os


class Auto2Para(object):
    """
    单例模式
    规划方法2的参数设置
    case7：新增小肿瘤肿瘤体积 9.76 ml、肿瘤平均尺寸 14.4 mm
    """
    index = 5
    instance = None  # 记录第一个被创建对象的引用
    init_flag = False  # 标记是否执行过初始化动作
    case_dic = {1: "3Dircadb1.9",
                2: "3Dircadb1.15",
                3: "3Dircadb1.15",
                4: "3Dircadb1.16",
                5: "3Dircadb1.17",
                6: "3Dircadb1.17",
                7: "3Dircadb1.1"}
    tmrName_dic = {1: "livertumor1",
                   2: "livertumor1",
                   3: "livertumor2",
                   4: "livertumor1",
                   5: "livertumor1",
                   6: "livertumor2",
                   7: "livertumor5"}
    obList_dic = {1: ['artery', 'bone', 'gallbladder', 'portalvein', 'venoussystem'],
                  2: ['bone', 'portalvein', 'venoussystem'],
                  3: ['bone', 'portalvein', 'venoussystem'],
                  4: ['bone', 'portalvein', 'venoussystem'],
                  5: ['bone', 'portalvein', 'venoussystem'],
                  6: ['artery', 'bone', 'portalvein', 'venoussystem'],
                  7: ['artery', 'bone', 'leftkidney', 'leftlung', 'portalvein', 'rightkidney',
                      'rightlung', 'spleen', 'venoussystem']
                  }
    isBig_dic = {1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 1}
    phi_dic = {
        1: [180, 300],
        2: [180, 360],
        3: [180, 360],
        4: [180, 230],
        5: [220, 350],
        6: [180, 290],
        7: [180, 300]
    }

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否是空对象
        if cls.instance is None:
            # 2.调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
            # print("构造Auto2Para参数配置")
        return cls.instance

    def __init__(self):
        if not Auto2Para.init_flag:
            # print("初始化Auto2Para参数配置")
            super().__init__()
            index = Auto2Para.index
            self.head = r"E:\thesis_task\thesis2\Algorithm2_data"
            self.case = Auto2Para.case_dic[index]
            self.vtkpath = os.path.join(self.head, self.case, "MASKS_PNGPTS", "MESHES_VTK")
            self.tmrname = Auto2Para.tmrName_dic[index]
            self.oblist = Auto2Para.obList_dic[index]
            self.phi = Auto2Para.phi_dic[index]  # 获取预进针区域参数设置：横向角度约束
            self.mz = 30
            self.feasible_r = 50  # 可行域球的半径
            self.isbig = Auto2Para.isBig_dic[index]
            self.MAXABR = 26  # 最大短轴半径
            self.K = 1.3  # 长短轴比例
            Auto2Para.init_flag = True
