import cv2
import os
import numpy as np
from sys import path
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\params')
from setpara import *


path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\tools')
from tf_tools import *
path.append(r'E:\thesis_task\thesis2\Algorithm1_reconsitution\preprocess')
from get_targetstxt import *
from PIL import Image, ImageDraw
import globalvar as gl
from sklearn.neighbors import NearestNeighbors

def angle_to_pic(angle,anglename,Hindex):
    #保存角度组合为图片
    bg = Image.open(os.path.join(head,"bg.png"))
    for ele in angle:
    	if ele[1]!=0:
        	bg.putpixel(ele,color_dic[Hindex])
    bg.save(os.path.join(opic_ndlpath, anglename+'.png'))

def closing(size,anglename):
	#对图片进行闭运算
    anglepic = cv2.imread(os.path.join(opic_ndlpath, anglename+'.png'))
    #保存闭运算后的png
    kernel= cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    angle_backpic  = cv2.morphologyEx(anglepic , cv2.MORPH_CLOSE, kernel) 
    # print(angle_backpic[0][0] )   
    cv2.imwrite(os.path.join(opic_ndlpath, anglename+'_back.png'), angle_backpic )
    return angle_backpic


def change_color(name,color):
    #把白色改成彩色
    a=Image.open(os.path.join(opic_ndlpath, name+'.png'))
    for x in range(181):
        for y in range(361):
            if a.getpixel((x,y))==(255,255,255):
                a.putpixel([x,y],color)
    a.save(os.path.join(opic_ndlpath, name+'.png'))



def minus_pic(name1,name2,resname):
    #name1-name2
    a=Image.open(os.path.join(opic_ndlpath, name1+'.png'))
    b=Image.open(os.path.join(opic_ndlpath, name2+'.png'))
    for x in range(181):
        for y in range(361):
            if a.getpixel((x,y))==(255,255,255) and b.getpixel((x,y))!=(0,0,0):
                a.putpixel([x,y],(0,0,0))
    a.save(os.path.join(opic_ndlpath, resname+'.png'))


def minus_pic_and_get_Hskin(name1,name2,resname):
    #输入：排除的图像和皮肤字典
    #输出：硬约束排除的皮肤
    #一定要从图像角度来找，否则找到的皮肤点不够密
    skin_dic=gl.get_value('skin_dic' )
    Hskin=[]
    a=Image.open(os.path.join(opic_ndlpath, name1+'.png'))
    b=Image.open(os.path.join(opic_ndlpath, name2+'.png'))
    for x in range(181):
        for y in range(361):
            helper=str([x,y])
            if b.getpixel((x,y))!=(0,0,0) and helper in skin_dic:
                a.putpixel([x,y],(0,0,0))
                Hskin.append(skin_dic[helper][1])
    a.save(os.path.join(opic_ndlpath, resname+'.png'))
    if name2=='H4_back' :
        np.savetxt(os.path.join(otxt_hardpath,'H4',name2+'_skin.txt'),Hskin)
    elif name2=='H5_back':
        np.savetxt(os.path.join(otxt_hardpath,'H5',name2+'_skin.txt'),Hskin)
    elif name2=='H6_back' :
        np.savetxt(os.path.join(otxt_hardpath,'H6',name2+'_skin.txt'),Hskin)
    elif name2=='H7_back' :
        np.savetxt(os.path.join(otxt_hardpath,'H7',name2+'_skin.txt'),Hskin)
    else:
        np.savetxt(os.path.join(otxt_hardpath,'H4',name2+'_skin.txt'),Hskin)











def minus_pic_and_get_skin_dic(name1,name2,resname):
    #name1-name2
    skin_dic={}
    H3_skin=[]
    neigh = NearestNeighbors(n_neighbors=1)
    skin_helper=gl.get_value('skin_helper' )
    neigh.fit([ele[1:3] for ele in skin_helper])
    
    a=Image.open(os.path.join(opic_ndlpath, name1+'.png'))
    b=Image.open(os.path.join(opic_ndlpath, name2+'.png'))
    helper=[]
    for x in range(181):
        for y in range(361):
            if a.getpixel((x,y))==(255,255,255):
                if b.getpixel((x,y))!=(0,0,0):
                    a.putpixel([x,y],(0,0,0))
                    helper.append([x,y])
                    dist, ind = neigh.kneighbors([[x,y]])
                    H3_skin.append(skin_helper[ind[0][0]][3])
                else:
                    dist, ind = neigh.kneighbors([[x,y]]) 
                    value=[skin_helper[ind[0][0]][0],skin_helper[ind[0][0]][3]]
                    skin_dic[str([x,y])]=value
                    #skin_dic[str([x,y+1])]=value
    gl.set_value('skin_dic',skin_dic )
    np.savetxt(os.path.join(otxt_hardpath,'H3','H3_skin.txt'),H3_skin)
    np.savetxt(os.path.join(otxt_hardpath,'skin_dic_keys.txt'),list(skin_dic.keys()),fmt='%s')
    a.save(os.path.join(opic_ndlpath, resname+'.png'))
    fresh_H3(helper)



def fresh_H3(helper):
    #if test_index==5 or test_index==6:
    bg = Image.open(os.path.join(head,"bg.png"))
    for ele in helper:
        bg.putpixel(ele,color_dic[3])
    bg.save(os.path.join(opic_ndlpath, 'H3_back.png'))




def get_mirror(sphere):
    if sphere[1]<181:
        mirror=[180-sphere[0],sphere[1]+180]
    else:
        mirror=[180-sphere[0],sphere[1]-180]
    return mirror



