"""
# @author chrisxu
# @create 2020-08-20 10:22
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
import datetime


def time_me(func):
    """
    这个装饰器用于统计函数运行的耗时。用来分析脚本的性能
    :param fn:
    :return:
    """

    def wrapper(*args, **kw):
        start_time = datetime.datetime.now()
        res = func(*args, **kw)
        over_time = datetime.datetime.now()
        print('{0} 的运行时长为 {1}'.format(func.__name__, round((over_time - start_time).total_seconds(), 2)), "s")
        return res

    return wrapper
