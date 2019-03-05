import os
from random import randint
import operator
from interest_sorting import interest_factor


global INPUT_FILE_NAME
global NUM_TAGS
global NUM_IMAGES
INPUT_FILE_NAME = 'Problem Statement/a_example.txt'
# INPUT_FILE_NAME = 'Problem Statement/b_lovely_landscapes.txt'
# INPUT_FILE_NAME = 'Problem Statement/c_memorable_moments.txt'



with open(INPUT_FILE_NAME) as fin:
    tag_names = []
    orientation_list = []
    num_tags_list = []
    raw_image_list = []
    # format: [(index in input file, [tag1, tag3, ...]), ...]
    horizontal_image_list = []
    vertical_image_list = []
    # read the number of images
    NUM_IMAGES = int(fin.readline())
    print('reading {} images'.format(NUM_IMAGES))
    # read the images into 
    for i in range(NUM_IMAGES):
        if (i % 1000 == 0):
            print('read {} images'.format(i))
        tokens = fin.readline().split()
        orientation_list.append(tokens[0] == 'H')
        num_tags_list.append(tokens[1])
        image = tokens[2:]
        # Seperate images into lists containing horizontal and vertical images
        if (orientation_list[-1]):
            horizontal_image_list.append((i, image))
        else:
            vertical_image_list.append((i, image))
        raw_image_list.append(image)
        for tag in raw_image_list[-1]:
            tag_names.append(tag)
    print('Finished reading file')
    print('The least number of tags:', len(min(raw_image_list, key=lambda x: len(x))))
    print('The largest number of tags:', len(max(raw_image_list, key=lambda x: len(x))))
    # Count number of unique tags
    tag_names = list(set(tag_names))
    NUM_TAGS = len(tag_names)
    print('Number of unique tags', NUM_TAGS)
    # Generate boolean matrix of NUM_IMAGES by NUM_TAGS
    # image_matrix = [[True if (tag_names[i] in image) else False for i in range(NUM_TAGS)] for image in raw_image_list]
    # print(len(image_matrix))



def merge_tags(image_1, image_2):
    return list(set(image_1 + image_2))



def random_connect(endpoint_dict):
    # # Delete 1 connectness if total connectness is odd
    # if (sum(connectness_dict.values()) % 2 == 1):
    #     connectness_dict[image_index_list[-1]] -= 1
    # Connect nodes with 2 connectness first to ensure no 2 connectness nodes are left alone
    # one_connectness_list = []
    # two_connectness_list = []
    # for i in image_index_list:
    #     if (connectness_dict[i] == 1):
    #         one_connectness_list.append(i)
    #     elif (connectness_dict[i] == 2):
    #         two_connectness_list.append(i)
    #     else:
    #         raise('connectness_dict input to random_connect contains 0 connectness nodes')
    chosen_connections = []
    while (len(endpoint_dict) != 2 or endpoint_dict[list(endpoint_dict.keys())[0]] != list(endpoint_dict.keys())[1]):
        endpoint_list = list(endpoint_dict.keys())
        num_endpoints = len(endpoint_list)
        i = endpoint_list[randint(0, num_endpoints-1)]
        j = endpoint_list[randint(0, num_endpoints-1)]
        while (i == j):
            j = endpoint_list[randint(0, num_endpoints-1)]
        chosen_connections.append((i, j))
        end_1 = endpoint_dict.pop(i)
        end_2 = endpoint_dict.pop(j)
        endpoint_dict[end_1] = end_2
        endpoint_dict[end_2] = end_1
    global START_IMAGE
    START_IMAGE = list(endpoint_dict.keys())[0]
    return chosen_connections



