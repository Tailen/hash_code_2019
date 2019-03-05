# import os
# import numpy as np

# global INPUT_FILE_NAME
# global NUM_TAGS
# global NUM_IMAGES
# INPUT_FILE_NAME = 'a_example.txt'
# #INPUT_FILE_NAME = 'Problem Statement/b_lovely_landscapes.txt'

# orientation_list = []
# num_tags_list = []
# raw_image_list = []

# with open(INPUT_FILE_NAME) as fin:
#     tag_names = []
#     # read the number of images
#     NUM_IMAGES = int(fin.readline())
#     print('reading', NUM_IMAGES, 'images')
#     # read the images into 
#     for i in range(NUM_IMAGES):
#         if (i % 1000 == 0):
#             print('read 1000 images')
#         tokens = fin.readline().split()
#         orientation_list.append(tokens[0] == 'H')
#         num_tags_list.append(tokens[1])
#         raw_image_list.append(tokens[2:])
#         for tag in raw_image_list[-1]:
#             tag_names.append(tag)
#     # Count number of unique tags
#     print('Finished reading file')
#     tag_names = list(set(tag_names))
#     NUM_TAGS = len(tag_names)
#     # print(raw_image_list)
#     print(NUM_TAGS)
#     # print(tag_names)

#     image_matrix = [[True if (tag_names[i] in image) else False for i in range(NUM_TAGS)] for image in raw_image_list]
#     print(len(image_matrix))

# global NUM_TAGS
# global NUM_IMAGES

# NUM_IMAGES = 10
# NUM_TAGS = 3

# ## Function to get the interest factor of two images
# ## We find the common and the existant in image_1 but not image_2
# ## Then we get the minimum of these 3 values
# def interest_factor(image_1, image_2):
#     common, in_image_1 = 0, 0
#     for i in range(len(image_1)):
#         if (image_1[i] in image_2):
#             common+=1
#         else: 
#             in_image_1+=1
#     return min(common, in_image_1, len(image_1) - in_image_1)

## Function to get the interest factor of two images
## We find the common and the existant in image_1 but not image_2
## Then we get the minimum of these 3 values
def interest_factor(image_1, image_2):
    common = 0
    for i in range(len(image_1)):
        if (image_1[i] in image_2):
            common+=1
    return min(common, len(image_1)-common, len(image_2)-common)

## Function that swaps two elements in an array, given the array and the indexes
def swap(A, i, j):
    c = A[i]
    A[i] = A[j]
    A[j] = c

# ## For every image, we calculate the interest factor with a random other image
# ## If it is close enough to n/3, we choose that image and move to the next
# def sorting(image_matrix):
#     n = 0
#     while n < NUM_IMAGES-1:
#         best = 0
#         i = n + 1
#         best_ind = n
#         while i < NUM_IMAGES:
#             int_factor = interest_factor(image_matrix[n], image_matrix[i])
#             if (int_factor - NUM_IMAGES/3) < 2:
#                 swap(image_matrix, n+1, i)
#                 i = NUM_IMAGES
#             elif (int_factor > best):
#                 best = int_factor
#                 best_ind = i
#             i+=1 
#         if (best_ind != n) and (i != NUM_IMAGES + 1):
#             swap(image_matrix, n, best_ind)
#         n = n + 2
#     return image_matrix 
