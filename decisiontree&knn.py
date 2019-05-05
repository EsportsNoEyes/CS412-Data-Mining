import sys
import math

#######################Decision Tree#######################
# Decision tree structure
class Node:
    def __init__(self, depth=None, data=None, attr=None, threshold=None, left=None, right=None, index=None):
        self.depth = depth
        self.data = data
        self.attr = attr
        self.threshold = threshold
        self.left = left
        self.right = right
        self.index = index
        

def calculateGini(left, right, l_num, r_num):
    # Calculate Gini_A(D)
    total_num = l_num + r_num
    ret_left = 1
    ret_right = 1
    for l in left.values():
        ret_left = ret_left - math.pow(float(l/l_num),2)
    for r in right.values():
        ret_right = ret_right - math.pow(float(r/r_num),2)
    return float(l_num/total_num)*(ret_left) + float(r_num/total_num)*(ret_right)
        
def findThresholdMinGini(data, idx, threshold):
    left = {}
    right = {}
    cl = 0
    cr = 0
    # Split data according to threshold
    for d in data.values():
        val = float(d[idx].split(':')[1]) 
        if val <= threshold:
            left[cl] = d
            cl = cl + 1
        else:
            right[cr] = d
            cr = cr + 1
    # Calculate gini index based on the split
    left_num = len(left)
    right_num = len(right)
    total_num = left_num+right_num
    left_label = {}
    right_label = {}
    for v in left.values():
        if not v[0] in left_label.keys():
            left_label[v[0]] = 1
        else:
            left_label[v[0]] = left_label[v[0]] + 1
    for v in right.values():
        if not v[0] in right_label.keys():
            right_label[v[0]] = 1
        else:
            right_label[v[0]] = right_label[v[0]] + 1
    # print(left)
    # print(right)
    # print(left_label)
    # print(right_label)
    gini_index = calculateGini(left_label, right_label, left_num, right_num)
    return gini_index, left, right
    
def findAttributeThresholds(data, idx):
    # Generate all possible thresholds
    distinct_point = []
    threshold = []
    for d in data.values():
        val = float(d[idx].split(':')[1])           
        distinct_point.append(val)
    # print(distinct_point)
    distinct_point = sorted(list(set(distinct_point)))
    # print(distinct_point)
    # print('distinct')
    # print(distinct_point)
    # print(len(distinct_point)-1)
    # print('st')
    for j in range(0,len(distinct_point)-1):
        threshold.append((distinct_point[j]+distinct_point[j+1])/2)

    if len(threshold) == 0:
        return distinct_point
    return threshold

def findLabels(data):
    # Find the labels that appeared in the data
    labels = []
    for v in data.values():
        labels.append(v[0])
    return list(set(labels))

def majorityVoting(data):
    # Find the most common label
    count = {}
    for d in data.values():
        if not d[0] in count.keys():
            count[d[0]] = 1
        else:
            count[d[0]] = count[d[0]] + 1
    # print('voting')
    # print(count)
    sorted_count = sorted(count.items(),key=lambda x:(-x[1],x[0]))   
    # print('sortvoting')
    # print(count)
    return sorted_count[0][0]
        
