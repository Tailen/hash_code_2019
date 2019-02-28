import os
import numpy as np

global NUM_TAGS
global NUM_IMAGES

NUM_IMAGES = 10
NUM_TAGS = 3

## Function to get the interest factor of two images
## We find the common and the existant in image_1 but not image_2
## Then we get the minimum of these 3 values
def interest_factor(image_1, image_2):
    common, in_image_1 = 0, 0
    for i in range(len(image_1)):
        if (image_1[i] in image_2):
            common+=1
        else: 
            in_image_1+=1
    return min(common, in_image_1, len(image_1) - in_image_1)

## Function that swaps two elements in an array, given the array and the indexes
def swap(A, i, j):
    c = A[i]
    A[i] = A[j]
    A[j] = c

## GREEDY APPROACH FOR GETTING A SLIDESHOW
def sorting(image_matrix):
    n = 0
    while n < NUM_IMAGES-1:
        best = 0
        i = n + 1
        best_ind = n
        while i < NUM_IMAGES:
            int_factor = interest_factor(image_matrix[n], image_matrix[i])
            if (int_factor > best):
                best = int_factor
                best_ind = i
            i+=1 
        swap(image_matrix, n, best_ind)
        n = n + 1
    return image_matrix 