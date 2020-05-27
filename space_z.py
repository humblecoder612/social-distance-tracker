from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import pandas as pd
import order_points

focalLength={'phone': [4.5,4.0] , 'camera': [25.0,10.0] ,'cctv': [7.0,2.6] }

def z_distance(real_height,im_height,pixel_height,focalType):
    real_height=real_height
    upper= focalLength[focalType][0]*real_height*pixel_height
    lower=im_height*focalLength[focalType][1]
    return (upper/lower)
    


