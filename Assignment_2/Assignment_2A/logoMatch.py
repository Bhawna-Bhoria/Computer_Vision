# -*- coding: utf-8 -*-
"""logoMatch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GrYhm3muCBl7vQNTrM2JGDei-n_eGFYz
"""

#@title Importing the libraries

import cv2
import numpy as np
import glob
from google.colab.patches import cv2_imshow
from matplotlib import pyplot as plt

#@title SIFT Method

def SIFT_find_match(image,logo):
  sift = cv2.SIFT_create()

  kp_logo, des_logo = sift.detectAndCompute(logo, None)
  kp_scene, des_image = sift.detectAndCompute(image, None)
  matcher = cv2.FlannBasedMatcher()

  matches = matcher.knnMatch(des_logo, des_image, k=2)
  good_matches = []
  for m,n in matches:
    if m.distance < 0.6*n.distance:
      good_matches.append(m)
  print(f"Number of good matches are {len(good_matches)}")
  return len(good_matches)

def SIFT_show_match(image,logo):
  sift = cv2.SIFT_create()

  kp_logo, des_logo = sift.detectAndCompute(logo, None)
  kp_scene, des_scene = sift.detectAndCompute(image, None)
  matcher = cv2.FlannBasedMatcher()

  matches = matcher.knnMatch(des_logo, des_scene, k=2)
  good_matches = []
  for m,n in matches:
    if m.distance < 0.6*n.distance:
      good_matches.append(m)
  result = cv2.drawMatches(logo, kp_logo, image, kp_scene, good_matches, None)
  cv2_imshow(result)

#@title Example 1 Using SIFT
path = "/content/logos/*.*"
image1 = cv2.imread('levis_image.jpg')
final_logo=None
n=0
curr_matches=0
for file in glob.glob(path):
   print(file)
   logo= cv2.imread(file)
   n=SIFT_find_match(image1,logo)
   if n>curr_matches:
     final_logo = logo
     curr_matches=n
print("Matched logo is")
cv2_imshow(final_logo)
SIFT_show_match(image1,final_logo)

#@title Example 2 Using SIFT
path = "/content/example2/logos/*.*"
image2 = cv2.imread('/content/example2/starbucks_image.jpeg')
final_logo=None
n=0
curr_matches=0
for file in glob.glob(path):
   print(file)
   logo= cv2.imread(file)
   n=SIFT_find_match(image2,logo)
   if n>curr_matches:
     final_logo = logo
     curr_matches=n
print("Matched logo is")
cv2_imshow(final_logo)
SIFT_show_match(image2,final_logo)

#@title ORB Method

def ORB_find_match(image, logo):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    kp_logo, des1 = orb.detectAndCompute(image_gray, None)
    kp_scene, des2 = orb.detectAndCompute(logo_gray, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    match_count=0
    for i in range(len(matches)):
      match=matches[i]
      if match.distance > 70:
        match_count+=1
    print(f"Number of good matches are {match_count}")
    return match_count
def ORB_show_match(image, logo):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    kp_logo, des1 = orb.detectAndCompute(image_gray, None)
    kp_scene, des2 = orb.detectAndCompute(logo_gray, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    img3 = cv2.drawMatches(image, kp_logo, logo, kp_scene, matches[:5], None, flags=2)
    cv2_imshow(img3)

#@title Example 1 Using OBR
path = "/content/logos/*.*"
image1 = cv2.imread('levis_image.jpg')
final_logo=None
n=0
curr_matches=0
for file in glob.glob(path):
   print(file)
   logo= cv2.imread(file)
   n=ORB_find_match(image1,logo)
   if n>curr_matches:
     final_logo = logo
     curr_matches=n
print("Matched logo is")
cv2_imshow(final_logo)
ORB_show_match(image1,final_logo)

#@title Example 2 Using OBR
path = "/content/example2/logos/*.*"
image2 = cv2.imread('/content/example2/starbucks_image.jpeg')
final_logo=None
n=0
curr_matches=0
for file in glob.glob(path):
   print(file)
   logo= cv2.imread(file)
   n=ORB_find_match(image2,logo)
   if n>curr_matches:
     final_logo = logo
     curr_matches=n
print("Matched logo is")
cv2_imshow(final_logo)
ORB_show_match(image2,final_logo)



#@title Template Matching

def template_matching(image, logo):
  img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  template = cv2.imread(logo, 0)
  width, height = template.shape[::-1]
  res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
  thresh = 0.4
  loc = np.where(res >= thresh)
  match_count=0
  for pt in zip(*loc[::-1]):
    cv2.rectangle(image, pt, (pt[0] + width, pt[1] + height), (0, 255, 255), 2)
    match_count+=1
  print(match_count)
  return match_count

#@title Example 1 Using Template Matching
path = "/content/logos/*.*"
image1 = cv2.imread('levis_image.jpg')
final_logo=None
n=0
curr_matches=0
for file in glob.glob(path):
   print(file)
  #  logo= cv2.imread(file)
   n=template_matching(image1,file)
   if n>curr_matches:
     final_logo = file
     curr_matches=n
print("Matched logo is")
cv2_imshow(cv2.imread(final_logo))

#@title Example 2 Using Template Matching
path = "/content/example2/logos/*.*"
image2 = cv2.imread('/content/example2/starbucks_image.jpeg')
final_logo=None
n=0
curr_matches=0
for file in glob.glob(path):
   print(file)
  #  logo= cv2.imread(file)
   n=template_matching(image2,file)
   if n>curr_matches:
     final_logo = file
     curr_matches=n
print("Matched logo is")
cv2_imshow(cv2.imread(final_logo))