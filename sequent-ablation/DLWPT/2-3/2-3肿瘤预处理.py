import cv2
import numpy as np
from PIL import Image
#图1
# a = Image.open("a.png")
# b = Image.open("b.png")
# for x in range(512):
# 	for y in range(512):
# 		if b.getpixel((x,y))==(255,255,255):
# 			if a.getpixel((x,y))==(255,160,122):
# 				a.putpixel([x,y],(200,200,200))
# 			elif a.getpixel((x,y))==(0,0,0):
# 				a.putpixel([x,y],(255,0,0))
# a.save("c.png")
#图2-36

# a = Image.open("gall.png")
# c = Image.open("tmr.png")
# for x in range(512):
# 	for y in range(512):
# 		if a.getpixel((x,y))==(255,255,255):
# 			a.putpixel([x,y],(255,182,193))
# 		if c.getpixel((x,y))==(255,255,255):
# 			c.putpixel([x,y],(105,105,105))
# c.save("tmr.png")
# a.save("gall.png")

# b = Image.open("diled.png")
# a = Image.open("gall.png")
# c = Image.open("tmr.png")
# for x in range(512):
# 	for y in range(512):
# 		if b.getpixel((x,y))==(255,255,255):
# 			if c.getpixel((x,y))==(0,0,0):
# 				c.putpixel([x,y],(200,200,200))
# 			# else:
# 			# 	b.putpixel([x,y],(255,0,0))
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