"""
# @author chrisxu
# @create 2020-08-24 21:23
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import src.GlobalVar as gl


class LabelUtils():
    """
    Label的工具类
    用于更新整个页面的所有的label
    """



    @staticmethod
    def update_label_TNOW():
        """
        根据透明度滑条，
        更新透明度的label显示值
        :return:
        """
        md = gl.get_value('md')
        alpha = round(md.T_Slider.value() / 100, 2)
        md.label_TNOW.setText(str(alpha))

    @staticmethod
    def update_label_RNOW():
        """
        根据消融半径滑条，
        更新消融半径的label显示值
        :return:
        """
        md = gl.get_value('md')
        R = round(md.R_Slider.value() / 100 * (26 - 18) + 18, 2)
        md.label_RNOW.setText(str(R))

    @staticmethod
    def update_label_KNOW():
        """
        根据长短轴比滑条，
        更新长短轴比的label显示值
        :return:
        """
        md = gl.get_value('md')
        K = round(md.K_Slider.value() / 100 + 1, 2)
        md.label_KNOW.setText(str(K))

    @staticmethod
    def update_pareto_label_by_slider():
        """
        根据帕累托滑条，
        更新帕累托的label显示值
        :return:
        """
        md = gl.get_value('md')

        distmin = float(md.label_distmin.text())
        distmax = float(md.label_distmax.text())
        distnow = round(distmax - md.dist_Slider.value() / 100 * (distmax - distmin), 2)
        md.label_distnow.setText(str(distnow))

        anglemin = float(md.label_anglemin.text())
        anglemax = float(md.label_anglemax.text())
        anglenow = round(anglemax - md.angle_Slider.value() / 100 * (anglemax - anglemin), 2)
        md.label_anglenow.setText(str(anglenow))

        riskmin = float(md.label_riskmin.text())
        riskmax = float(md.label_riskmax.text())
        risknow = round(riskmax - md.risk_Slider.value() / 100 * (riskmax - riskmin), 2)
        md.label_risknow.setText(str(risknow))
