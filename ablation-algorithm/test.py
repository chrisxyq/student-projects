import os
import time
import random




#打开手机开发者选项，小米手机打开usb调试（安全设置），打开指针位置，找到要点击的 x,y坐标
def loop_click_for_android(run_num=150):
    inputs = str(input("请确保已打开测试页面(y/n)： "))

    if inputs == "y":
        inputsxy = str(input("输入坐标（用空格分割）： "))
        sum = 0
        n = 4888
        while (sum <n):
            strr ="1"
            if inputsxy == "":
                    strr = ('adb shell input touchscreen swipe 330 880 930 880')
            else:
                    strr = ('adb -s 8e6c3a73 shell input tap '+str(inputsxy))
            a = os.system(strr)
            # x = random.randint(1,5)/10
            # time.sleep(x)
            sum += 1
            print(sum)
        # over_time = time.time()
        # print("{}次点击的运行时间是：{}".format(run_num, over_time - node_time))  # 次数统计并不准确
    else:
        print("程序关闭~")
        exit(1)

loop_click_for_android()