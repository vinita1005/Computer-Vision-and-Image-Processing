#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def write_image(img, img_saving_path):
    """Writes an image to a given path.
    """
    if isinstance(img, list):
        img = np.asarray(img, dtype=np.uint8)
    elif isinstance(img, np.ndarray):
        if not img.dtype == np.uint8:
            assert np.max(img) <= 1, "Maximum pixel value {:.3f} is greater than 1".format(np.max(img))
            img = (255 * img).astype(np.uint8)
    else:
        raise TypeError("img is neither a list nor a ndarray.")

    cv.imwrite(img_saving_path, img)

# In[ ]:

def test(img, coords):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Arrow, Circle
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    for i in coords:
        ax.add_patch(Circle((i[0],i[1]), radius=1, color='red'))
    plt.show(fig) 


# In[ ]:


def testKeypoints(img, kps1):
    img2 = cv.drawKeypoints(img, kps1, None, color=(255,0,0), flags=0)
    plt.imshow(img2), plt.show()


# In[ ]:


def testMatches(img1, kps1, img2, kps2):
    img = cv.drawMatches(img1, kps1, img2, kps2,matches[:10])
    plt.imshow(img), plt.show()


# In[ ]:

##Detecting key points using ORB##
def detectKeypoints(img):
    "ORB syntax implementation referenced from opencv documentation:"
    "https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html"
    orb = cv.ORB_create()
    k = orb.detect(img,None)
    k, d = orb.compute(img, k)
    return k, d


# In[ ]:

##Feature Detection algorithm##
def getFeatures(img1, img2, threshold):
    kps1, desc1 = detectKeypoints(img1)
    kps2, desc2 = detectKeypoints(img2) 
    pairwiseDistances = cdist(desc1, desc2, 'hamming')

    Y = np.where(pairwiseDistances < threshold)
    points_in_img1 = Y[0]
    points_in_img2 = Y[1]
    coordinates_in_img1 = []
    coordinates_in_img2 = []

    for point in points_in_img1:
        coordinates_in_img1.append(kps1[point].pt)
    for point in points_in_img2:
        coordinates_in_img2.append(kps2[point].pt)

    #testKeypoints(img1, kps1)
    #testKeypoints(img2, kps2)
    
    matched_coords = [[]]
    
    try:
        matched_coords = np.concatenate( (coordinates_in_img1, coordinates_in_img2) , axis=1 )
    except: print("No matching coordinates")
    
    
    #print(matched_coords)
    return matched_coords


# In[ ]:


def getHomographyMatrix(matched_coords):
    count = 0
    max_inliers = 0
    H = []
    for i in range(1000):
        current_h, count = ransac_algo(matched_coords)
        if count > max_inliers:
            max_inliers = count
            H = current_h
    print("Best homography: ",H)
    print("Most inliers: ",max_inliers)
    return H


# In[ ]:


def ransac_algo(matched_coords):
    import random
    "Ransac algorithm for feature matching implemented as per approach in the Szeliski book"
    pairs = []
    pairs.append(random.choice(matched_coords))
    pairs.append(random.choice(matched_coords))
    pairs.append(random.choice(matched_coords))
    pairs.append(random.choice(matched_coords))
   
    matched_coords = np.asarray(matched_coords)
    current_h = computeHomographyMatrix(pairs)
    current_h = np.asarray(current_h)
    
    p1 = np.concatenate((matched_coords[:, 0:2], np.ones((len(matched_coords),1))), axis=1)
    p2 = matched_coords[:, 2:4]
    new_points = np.zeros((len(matched_coords), 2))
    
    for i in range(len(matched_coords)):
        temp = np.matmul(current_h, p1[i])
        new_points[i] = (temp/temp[2])[0:2]

    errors = np.linalg.norm(p2 - new_points, axis=1) ** 2
    idx = np.where(errors < 0.5)[0] 
    count = len(matched_coords[idx])
    
    return current_h, count


# In[ ]:

##Homography matrix computation for current pair of images##
def computeHomographyMatrix(pairs):
    "Computing the Homography matrix using the equation Ah=b"
    Amatrix = []
    for i in range(0, len(pairs)):
        x1, y1 = pairs[i][0], pairs[i][1]
        x2, y2 = pairs[i][2], pairs[i][3]
        Amatrix.append([-x1, -y1, -1, 0, 0, 0, x2*x1, x2*y1, x2])
        Amatrix.append([0, 0, 0, -x1, -y1, -1, y2*x1, y2*y1, y2])
    Amatrix = np.matrix(Amatrix)
    u, s, v = np.linalg.svd(Amatrix)
    L = v[-1,:] / v[-1,-1]
    homography = L.reshape(3, 3).transpose()
    return homography.T


# In[ ]:


def warpImages(H, colorImg1, colorImg2,idx):

    ##"Implemented according to the syntax of opencv documentation: https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html"
    
    p_height = int(colorImg2.shape[0] + colorImg1.shape[0]*0.3)
    p_width = int(colorImg2.shape[1] + colorImg1.shape[1]*0.6) 
    #filename = "./warp"+str(idx)+".jpg"
    result = cv.warpPerspective(colorImg1, H,( p_width, p_height))        
    result[0:colorImg2.shape[0], 0:colorImg2.shape[1]] = colorImg2
    #cv.imwrite(filename, result)
    cv.imwrite("./panoramaTest1b.jpg", result)
    return result