def get_Hskin(name):
    #输入：排除的图像和皮肤字典
    #输出：硬约束排除的皮肤
    #一定要从图像角度来找，否则找到的皮肤点不够密
    skin_dic=gl.get_value('skin_dic' )
    #print(skin_dic)
    Hskin=[]
    a=Image.open(os.path.join(opic_ndlpath, name+'.png'))
    for x in range(181):
        for y in range(361):
            helper=str([x,y])
            if a.getpixel((x,y))!=(0,0,0) and helper in skin_dic:
                Hskin.append(skin_dic[helper][1])
    if name=='round2' :
        np.savetxt(os.path.join(otxt_hardpath,'H5','round2_skin.txt'),Hskin)
    if name=='H4' :
        np.savetxt(os.path.join(otxt_hardpath,'H4','H4_skin.txt'),Hskin)
    # if name=='H4' or name=='H5' or name=='H6' or name=='H7':
    #     np.savetxt(os.path.join(otxt_hardpath,name,name+'_skin.txt'),Hskin)
    # else:
    #     np.savetxt(os.path.join(otxt_hardpath,'H3',name+'_skin.txt'),Hskin)

def H6_helper():
    if order==1:
        denoise('round2')
        #change_color('Final_denoise',RGB_feasible)
        read_Feasible()


def denoise(picname):
    image = Image.open(os.path.join(opic_ndlpath, picname+'.png'))
    image = image.convert("L")
    clearNoise(image, 70, 4, 5)
    image.save(os.path.join(opic_ndlpath, 'Final_denoise.png'))
    change_color('Final_denoise',RGB_feasible)
    # if picname=='H3':
    #     image.save(os.path.join(opic_ndlpath, 'H3.png'))
    # else:
    #     image.save(os.path.join(opic_ndlpath, 'Final_denoise.png'))
    


def read_Feasible():
    #读Final_denoise.png获取Feasible_angle.txt
    res=[]
    #bg = Image.open(os.path.join(head,"bg.png"))
    
    #a=Image.open(os.path.join(opic_ndlpath, 'Final_denoise.png'))
    a=Image.open(os.path.join(opic_ndlpath, 'round2.png')) if order==1 else Image.open(os.path.join(opic_ndlpath, 'round3.png'))
    for x in range(181):
        for y in range(360):
            #if a.getpixel((x,y))==255:
            if a.getpixel((x,y))==(255,255,255):
                res.append([x,y])
                #bg.putpixel([x,y],RGB_feasible)
    gl.set_value('Feasible',res)
    gl.set_value('FNUM',len(res) )
    print('可行域点数',len(res))
    #bg.save(os.path.join(opic_ndlpath, 'Final_denoise.png'))
    np.savetxt(os.path.join(otxt_hardpath,'Feasible_angle.txt'),res, fmt='%i')


#===================去噪===========================================
def getPixel(image, x, y, G, N):
    """
    工具4：ok_angle.png：去噪
    """
    L = image.getpixel((x, y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x, y - 1))
    else:
        return None
def clearNoise(image, G, N, Z):
    """
    工具4：ok_angle.png：去噪
    """
    draw = ImageDraw.Draw(image)
    for i in range(0, Z):
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)
 

# minus_pic('skin_back','H1_back','helper')
# minus_pic('helper','H2_back','helper')
# denoise('helper')
# read_Feasible()

# def erode(picname):
#     img = cv2.imread(os.path.join(opic_ndlpath, picname+'.png'))
#     print(image.shape)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#     dst = cv2.erode(binary, kernel)
#     cv2.imsave("erode", dst)


def erode(picname,knl):
    """
    功能：遍历MASKS_PNG文件夹，将器官膨胀5mm，保存在MASKS_PNG_DILATED
    参数：png_dir,dilate_dir
    使用大小为5 *2/ pixel_info[0]个像素的方形kernel，中心为kernel的中心体素
    """
    img = cv2.imread(os.path.join(opic_ndlpath, picname+'.png'))   
    kernel =cv2.getStructuringElement(cv2.MORPH_RECT,(knl,knl))
    erode = cv2.erode(img, kernel)
    cv2.imwrite(os.path.join(opic_ndlpath, picname+'.png'), erode)



def dilate(picname,knl):
    """
    功能：遍历MASKS_PNG文件夹，将器官膨胀5mm，保存在MASKS_PNG_DILATED
    参数：png_dir,dilate_dir
    使用大小为5 *2/ pixel_info[0]个像素的方形kernel，中心为kernel的中心体素
    """
    img = cv2.imread(os.path.join(opic_ndlpath, picname+'.png'))   
    kernel =cv2.getStructuringElement(cv2.MORPH_RECT,(knl,knl))
    dilate = cv2.dilate(img, kernel)
    cv2.imwrite(os.path.join(opic_ndlpath, picname+'.png'), dilate)
# denoise('round2')
# minus_pic_and_get_Hskin("round2",'H5_back','round2')

# erode('H6_back',3)


def OPEN(size,anglename):
    #对图片进行闭运算
    anglepic = cv2.imread(os.path.join(opic_ndlpath, anglename+'.png'))
    #保存闭运算后的png
    kernel= cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    angle_backpic  = cv2.morphologyEx(anglepic , cv2.MORPH_OPEN, kernel) 
    # print(angle_backpic[0][0] )   
    cv2.imwrite(os.path.join(opic_ndlpath, anglename+'.png'), angle_backpic )
    return angle_backpic

# denoise('round3')
# OPEN(3,'Final_denoise')
# # denoise('Final_denoise')