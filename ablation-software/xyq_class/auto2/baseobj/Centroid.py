"""
# @author chrisxu
# @create 2020-08-21 9:19
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from auto2.ObjToString import obj_to_string


class Centroid(object):
    """
    规划方法2的单个聚类中心的类
    """

    def __init__(self, pos):
        """
        聚类中心对象
        带参构造器
        初始化时，必须指定位置
        :param omega:
        """
        super().__init__()
        self.pos = pos
        self.cluster = []
        self.linevtk = None
        self.ellivtk = None

    def __str__(self):
        return obj_to_string(Centroid, self)
