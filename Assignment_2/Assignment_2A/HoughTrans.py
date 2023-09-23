# -*- coding: utf-8 -*-
"""HoughTrans.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DPCI4U8U_RYBunCKYKnDpNkjH73OUqUF
"""

#@title Importing the Libraries
import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow

#@title Hough Line Detection

shapes = cv2.imread('building.jpg')
cv2_imshow(shapes)
shapes_grayscale = cv2.cvtColor(shapes, cv2.COLOR_RGB2GRAY)

canny_edges = cv2.Canny(shapes_grayscale, 100, 200)
cv2_imshow(canny_edges)

def peaks_function(H, num_lines, mark=0, env_size=3):
    H1 = np.copy(H)
    indicies = []
    for i in range(num_lines):
        indices = np.argmax(H1)
        H1_indices = np.unravel_index(indices, H1.shape)
        indicies.append(H1_indices)
        indices_y, indices_x = H1_indices
        if (indices_x - (env_size/2)) < 0: min_x = 0
        else: min_x = indices_x - (env_size/2)
        if ((indices_x + (env_size/2) + 1) > H.shape[1]): max_x = H.shape[1]
        else: max_x = indices_x + (env_size/2) + 1
        if (indices_y - (env_size/2)) < 0: min_y = 0
        else: min_y = indices_y - (env_size/2)
        if ((indices_y + (env_size/2) + 1) > H.shape[0]): max_y = H.shape[0]
        else: max_y = indices_y + (env_size/2) + 1
        print(min_x, max_x,min_y, max_y)
        min_y = min_y.astype(int)
        max_y = max_y.astype(int)
        min_x = int(min_x)
        max_x = int(max_x)
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                H1[y, x] = 0
                if (x == min_x or x == (max_x - 1)):
                    H[y, x] = 255
                if (y == min_y or y == (max_y - 1)):
                    H[y, x] = 255
    return indicies, H

def accumulator_function(input_image, rr=1, tr=1):
    h, w = input_image.shape
    image_side = np.ceil(np.sqrt(h**2 + w**2))
    thetas = np.deg2rad(np.arange(-90, 90, tr))
    rhos = np.arange(-image_side, image_side + 1, rr)
    H = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)
    y_indices, x_indices = np.nonzero(input_image)

    for i in range(len(x_indices)):
        x = x_indices[i]
        y = y_indices[i]

        for j in range(len(thetas)):
            rho = int((x * np.cos(thetas[j]) +
                       y * np.sin(thetas[j])) + image_side)
            H[rho, j] += 1

    return H, rhos, thetas

def plot_hough_acc(H, title='Hough Accumulator Plot'):
    fig = plt.figure(figsize=(10, 10))
    fig.canvas.set_window_title(title)
    	
    plt.imshow(H, cmap='jet')

    plt.xlabel('Theta Direction'), plt.ylabel('Rho Direction')
    plt.tight_layout()
    plt.show()

def hough_lines_draw(input_image, indicies, rhos, thetas):
    for i in range(len(indicies)):
        rho = rhos[indicies[i][0]]
        theta = thetas[indicies[i][1]]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(input_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

H, rhos, thetas = accumulator_function(canny_edges)
indicies, H = peaks_function(H, 10, env_size=11)
plot_hough_acc(H)
hough_lines_draw(shapes, indicies, rhos, thetas)
cv2_imshow(shapes)

#@title Hough space display for a line
image = np.zeros((150,150))
# image[75, 75] = 1
# image[50, 50] = 1
image[:, :] = np.eye(150)
# accumulator, thetas, rhos = houghLine(image)
# thetas, rhos = houghLine(image)
H, rhos, thetas = accumulator_function(image)
indicies, H = peaks_function(H, 1, env_size=10) # find peaks
plot_hough_acc(H) # plot hough space, brighter spots have higher votes
hough_lines_draw(shapes, indicies, rhos, thetas)
plt.figure('Original Image')
plt.imshow(image)
plt.set_cmap('gray')
plt.figure('Hough Space')
# plt.imshow(accumulator)
plt.set_cmap('gray')
plt.show()