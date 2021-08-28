"""
# @author chrisxu
# @create 2020-08-15 9:57
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""

import src.GlobalVar as gl


class ComboBoxUtils():
    """
    ComboBox的工具类
    """

    @staticmethod
    def add_to_comboBox_schemes_auto2(auto2Pareto):
        """
        使用优化得到的auto2帕累托解
        添加到可选进针方案下拉框
        :return:
        """
        md = gl.get_value('md')
        md.comboBox_schemes_auto2.clear()
        for i in range(len(auto2Pareto.pareto)):
            md.comboBox_schemes_auto2.addItem("进针方案"+str(i + 1))

    @staticmethod
    def clear_all_comboBox():
        """
        清空所有下拉框
        由于“载入”也要使用，因此
        不清除comboBox_patient
        :return:
        """
        md = gl.get_value('md')

        md.comboBox_labelled_case.clear()  # 手动规划-已标记病例列表
        md.comboBox_targets_hand.clear()  # 手动规划-靶点列表
        md.comboBox_inpts_hand.clear()  # 手动规划-进针点列表

        md.comboBox_targets_auto1.clear()  # 逐针规划-靶点列表
        md.comboBox_pareto_auto1.clear()  # 逐针规划-帕累托列表

        md.comboBox_tmrs_auto2.clear()  # 并行规划-规划对象
        md.comboBox_schemes_auto2.clear()  # 并行规划-进针方案列表

    @staticmethod
    def add_to_comboBox(vtkname, comboBox):
        """
        将vtkname加到comboBox
        更新显示列表
        :return:
        """
        items = ComboBoxUtils.getall_from_comboBox(comboBox)
        if vtkname not in items:
            comboBox.addItem(vtkname)

    @staticmethod
    def whether_in_comboBox(vtkname, comboBox):
        items = ComboBoxUtils.getall_from_comboBox(comboBox)
        if vtkname in items:
            return 1
        else:
            return 0

    @staticmethod
    def getall_from_comboBox(comboBox):
        items = []
        for i in range(comboBox.count()):
            items.append(comboBox.itemText(i))
        return items

    @staticmethod
    def init_comboBox_farobj():
        """
        初始化父对象类型的combobox，在载入时候被调用
        注意！！！！！！！！！此时将自动调用on_comboBox_farobj()
        :return:
        """
        md = gl.get_value('md')
        # print("md.objdic",md.objdic)
        for name in md.objdic:
            # print("name",name)
            ComboBoxUtils.add_to_comboBox(name, md.comboBox_farobj)

    @staticmethod
    def update_comboBox_sonobj():
        """
        当父combox_farobj下拉框更新
        :return:
        """
        md = gl.get_value('md')
        if md.init3D:
            namelist = md.objdic[md.comboBox_farobj.currentText()]
            md.comboBox_sonobj.clear()
            for name in namelist:
                ComboBoxUtils.add_to_comboBox(name, md.comboBox_sonobj)

    @staticmethod
    def clear_comboBox_auto1():
        md = gl.get_value('md')
        md.comboBox_targets_auto1.clear()
        md.comboBox_pareto_auto1.clear()

    @staticmethod
    def addTarToCombox():
        """
        把靶点加到靶点列表
        :return:
        """
        md = gl.get_value('md')
        if md.init3D:
            md.comboBox_targets_auto1.clear()
            helper = md.comboBox_patient.currentText()
            if helper == '3Dircadb1.9':
                md.comboBox_targets_auto1.addItem("1.1-36-(110,213)")
                md.comboBox_targets_auto1.addItem("1.2-36-(97,230)")
            elif helper == '3Dircadb1.15':
                md.comboBox_targets_auto1.addItem("1-106-(279,184)")
                md.comboBox_targets_auto1.addItem("2-106-(141,222)")
            elif helper == '3Dircadb1.16':
                md.comboBox_targets_auto1.addItem("1-59-(134,243)")
            elif helper == '3Dircadb1.17':
                md.comboBox_targets_auto1.addItem("1.1-87-(261,178)")
                md.comboBox_targets_auto1.addItem("1.2-87-(282,172)")
                md.comboBox_targets_auto1.addItem("2.1-104-(148,171)")
                md.comboBox_targets_auto1.addItem("2.2-104-(133,194)")

    @staticmethod
    def init_comboBox_tmrs_auto2():
        """
        初始化并行规划的规划列表
        :return:
        """
        md = gl.get_value('md')
        if md.init3D:
            md.comboBox_tmrs_auto2.clear()
            helper = md.comboBox_patient.currentText()
            if helper == '3Dircadb1.9':
                md.comboBox_tmrs_auto2.addItem("livertumor1")
            elif helper == '3Dircadb1.15':
                md.comboBox_tmrs_auto2.addItem("livertumor1")
                md.comboBox_tmrs_auto2.addItem("livertumor2")
            elif helper == '3Dircadb1.16':
                md.comboBox_tmrs_auto2.addItem("livertumor1")
            elif helper == '3Dircadb1.17':
                md.comboBox_tmrs_auto2.addItem("livertumor1")
                md.comboBox_tmrs_auto2.addItem("livertumor2")
