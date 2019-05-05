import sys
import math

def l2norm(p1,p2):
    ret = 0
    for i in range(len(p1)):
        ret = ret + math.pow(abs(p1[i]-p2[i]),2)
    return math.sqrt(ret)

# N points and k cluster points
line = input().rstrip().split(' ')
pts_num = int(line[0])
cen_num = int(line[1])

# Store data points and set initial centroids
data = {}
for i in range(pts_num):
    line = input().rstrip().split(' ')
    tup = tuple([float(c) for c in line])
    data[tup] = -1

count = 0
centroids = {}
for line in sys.stdin:
    line = line.rstrip().split(' ')
    tup = tuple([float(c) for c in line])
    centroids[tup] = count
    count = count + 1
# print(centroids)
# print(data)
# print(centroids)

# K-means main loop
while True:
    stop_flag = True
    for pt in data.keys():
        distances = {}
        for cen,cid in centroids.items():
            dist = l2norm(pt,cen)
            distances[cid] = dist
        sorted_distances = sorted(distances.items(),key=lambda x:(x[1],[0]))
        if data[pt] != sorted_distances[0][0]:
            data[pt] = sorted_distances[0][0]
            stop_flag = False
    if stop_flag:
        break
    else:
        new_centroids = {}
        datacopy = {}
        datacopy.update(data)
        for i in range(count):
            temp = []
            for pt,cid in data.items():
                if cid == i:
                    temp.append(pt)
            n = len(temp)
            c_mean = tuple(sum(x)/n for x in zip(*temp))
            new_centroids[c_mean] = i
        centroids = new_centroids
     
for cid in data.values():
    print(cid)