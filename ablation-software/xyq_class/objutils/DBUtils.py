"""
# @author chrisxu
# @create 2020-08-17 9:19
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import sqlite3
import src.GlobalVar as gl


class DBUtils(object):
    """
    SQLite数据库操作
    """

    conn = sqlite3.connect('my_label.db')
    c = conn.cursor()

    def __init__(self):
        super().__init__()

    @staticmethod
    def query_marked_points():
        """
        查询当前病例已经标记的靶点/进针点
        :return:
        """
        md = gl.get_value('md')
        tarlist, inlist = [], []
        cursor = DBUtils.c.execute(
            "SELECT num, slice , X , Y from '%s' WHERE kind==0" % md.comboBox_labelled_case.currentText())
        for row in cursor:
            tarlist.append(row[0] + '-' + str(row[1]) + '-(' + str(row[2]) + ',' + str(row[3]) + ')')

        cursor = DBUtils.c.execute(
            "SELECT num, slice , X , Y from '%s' WHERE kind==1" % md.comboBox_labelled_case.currentText())
        for row in cursor:
            inlist.append(row[0] + '-' + str(row[1]) + '-(' + str(row[2]) + ',' + str(row[3]) + ')')

        return tarlist, inlist

    @staticmethod
    def query_marked_table():
        """
        查询非空的数据表格
        :return:
        """
        # 首先获取数据库中所有的表名保存在alltable
        alltable = DBUtils.c.execute("select name from sqlite_master where type = 'table' order by name").fetchall()
        # tblist用于保存数据库中标记记录不为空的table
        tblist = []
        for tbl in alltable:
            tbl = tbl[0]
            cursor = DBUtils.c.execute("SELECT kind from '%s'" % tbl)
            if len(cursor.fetchall()) != 0:  # 在tblist中添加表格内容不为空的病例名
                tblist.append(tbl)
        return tblist

    @staticmethod
    def query_points_from_slice():
        """
        查询当前层所有标记
        :return:
        """
        md = gl.get_value('md')
        tbl = md.comboBox_patient.currentText()
        slicer = md.Scroll_T.value()
        script = "SELECT kind,num , X , Y from '%s' where slice=%d;" % (tbl, slicer)
        cursor = DBUtils.c.execute(script)
        dao = []
        for row in cursor:
            dao.append(row)
        # print("当前所有标记", dao)
        return dao

    @staticmethod
    def del_points_from_slice():
        """
        删除当前层所有标记
        :return:
        """
        md = gl.get_value('md')
        tbl = md.comboBox_patient.currentText()
        slicer = md.Scroll_T.value()
        script = "DELETE from '%s' where slice=%d;" % (tbl, slicer)
        DBUtils.c.execute(script)
        DBUtils.conn.commit()
        # print("当前所有标记已经删除")

    @staticmethod
    def del_lastone():
        """
        撤销时使用
        :return:
        """
        md = gl.get_value('md')
        tbl = md.comboBox_patient.currentText()
        DBUtils.c.execute("SELECT * FROM '%s'" % tbl)
        lenth = len(DBUtils.c.fetchall())
        DBUtils.c.execute("DELETE from '%s' where ID=%d;" % (tbl, lenth))
        DBUtils.conn.commit()

    @staticmethod
    def delete(row):
        """
        删除单条数据
        :param row:
        :return:
        """
        md = gl.get_value('md')
        tbl = md.comboBox_patient.currentText()
        DBUtils.c.execute("DELETE from '%s' where num=%s and slice=%s and X=%s and Y=%s;" % (
            tbl, row[0], row[1], row[2], row[3]))
        # print("DELETE from '%s' where num=%s and slice=%s and X=%s and Y=%s;" % (
        #     tbl, row[0], row[1], row[2], row[3]))
        DBUtils.conn.commit()

    @staticmethod
    def insert(row):
        """
        插入单条数据
        :return:
        """
        md = gl.get_value('md')
        tbl = md.comboBox_patient.currentText()
        DBUtils.c.execute("SELECT * FROM '%s'" % tbl)
        lenth = len(DBUtils.c.fetchall())
        [kind, num, X, Y] = row
        DBUtils.c.execute("INSERT INTO '%s' (id,kind,num,slice,X,Y) VALUES (%d,%d, %s, %d,%d,%d )"
                            % (tbl, lenth + 1, kind, num, md.Scroll_T.value(), X, Y))
        DBUtils.conn.commit()
