# encoding=utf-8
from os import path
import numpy as np
import pydicom
import re
from matplotlib import pyplot as plt
import os
import time
import cv2
import glob
import codecs
import math
m=0
def rescale_trans(ds):
    rescale_intercept = ds.RescaleIntercept
    rescale_slope = ds.RescaleSlope
    img = ds.pixel_array
    img = img * rescale_slope + rescale_intercept
    return img
def window_trans(img, window_center, window_width, range):
    # :param img: numpy array,图像灰度矩阵
    # :param window_center: dicom文件中定义的window_center
    # :param window_width: dicom文件中定义的window_width
    # :param range: [min,max],灰度范围
    # :return: 处理后的图像灰度矩阵
    # """
    try:
        window_min = window_center - 0.5 - (window_width - 1) / 2
        window_max = window_center - 0.5 + (window_width - 1) / 2
    except Exception:
        window_center = window_center[0]
        window_width = window_width[0]
        window_min = window_center - 0.5 - (window_width - 1) / 2
        window_max = window_center - 0.5 + (window_width - 1) / 2
    ymin = range[0]
    ymax = range[1]
    def trans(x):
        if x <= window_min:
            return ymin
        elif x > window_max:
            return ymax
        else:
            return ((x - (window_center - 0.5)) / (window_width - 1) + 0.5) * (ymax - ymin) + ymin
    return np.array(list(map(trans, img.ravel())), np.uint8).reshape(img.shape)
def tranToPNG(addr,png_dir):
    """
    若下面这行注释掉，用于转成适合给医生的点投影的png，不注释就是用于nonzero的mask体素提取的png
    #ret, img_bgr = cv2.threshold(img_bgr, 127, 255, cv2.THRESH_BINARY)
    """
    fileName = addr
    ds = pydicom.read_file(fileName)
    # 预处理窗口变换
    if hasattr(ds, 'RescaleIntercept'):
        img = rescale_trans(ds)
    else:
        img = ds.pixel_array
    img = window_trans(img, 40, 200, [0, 255])
    shape = img.shape
    img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    ret, img_bgr = cv2.threshold(img_bgr, 127, 255, cv2.THRESH_BINARY)
    liver_img_path_og = path.join('mimics',png_dir + '.png')
    cv2.imwrite(liver_img_path_og, img_bgr)
    print(liver_img_path_og, 'is saved')

def get_file_names(file_dir):
    allfiles = []
    for root, dirs, files in os.walk(file_dir):
                allfiles.append(dirs)
    return allfiles[0]




def dicom_to_png(dicom_dir,organame,files):
    """
    
    """
    filenames = get_file_names(dicom_dir)
    if not os.path.exists(os.path.join(head, 'MASKS_PNG', organame)):
        os.makedirs(os.path.join(head, 'MASKS_PNG', organame))
    try:
        fileaddr =dicom_dir+ "\\image_"
        for i in range(files):
            file = fileaddr + str(i)
            png_dir = os.path.join(head, 'MASKS_PNG', organame,'image_')+ str(i)
            tranToPNG(file,png_dir)
    except:
        print("出错")
        pass