# image_dict: a dicitionary with format {index in original image: tags of image i}
# connectness_dict: a dictionary with format
# endpoint_dict: a dict of endpoints of connected images: [start1:end1 ...], each endpoint recorded once
# connection_per_node: The connections tried for each image
# threshhold_percent: Takes the threshhold_percent of best connections with respect to the num images left
# connection_scale_factor: Try this more connections in next iteration ()
# giveup_threshhold: the number of images left to return random/optimal connections
def iterative_connect(image_dict, connectness_dict, endpoint_dict, connection_per_node=3, threshhold_percent=0.1, 
                       connection_scale_factor=1, giveup_threshhold=10, num_iteration=1):
    random_connections = []
    value_dict = {}
    chosen_connections = []
    image_index_list = list(image_dict.keys())
    for i in image_index_list:
        for _ in range(connection_per_node):
            j = image_index_list[randint(0, len(image_dict)-1)]
            while (j == i or endpoint_dict[i] == j):
                print('invalid j at iteration', num_iteration)
                j = image_index_list[randint(0, len(image_dict)-1)]
            if (i < j):
                random_connections.append((i, j))
            else:
                random_connections.append((j, i))
    random_connections = list(set(random_connections))
    for c in random_connections:
        value_dict[c] = interest_factor(image_dict[c[0]], image_dict[c[1]])
    # sorted_connections: [((i, j), interest_value)]
    sorted_connections = sorted(value_dict.items(), key=operator.itemgetter(1))
    # Take the threshhold amount of connections and apply iteratively for unconnected edges
    best_connections = sorted_connections[-int(len(image_dict)*threshhold_percent):]
    for c in range(len(best_connections)-1, -1, -1):
        i = best_connections[c][0][0]
        j = best_connections[c][0][1]
        if (connectness_dict[i] != 0 and connectness_dict[j] != 0 and endpoint_dict[i] != j):
            connectness_dict[i] -= 1
            connectness_dict[j] -= 1
            chosen_connections.append((i, j))
            # Delete entries of i and j, then modify i and j's original endpoints to point to each other
            end_1 = endpoint_dict.pop(i)
            end_2 = endpoint_dict.pop(j)
            endpoint_dict[end_1] = end_2
            endpoint_dict[end_2] = end_1
    # Calculate the remaining nodes
    new_image_dict = {}
    new_connectioness_dict = {}
    for i in image_index_list:
        if (connectness_dict[i] != 0):
            new_image_dict[i] = (image_dict[i])
            new_connectioness_dict[i] = (connectness_dict[i])

    # if (num_iteration > 20):
    #     print('endpoint_dict:', endpoint_dict)

    # Recursive Step
    if (len(new_image_dict) > giveup_threshhold):
        # Call self again
        return chosen_connections + iterative_connect(new_image_dict, new_connectioness_dict, endpoint_dict,
                                                     connection_per_node=(connection_per_node+connection_scale_factor),
                                                     threshhold_percent=threshhold_percent, 
                                                     connection_scale_factor=connection_scale_factor,
                                                     num_iteration=(num_iteration+1))
    else:
        # Base Case: Return random connections
        print('remaining connectioness_dict:', new_connectioness_dict)
        print('remaining image_dict:', new_image_dict)
        print('total iterations:', num_iteration)
        return random_connect(endpoint_dict)



def check_connection(connections, start):
    heads = []
    tails = []
    walk = [start]
    for c in connections:
        heads.append(c[0])
        tails.append(c[1])
    current_node = start
    for _ in range(len(connections)):
        if current_node in heads:
            i = heads.index(current_node)
            heads.pop(i)
            current_node = tails.pop(i)
        elif current_node in tails:
            i = tails.index(current_node)
            tails.pop(i)
            current_node = heads.pop(i)
        else:
            print(len(walk))
            raise('Connection broken from image {}'.format(current_node))
        walk.append(current_node)
    print(walk)



# merge random vertical images together, last image is discarded if num_vertical_image is odd
merged_image_list = horizontal_image_list
for i in range(0, len(vertical_image_list), 2):
    merged_image_list.append(((vertical_image_list[i][0], vertical_image_list[i+1][0]), 
                               merge_tags(vertical_image_list[i][1], vertical_image_list[i+1][1])))
# format inputs for iterative_connect
connectness_dict = {}
image_dict = {}
endpoint_dict = {}
index_lookup_dict = {} # {new_index: (i, j), new_index: k, ...}
for i in range(len(merged_image_list)):
    index_lookup_dict[i] = merged_image_list[i][0]
    image_dict[i] = merged_image_list[i][1]
    connectness_dict[i] = 2
    # Construct endpoint dict for init: {0:0, 1:1, 2:2 ...}
    endpoint_dict[i] = i
# drop two connections for the start and end
connectness_dict[len(connectness_dict)-1] = 1
connectness_dict[len(connectness_dict)-2] = 1
connections = (iterative_connect(image_dict, connectness_dict, endpoint_dict, connection_per_node=1, 
                        threshhold_percent=0.15, connection_scale_factor=2))
print('START>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', START_IMAGE)

check_connection(connections, START_IMAGE)