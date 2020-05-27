from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import pandas as pd
import order_points
import space_z
import math

image='img.jpg'
width=15.0 #inches

# numpy taken
rec = np.loadtxt("yolo_new.txt")
ind = np.argsort( rec[:,0] )
rec = rec[ind]
rec_sort=rec
#image
test=cv2.imread(image)
im=test.copy()

#view
view='none'

#some functions 
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def center(a,b):
    return (a+b)*0.5

mid=[]
PPI=0
D=0
for i in range(0,len(rec_sort)-1):
    box_1 = rec_sort[i]
    box_2 = rec_sort[i+1]
    cX_1,cX_2 = center(box_1[0],box_1[2]), center(box_2[0],box_2[2])
    cY_1,cY_2 = center(box_1[1],box_1[3]), center(box_2[1],box_2[3])
    cZ_1,cZ_2=z_point=space_z.z_distance(65,box_1[3]-box_1[1],test.shape[0],'camera'),space_z.z_distance(65,box_2[3]-box_2[1],test.shape[0],'camera')
    ppi_box=order_points.rect_per(box_1)
    (tl, tr, br, bl)=order_points.order_points_new(ppi_box)
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    '''(tlblX,tlblY) = midpoint(ppi_box[0],ppi_box[1])
    (trbrX,trbrY) = midpoint(ppi_box[2],ppi_box[3])'''
    PPE=dist.euclidean((tlblX, tlblY,cZ_1), (trbrX, trbrY,cZ_1))
    PPI=PPE/width
    mid.append([cX_1,cY_1,cZ_1,cX_2,cY_2,cZ_2])



i=0
for one,two,three,four,five,six in mid: 
    if view!='fish-eye':
        counter=list(range(90-(10*len(rec_sort-1)),90,5))
        angles=[angle*np.pi/180. for angle in counter]
    else:
        angles=[90]*len(rec_sort-1)
    D = ((dist.euclidean((one, two,three), (four,five,six)))/(math.sin(angles[i])) ) / PPI

    (mX, mY) = midpoint((one, two), (four, five))
    
    if D>72:
        cv2.line(im,(int(one),int(two)),(int(four),int(five)),color=(0,255,0),thickness=2)
        cv2.putText(im, "accepted {:.1f}in".format(D), (int(mX-10), int(mY -10)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,0), 2)
    elif D>60:
        cv2.line(im,(int(one),int(two)),(int(four),int(five)),color=(255,0,0),thickness=2)
        cv2.putText(im, "somewhat accepted {:.1f}in".format(D), (int(mX+10), int(mY -10)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,0,0), 2)
    else:
        cv2.line(im,(int(one),int(two)),(int(four),int(five)),color=(0,0,255),thickness=2)
        cv2.putText(im, "not accepted {:.1f}in".format(D), (int(mX-10), int(mY -10)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,255), 2)

    i=i+1
cv2.imshow('image',im)
resized = imutils.resize(im, width=600)
cv2.imwrite('example3.jpg',im)
cv2.imwrite('example3_resized.jpg',resized)
cv2.waitKey(0)