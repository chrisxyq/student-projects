"""
# @author chrisxu
# @create 2020-08-22 19:25
# Ctrl + Alt + L：格式化代码
# ctrl + Alt + T：代码块包围
# ctrl + Y：删除行
# ctrl + D：复制行
# alt+上/下：移动光标到上/下方法
"""
from vtkplotter import *
import os

if __name__ == '__main__':

    head = r'E:\thesis_task\ALL_DATA'
    casename = "3Dircadb1.19"
    showlist = []
    vtknames = os.listdir(os.path.join(head, casename, "MESHES_VTK"))
    print("病例名为", casename)
    for vtkname in vtknames:
        if "livertumor" in vtkname:
            vtk = load(os.path.join(head, casename, "MESHES_VTK", vtkname), c=(105, 105, 105), alpha=0.5)
            showlist.append(vtk)
            print(vtkname, "的体积为", round(vtk.volume() / 1000, 2), "ml,平均尺寸为", round(vtk.averageSize() / 10, 2), "cm")
    show(showlist) if showlist != [] else print("该病例没有肿瘤")
