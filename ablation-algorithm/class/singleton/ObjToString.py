"""
# @author chrisxu
# @create 2020-08-20 21:42
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""


def obj_to_string(cls, obj):
    """
    简单地实现类似对象打印的方法
    :param cls: 对应的类(如果是继承的类也没有关系，比如A(object),
    cls参数传object一样适用，如果你不想这样，可以修改第一个if)
    :param obj: 对应类的实例
    :return: 实例对象的to_string
    """
    if not isinstance(obj, cls):
        raise TypeError("obj_to_string func: 'the object is not an instance of the specify class.'")
    to_string = str(cls.__name__) + "("
    items = obj.__dict__
    n = 0
    for k in items:
        if k.startswith("_"):
            continue
        to_string = to_string + str(k) + "=" + str(items[k]) + ","
        n += 1
    if n == 0:
        to_string += str(cls.__name__).lower() + ": 'Instantiated objects have no property values'"
    return to_string.rstrip(",") + ")"
