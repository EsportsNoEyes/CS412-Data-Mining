import sys
import math

def updateDistanceMatrix(clusters, D, p, q):
    # Update distance related to p since p < q
    new_D = {}
    new_D.update(D)
    for k,v in D.items():
        if k != p and k != q:
            new_dist = min(D[k][p],D[k][q])
            new_D[k][p] = new_dist
            new_D[p][k] = new_dist
            del new_D[k][q]       
    del new_D[q]
    del new_D[p][q]
    return new_D

def initDistanceMatrix(clusters, data):
    # Initialize distance matrix
    D = {}
    for i in range(0,len(data)): 
        temp = {}
        for j in range(0,len(data)):
            # Only deal with entry with index j != i
            if j != i:
                dist = getClusterMinDist(clusters[i],clusters[j],data)
                temp[j] = dist
        D[i] = temp
    return D

def getClusterMinDist(c1, c2, data):
    # c1, c2: list of clusters
    # Calculate the minimum distance between two clusters using single link
    distances = []
    for i in c1:
        for j in c2:
            d = l2norm(i,j)
            distances.append(d)
    return min(distances)

def l2norm(p1, p2):
    # Calculate Euclidean distance between two points
    ret = 0
    for i in range(len(p1)):
        ret = ret + math.pow(abs(p1[i]-p2[i]),2)
    return math.sqrt(ret)

def findMinDist(D):
    # Find the minimum distance in the distance matrix and its index
    min_dist = 99999
    min_index = []
    for k1,v1 in D.items():
        for k2,v2 in v1.items():
            if v2 < min_dist :
                min_dist = v2
    for k1,v1 in D.items():
        for k2,v2 in v1.items():
            if v2 == min_dist:
                min_index.append(tuple((k1,k2)))
    # make sure p < q
    sorted_mins = sorted(min_index,key=lambda x:(x[0],x[1]))
    ret_index = sorted_mins[0]
    return min_dist, ret_index[0], ret_index[1]

# N points and k final clusters
line = input().rstrip().split(' ')
pts_num = int(line[0])
cls_num = int(line[1])

# Set N data points as N clusters
count = 0
data = {}
clusters = {}
cids = {}
for i in range(pts_num):
    line = input().rstrip().split(' ')
    tup = tuple([float(c) for c in line])
    data[count] = tup
    clusters[count] = []
    clusters[count].append(tup)
    cids[count] = []
    cids[count].append(count)
    count = count + 1
data_num = len(data)

# Set initial distance matrix D
D = initDistanceMatrix(clusters,data)

while data_num > cls_num:
    # p < q
    min_dist, p, q = findMinDist(D)
    clusters[p].extend(clusters[q])
    clusters[p] = sorted(clusters[p])
    del clusters[q]
    # update cids
    cids[p].extend(cids[q])
    cids[p] = sorted(cids[p])
    del cids[q]
    # update distance matrix
    D = updateDistanceMatrix(clusters, D, p, q)
    data_num = data_num - 1

for v in data.values():
    for cid, pts in clusters.items():
        if v in pts:
            print(cid)
