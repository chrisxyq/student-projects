"""
# @author chrisxu
# @create 2020-08-19 10:46
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl

class SliderUtils(object):
    """
    滑块控件的管理类
    所有关于界面滑块的操作写在这里
    """

    def __init__(self, ):
        super().__init__()

    @staticmethod
    def reset_auto1_slider():
        """
        重置所有帕累托滑块为初始状态
        :return:
        """
        md = gl.get_value('md')
        md.comboBox_targets_auto1.clear()
        md.comboBox_pareto_auto1.clear()
        md.label_anglemax.setText("0")
        md.label_anglenow.setText("0")
        md.label_anglemin.setText("0")
        md.angle_Slider.setValue(0)

        md.label_distmax.setText("0")
        md.label_distnow.setText("0")
        md.label_distmin.setText("0")
        md.dist_Slider.setValue(0)

        md.label_riskmax.setText("0")
        md.label_risknow.setText("0")
        md.label_riskmin.setText("0")
        md.risk_Slider.setValue(0)