def buildDecisionTree(node):
    # Stop when all instances in the node have same label or max_depth is reached
    # print('build tree')
    # print(node.data)
    # print(node.depth)
    if len(findLabels(node.data)) <= 1 or node.depth >= 2:
        return
    else:
        splits = {}
        for i in range(1,len(node.data[0])):
            # Find possible thresholds for each attribute
            threshold = findAttributeThresholds(node.data, i)
            # Calculate gini index for each threshold of the attribute and find the smallest one
            # print(threshold)
            min_gini = 2
            split_threshold = threshold[0]
            left_split = {}
            right_split = {}
            for t in threshold:
                gini_index, temp_left, temp_right = findThresholdMinGini(node.data, i, t)
                if gini_index < min_gini:
                    min_gini = gini_index
                    split_threshold = t
                    left_split.clear()
                    right_split.clear()
                    left_split.update(temp_left)
                    right_split.update(temp_right)
            # Store possible splits
            splits[i] = []
            splits[i].append(min_gini)
            splits[i].append(node.data[0][i].split(':')[0])
            splits[i].append(split_threshold)
            splits[i].append(left_split)
            splits[i].append(right_split)
        
        splits = dict(sorted(splits.items(), key=lambda x:(x[1][0],x[1][1])))
        # print('best')
        # pf = 1
        # for s in splits.values():
        #     if pf ==1:    
        #         print(s)
        #         pf =0
        # print('tttttttttttttttttttttttt')
        flag = 1
        left_node = Node(node.depth+1,None,None,None,None,None,None)
        right_node = Node(node.depth+1,None,None,None,None,None,None)
        for k,v in splits.items():
            # print('key')
            # print(k)
            if flag == 1:
                node.attr = v[1]
                node.threshold = v[2]
                left_node.data = v[3]
                right_node.data = v[4]
                node.index = k
                flag = 0
        node.left = left_node
        node.right = right_node
        
        # print('split info')
        # print(node.threshold)
        # print(node.attr)
        buildDecisionTree(left_node)
        buildDecisionTree(right_node)
        # node.attr = splits[0][1]
        # node.threshold = splits[0][2]
        # left_node = Node(node.depth+1,splits[0][3],None,None,None,None,f)
        # right_node = Node(node.depth+1,splits[0][4],None,None,None,None,f)
        # buildDecisionTree(left_node)
        # buildDecisionTree(right_node)
        # print('sssss')
        # for i in splits.values():
        #     print(i)
            
            
# Handle input database
train = {}
test = {}
c1 = 0
c2 = 0
for line in sys.stdin:
    temp = line.rstrip().split(' ')
    if temp[0] == '0':
        test[c1] = []
        for i in range(0,len(temp)):
            test[c1].append(temp[i])
        c1 = c1 + 1
    else:
        train[c2] = []
        for i in range(0,len(temp)):
            train[c2].append(temp[i])
        c2 = c2 + 1
# print(train)
# print(test)

root = Node(0,train,None,None,None,None,None)
buildDecisionTree(root)

# print('nodeeeeeeeeeeeee')
# print(root.threshold)
# print(root.attr)
# print(root.left.data)
# print(root.left.attr)
# print(root.left.threshold)
# print(root.right.attr)
# print(root.right.threshold)

# print('starttrtttttttt')
dt_prediction = []
for v in test.values():
    curr_node = root
    
    while True:
        if curr_node.attr == None :
            break
        if float(v[curr_node.index].split(':')[1]) <= curr_node.threshold:
            # print('goleft')
            curr_node = curr_node.left
        else:
            # print('goright')
            curr_node = curr_node.right
    
    dt_prediction.append(majorityVoting(curr_node.data))
# print('dt_prediction')
for p in dt_prediction:
    sys.stdout.write(p)
    sys.stdout.write('\n')
print()


#######################K-nearest neighbor#######################
knn_prediction = []
for te in test.values():
    neighbors = {}
    knn = {}
    for tr_k,tr_v in train.items():
        dist = 0
        for j in range(1,len(train[0])):
            train_val = float(tr_v[j].split(':')[1])
            test_val = float(te[j].split(':')[1])
            dist = dist + math.pow(train_val-test_val,2)
        dist = math.sqrt(dist)
        neighbors[tr_k] = []
        neighbors[tr_k].append(tr_v[0])
        neighbors[tr_k].append(dist)
    sorted_neighbors = dict(sorted(neighbors.items(), key=lambda x:(x[1][1],x[1][0])))
    counter = 0
    for k,v in sorted_neighbors.items():
        if counter < 3:
            knn[k] = v
            counter = counter+1
        else:
            break
    count = {}
    for v in knn.values():
        if not v[0] in count.keys():
            count[v[0]] = 1
        else:
            count[v[0]] = count[v[0]] + 1
    # print('not sorted')
    # print(count)
    sorted_count = sorted(count.items(), key=lambda x:(-x[1],x[0]))
    # print('sorted_count')
    # print(sorted_count)
    knn_prediction.append(sorted_count[0][0])
# print('knn_prediction')
# print(knn_prediction)
for p in knn_prediction:
    sys.stdout.write(p)
    sys.stdout.write('\n')