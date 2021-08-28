
from hard_tools import *
from sklearn.cluster import KMeans
import numpy as np
# from graham_scan import *

from GrahamScan import *



def H3_helper(H3_angle):
	#输出:H3back
	#对于空腔约束，不同的病例不同的处理方式
    if test_index==0 or test_index==1 or test_index==7 or test_index==8:
        closing(H3kernel_dic[test_index],'H3')
        if test_index==0:
        	OPEN(2,'H3_back')
    if test_index==2 or test_index==6:
        draw_contour(2,np.array(H3_angle))
    if test_index==3 or test_index==4:
        draw_contour(1,H3_angle)
    if test_index==5 :
        sort(H3_angle)
        #draw_contour(3,np.array(H3_angle))






def sort(H3_angle):
	#对test_index==5的H3的scatter进行分类，然后凸包检测
	sort1=[]
	sort2=[]
	sort3=[]
	contours=[]
	for ele in H3_angle:
		if ele[1]<50:
			sort1.append(ele)

		elif ele[1]<222:
			sort2.append(ele)
			helper=GrahamScan(np.array(sort2))
			contour=np.array([helper])
		else:
			sort3.append(ele)
			helper=GrahamScan(np.array(sort3))
			contour=np.array([helper])
	helper=GrahamScan(np.array(sort1))
	contour=np.array([helper])
	contours.append(contour)
	helper=GrahamScan(np.array(sort2))
	contour=np.array([helper])
	contours.append(contour)
	helper=GrahamScan(np.array(sort3))
	contour=np.array([helper])
	contours.append(contour)
	img = cv2.imread(os.path.join(head, 'bg.png')) 
	img = cv2.drawContours(img, contours, -1, (173,205,249),  cv2.FILLED)
	cv2.imwrite(os.path.join(opic_ndlpath, 'H3_back.png'), img)



def draw_contour(num,data):
	#对于聚类效果比较好的case，直接聚类然后画凸包
	if num>1:
		kmeans=KMeans(n_clusters=num) 
		kmeans.fit(data) 

		label = kmeans.labels_ # 获取聚类标签
		contours=[]
		for i in range(num):
			sub = data[label == i]
			helper=GrahamScan(sub)
			contour=np.array([helper])
			contours.append(contour)
		#print(contours)
	else:
		helper=GrahamScan(np.array(data))
		contours=np.array([helper])
	img = cv2.imread(os.path.join(head, 'bg.png')) 
	img = cv2.drawContours(img, contours, -1, (173,205,249),  cv2.FILLED)
	cv2.imwrite(os.path.join(opic_ndlpath, 'H3_back.png'), img)