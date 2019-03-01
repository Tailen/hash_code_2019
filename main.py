import os
from random import randint
import operator
from interest_sorting import interest_factor


global INPUT_FILE_NAME
global NUM_TAGS
global NUM_IMAGES
global raw_image_list
# INPUT_FILE_NAME = 'Problem Statement/a_example.txt'
INPUT_FILE_NAME = 'Problem Statement/b_lovely_landscapes.txt'


orientation_list = []
num_tags_list = []
raw_image_list = []


with open(INPUT_FILE_NAME) as fin:
    tag_names = []
    # read the number of images
    NUM_IMAGES = int(fin.readline())
    print('reading', NUM_IMAGES, 'images')
    # read the images into 
    for i in range(NUM_IMAGES):
        if (i % 1000 == 0):
            print('read {} images'.format(i))
        tokens = fin.readline().split()
        orientation_list.append(tokens[0] == 'H')
        num_tags_list.append(tokens[1])
        raw_image_list.append(tokens[2:])
        for tag in raw_image_list[-1]:
            tag_names.append(tag)
    # Count number of unique tags
    print('the largest number of tags:', len(max(raw_image_list, key=lambda x: len(x))))
    print('Finished reading file')
    tag_names = list(set(tag_names))
    NUM_TAGS = len(tag_names)
    # print(raw_image_list)
    print(NUM_TAGS)
    # print(tag_names)
    # image_matrix = [[True if (tag_names[i] in image) else False for i in range(NUM_TAGS)] for image in raw_image_list]
    # print(len(image_matrix))



def random_connect(image_list, connectness_list):
    for i in range(len(image_list)):
        while (connectness_list[i] != 0):
            for j in range(i+1, len(connectness_list)):
                # if (connectness_list
                pass



connectness_list = [2 for i in range(NUM_IMAGES)]

# connection_per_node: The connections tried for each image
# threshhold_percent: Takes the threshhold_percent of best connections and iterative_connect the rest
# connection_scale_factor: Try this times more connections in next iteration
# giveup_threshhold: the number of images left to return random/optimal connections
def iterative_connect(image_list, connectness_list, connection_per_node=3, threshhold_percent=0.1, 
                       connection_scale_factor=2, giveup_threshhold=10):
    connections = []
    value_dict = {}
    for i in range(len(image_list)):
        for _ in range(connection_per_node):
            j = randint(0, len(image_list)-1)
            while (j==i):
                print('i and j clashed')
                j = randint(0, len(image_list)-1)
            if (i < j):
                connections.append((i, j))
            else:
                connections.append((j, i))
    connections = list(set(connections))
    for c in connections:
        value_dict[c] = interest_factor(image_list[c[0]], image_list[c[1]])
    sorted_connections = sorted(value_dict.items(), key=operator.itemgetter(1))
    # Take the threshhold amount of connections and apply iteratively for unconnected edges
    pending_connections = sorted_connections[int(len(sorted_connections) * (1 - threshhold_percent)):]
    final_connections = []
    for c in pending_connections:
        i = c[0][0]
        j = c[0][1]
        if (connectness_list[i] != 0 and connectness_list[j] != 0):
            connectness_list[i] -= 1
            connectness_list[j] -= 1
            final_connections.append((i, j))
    # calculate the remaining nodes
    new_image_list = []
    new_connectioness_list = []
    for i in range(len(image_list)):
        if (connectness_list[i] != 0):
            new_image_list.append(image_list[i])
            new_connectioness_list.append(connectness_list[i])
    if (len(new_image_list) > giveup_threshhold):
        # Call self again
        return final_connections + iterative_connect(new_image_list, new_connectioness_list, 
                                                     connection_per_node=connection_per_node*connection_scale_factor,
                                                     threshhold_percent=threshhold_percent, 
                                                     connection_scale_factor=connection_scale_factor)
    else:
        # Return random connections if 
        print(new_connectioness_list)
        print(new_image_list)
        return []



print(iterative_connect(raw_image_list, connectness_list, connection_per_node=1, threshhold_percent=0.3, connection_scale_factor=2)[100:])