# In[ ]:


def crop_image(path):
    
    warp_img = cv.imread('./panoramaTest1b.jpg', 1)
    warp_img = np.array(warp_img)
    
    cnt, x_max, y_max = countBlackSpots(warp_img)

    final_panaroma = warp_img[0:x_max+1,0:y_max+1, :]
    try: 
        os.remove(path + 'panorama.jpg')
    except: pass
    cv.imwrite(path + 'panorama.jpg', final_panaroma)


# In[ ]:

##Will be used to crop the final image##
def countBlackSpots(result):
    black = np.zeros(3)
    x_max = 0
    y_max = 0
    count = 0
    for x in range(len(result)):
        for y in range(len(result[0])):
            I = result[x,y]
            if not np.array_equal(I, black):
                if x > x_max:
                    x_max = x
                if y > y_max:
                    y_max = y
                count = count + 1
    return count, x_max, y_max        


# In[ ]:


def buildPanaroma(matched_coords, cim, cim_next, i):
    print("Getting homography matrix")
    H = getHomographyMatrix(matched_coords)
    print("Getting warped Images")
    result = warpImages(H, cim, cim_next, i)
    print("Building final panaroma")
    return result


# In[ ]:

##Obtain the best features from all the matches##
def getBestMatch(img1, img2):
    matched_coords = getFeatures(img1, img2, 0.10)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.20)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.25)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.30)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.35)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.40)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.45)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.50)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.55)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.60)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.65)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.70)
    if len(matched_coords) < 20:
        matched_coords = getFeatures(img1, img2,0.75)
    if len(matched_coords) < 20:   
        matched_coords = getFeatures(img1, img2,0.80)
    return matched_coords


# In[ ]:


def isMatchLeft(img1, p1):
    
    center_x = int(img1.shape[0]/2)
    center_y = int(img1.shape[1]/2)
    #p1 = matched_coords[:, 0:2]
    #print(p1)
    count = 0
    rt = 0
    
    for x in p1:
        if x[0] < center_x:
            #print("X is: ", x[0],"Center: ",center_x)
            count = count + 1
        else:
            rt = rt + 1
    
    print("Right count: ",rt)
    print("Left count: ",count)
    if count > rt:
        return True
    else:
        return False


# In[ ]:


import argparse
import copy
import os
import glob
import sys

import cv2 as cv
import numpy as np
from PIL import Image

from matplotlib import pyplot as plt
import IPython

from scipy.spatial.distance import cdist

# import time
# start_time = time.time()

from datetime import datetime
startTime = datetime.now()

##Code starts here##
print("Hello")
print(sys.argv[1])

try: 
    os.remove(sys.argv[1] + 'panorama.jpg')
except: pass

##GrayScale image, used for feature detection and matching
img = [cv.imread(file,0) for file in glob.glob(sys.argv[1] + "*")]
img = np.array(img)

##Colored images, used for matching
colorImages = [cv.imread(file,1) for file in glob.glob(sys.argv[1] + "*")]
print("Initializing panorama")
idx = 0
cnt = 0
while len(img)!=1 and len(colorImages)!=1:   
    print(len(img))
    print(len(colorImages))
    anchor = img[0]
    anchor_clr = colorImages[0]
    total_matches = 0
    anchor_matches = []
    for i in range(len(img)):
        if i!=0:
            print("Finding matches for anchor, img",i)
            ##Get features for comparision with anchor image##
            matched_coords = getFeatures(anchor, img[i], 0.40)
            
            if len(matched_coords)!=0:
                print("Found matches")
                if(total_matches < len(matched_coords)):
                    total_matches = len(matched_coords)
                    anchor_matches = matched_coords
                    anchor_next = img[i]
                    anchor_clr_next = colorImages[i]
                    idx = i
    if total_matches == 0:
        print("No matching images found")
        img = np.delete(img, 0, axis=0)
    else:
        ##Get the best features out of all the matches##
        anchor_matches = np.array(getBestMatch(anchor, anchor_next))
#         test(anchor_clr, anchor_matches[:, 0:2])
#         test(anchor_clr_next, anchor_matches[:, 2:4])
        
        new_img = []
        ##Build panorama for the current pair of images##
        colorImages[0] = buildPanaroma(anchor_matches, anchor_clr, anchor_clr_next, cnt)
        cnt = cnt + 1
        pan = np.array(cv.imread("./panoramaTest1b.jpg",0))
        new_img.append(pan)
        for j in range(len(img)):
            if j!=0:
                new_img.append(img[j])
        new_img = np.delete(new_img, idx, axis=0)
        img =  new_img
        colorImages = np.delete(colorImages, idx, axis=0)
##Crop the final image##
crop_image(sys.argv[1])

print("Panorama stitching completed in %s minutes" % (datetime.now() - startTime))