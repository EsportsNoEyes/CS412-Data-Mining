import sys

# setup thresholds
minsup = 2
minlen = 2
maxlen = 5

# handle inputs
seq_db = []
for line in sys.stdin:
    seq_db.append(line.rstrip().split(' '))
    
# generate and prune patterns
temp = {}
c_freq = {}
for seq in seq_db:
    for i in seq:
        if not i in temp.keys():
            temp[i] = 1
        else:
            temp[i] = temp[i] + 1
for pattern in temp.keys():
    if temp[pattern] >= minsup:
        c_freq[pattern] = temp[pattern]

# start from generating length=2 patterns
res = {}
length = 2
while len(c_freq) > 0:
    temp = {}
    pruned = {}
    for seq in seq_db:
        for i in range(0,len(seq)-length+1):
            tmp = ' '.join(seq[i:i+length-1])
            if tmp in c_freq.keys():
                tmp = ' '.join(seq[i:i+length])
                if not tmp in temp.keys():
                    temp[tmp] = 1
                else:
                    temp[tmp] = temp[tmp] + 1
    for pattern in temp.keys():
        if temp[pattern] >= minsup:
            pruned[pattern] = temp[pattern]
    c_freq = pruned
    res.update(c_freq)
    if length+1 > maxlen:
        break
    else:
        length = length + 1

sorted_res = dict(sorted(res.items(), key=lambda x: (-x[1],x[0])))
c = 1
for k in sorted_res.keys():
    if c > 20:
        break
    sys.stdout.write('[')
    sys.stdout.write(str(sorted_res[k]))
    sys.stdout.write(', ')
    sys.stdout.write('\'')
    sys.stdout.write(k)
    sys.stdout.write('\'')
    sys.stdout.write(']')
    print()
    c = c + 1