import sqlite3

from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *

import re
import pydicom


def get_pixel_info(): 
    dcm_tag = pydicom.read_file(os.path.join(r"E:\thesis_task\3Dircadb_download",case,'PATIENT_DICOM','image_0'))
    pixel_info = [dcm_tag.PixelSpacing[0], dcm_tag.PixelSpacing[1], dcm_tag.SliceThickness, len(os.listdir(os.path.join(r"E:\thesis_task\3Dircadb_download",case,'PATIENT_DICOM')))]
    print(pixel_info)
    gl.set_value('pixel_info',pixel_info )
    return pixel_info


def get_targetstxt():
    """
    功能：1.读取医生标记的db文件的靶点坐标
    2.获取医生标记该病例的dicom参数
    """
 
    pixel_info= get_pixel_info()
    tblname='PATIENT_PNG'+re.sub('\\D','',case)[2:] #'\\D'代表非数字，意为提取3Dircadb1.17(3117)的17
    targetpts=[]
    inpts=[] 

    conn = sqlite3.connect(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\label.db')
    c = conn.cursor()    
    if tblname=='PATIENT_PNG17': #(2个两针大肿瘤) re.sub('\\D','',tmrname)
        
        cursor = c.execute("SELECT slice , X , Y from %s WHERE kind==0 and num==" %tblname +str(re.sub('\\D','',tmrname))+"."+str(order) )
        for row in cursor:
            #靶点为[笛卡尔xyz，ct图上的xy和层数]
            targetpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2],row[1],row[2],row[0]]) 
        
        cursor = c.execute("SELECT slice , X , Y from %s WHERE kind==1 and num==" %tblname +str(re.sub('\\D','',tmrname))+"."+str(order) )
        for row in cursor:
            #进针点为[笛卡尔xyz，ct图上的xy和层数]
            inpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2]])  
                      

    elif tblname=='PATIENT_PNG15': #(2个小肿瘤)
        if tmrname == "livertumor1":
            cursor = c.execute("SELECT slice , X , Y from %s WHERE kind==0 and num==1" %tblname)
            for row in cursor:
                targetpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2],row[1],row[2],row[0]])
        
            cursor2 = c.execute("SELECT slice , X , Y from %s WHERE kind==1 and num==1" %tblname)
            for row in cursor2:
                inpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2]])                   

        elif tmrname == "livertumor2":
            cursor = c.execute("SELECT slice , X , Y from %s WHERE kind==0 and num==2" %tblname)
            for row in cursor:
                targetpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2],row[1],row[2],row[0]])
   
            cursor2 = c.execute("SELECT slice , X , Y from %s WHERE kind==1 and num==2" %tblname)
            for row in cursor2:
                inpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2]])
    elif tblname=='PATIENT_PNG9': #（单发肿瘤）
        cursor = c.execute("SELECT slice , X , Y from %s WHERE kind==0 and num==" %tblname +str(order) )
        for row in cursor:
            targetpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2],row[1],row[2],row[0]])
        #print("SELECT slice , X , Y from %s WHERE kind==1 and num==" %tblname +str(order))
        cursor2 = c.execute("SELECT slice , X , Y from %s WHERE kind==1 and num==" %tblname +str(order))
        for row in cursor2:
            inpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2]])
    else: #（单发肿瘤）
        cursor = c.execute("SELECT slice , X , Y from %s WHERE kind==0" %tblname)
        for row in cursor:
            targetpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2],row[1],row[2],row[0]])
        cursor2 = c.execute("SELECT slice , X , Y from %s WHERE kind==1" %tblname)
        for row in cursor2:
            inpts.append([row[1]*pixel_info[0],row[2]*pixel_info[1],row[0]*pixel_info[2]])
    conn.close()
    gl.set_value('targetpos', targetpts[0])#靶点为[笛卡尔xyz，ct图上的xy和层数]
    gl.set_value('inpts', np.array(inpts))#进针点为[笛卡尔xyz，ct图上的xy和层数]
    print('靶点坐标为',gl.get_value('targetpos'))
    print('进针点坐标为',gl.get_value('inpts'))



	    

