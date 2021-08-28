import cv2
import numpy as np
from PIL import Image

def dilate(png_dir,dilate_dir,knl):
    pic = cv2.imread(png_dir, cv2.IMREAD_UNCHANGED)    
    kernel =cv2.getStructuringElement(cv2.MORPH_RECT,(knl,knl))
    dilate = cv2.dilate(pic, kernel)
    cv2.imwrite(dilate_dir, dilate)
    print(dilate_dir, 'is saved')


a = Image.open("a.png")
b = Image.open("b.png")
for x in range(512):
	for y in range(512):
		if b.getpixel((x,y))==(255,255,255):
			if a.getpixel((x,y))==(255,160,122):
				a.putpixel([x,y],(200,200,200))
			elif a.getpixel((x,y))==(0,0,0):
				a.putpixel([x,y],(255,0,0))
a.save("c.png")

# dilate("image_93.png","b.png",int(5/0.8))

# b = Image.open("dilated.png")
# a = Image.open("gall.png")
# c = Image.open("tmr.png")
# for x in range(512):
# 	for y in range(512):
# 		if b.getpixel((x,y))==(105,105,105):
# 			#b.putpixel([x,y],(105,105,105))
# 			if c.getpixel((x,y))==(0,0,0):
# 				c.putpixel([x,y],(200,200,200))
# c.save("diledtmr.png")

# b = Image.open("diledtmr.png")
# a = Image.open("gall.png")
# for x in range(512):
# 	for y in range(512):
# 		if a.getpixel((x,y))==(255,182,193):
# 			if b.getpixel((x,y))==(200,200,200):
# 				b.putpixel([x,y],(255,0,0))
# 			else:
# 				b.putpixel([x,y],(255,182,193))
# b.save("res.png")