# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys

###################Implement Apriori Algorithm###################
def generate_all_candidate(f_k):
    pattern = []
    for i in f_k.keys():
        pattern.append(i)
    # generate all combinations
    combination = []
    for i in range(0,len(pattern)-1):
        for j in range(i+1,len(pattern)):
            join_result = self_join(pattern[i],pattern[j])
            if join_result != '':
                combination.append(join_result)
    return combination
                          
def self_join(a,b):
    # If first k-1 element are the same, self join two patterns.
    # If not, continue.
    a_split = a.split(' ')
    b_split = b.split(' ')
    ret = []
    for i in range(0, len(a_split)-1):
        if a_split[i] != b_split[i]:
            return ''
        ret.append(a_split[i])
    ret.append(a_split[len(a_split)-1])
    ret.append(b_split[len(b_split)-1])
    ret = sorted(ret)
    ret = ' '.join(ret)
    return ret

def prune_candidate(candidate, tdb, minsup):
    ret = {}
    for c in candidate:
        tmp = c.split(' ')
        count = 0
        for t in tdb:
            contain = True
            for i in tmp:
                if not i in t:
                    contain = False
                    break
            if contain:
                count = count + 1
        if count >= minsup:
            ret[c] = count
    return ret

def print_answer(ans):
    for i in ans.keys():
        sys.stdout.write(str(ans[i]))
        sys.stdout.write(' ')
        sys.stdout.write('[')
        sys.stdout.write(i)
        sys.stdout.write(']')
        print()
                   
# min support
minsup = int(sys.stdin.readline().rstrip())
# candidate 1-itemset
freq_1 = {}
candidate_1 = {}
tdb = []
for line in sys.stdin:
    input = line.rstrip().split(' ')
    tmp = set()
    for item in input:
        tmp.add(item)
        if item in candidate_1.keys():
            candidate_1[item] = candidate_1[item] + 1
        else:
            candidate_1[item] = 1
    tdb.append(tmp)

# frequent 1-itemset
for c in candidate_1.keys():
    if candidate_1[c] >= minsup:
        freq_1[c] = candidate_1[c]
freq_1 = dict(sorted(freq_1.items(), key=lambda x: (-x[1], x[0])))
candidate = {}
frequent = {}   # store all of the frequent patterns here
f_k = {}
frequent.update(freq_1)
f_k.update(freq_1)  # store current frequent patterns here

# Apriori main loop
while len(f_k) > 0:
    candidate = generate_all_candidate(f_k)
    f_k = prune_candidate(candidate, tdb, minsup)
    frequent.update(f_k)

# Print formatted answer of part one
sorted_frequent = dict(sorted(frequent.items(), key=lambda x: (-x[1],x[0])))
print_answer(sorted_frequent)

###################Implement closed pattern###################
sorted_frequent = dict(sorted(frequent.items(),key=lambda x: len(x[0])))
closed_frequent = {}   # store all of the maximal frequent patterns here
frequent_list = []

for k in sorted_frequent.keys():
    frequent_list.append(k)
for i in range(0, len(frequent_list)-1):
    curr_closed = set(frequent_list[i].split(' '))
    for j in range(i+1, len(frequent_list)):
        other = set(frequent_list[j].split(' '))
        if len(other) <= len(curr_closed):
            continue
        if other.issuperset(curr_closed) and sorted_frequent[frequent_list[i]] == sorted_frequent[frequent_list[j]]:
            curr_closed = other
    closed_pattern = ' '.join(list(curr_closed))
    if not closed_pattern in closed_frequent.keys():
        closed_frequent[closed_pattern] = sorted_frequent[closed_pattern]
# Print formatted answer of part two
print()
print_answer(dict(sorted(closed_frequent.items(), key=lambda x: (-x[1],x[0]))))

###################Implement maximal pattern###################
sorted_frequent = dict(sorted(frequent.items(),key=lambda x: len(x[0])))
maximal_frequent = {}   # store all of the maximal frequent patterns here
frequent_list = []

for k in sorted_frequent.keys():
    frequent_list.append(k)
for i in range(0, len(frequent_list)-1):
    curr_max = set(frequent_list[i].split(' '))
    for j in range(i+1, len(frequent_list)):
        other = set(frequent_list[j].split(' '))
        if len(other) <= len(curr_max):
            continue
        if other.issuperset(curr_max):
            curr_max = other
    maximal_pattern = ' '.join(list(curr_max))
    if not maximal_pattern in maximal_frequent.keys():
        maximal_frequent[maximal_pattern] = sorted_frequent[maximal_pattern]
# Print formatted answer of part three
print()        
print_answer(dict(sorted(maximal_frequent.items(), key=lambda x: (-x[1],x[0]))))