import sys
from random import randint
import time

#utility function for getting the sum of the freq of key within given range in a list
def sumL(freq, i, j,l_size):
	s = 0
	for k in xrange(i,j+1):
		if k<l_size: s+=freq[k]
	return s

#go through the matrix of costs by diagonals (l_size-i) and compute cost of using each new key as root
#by adding it to the minimum of the cost of using previous keys as root of subtrees
def opt_search_tree(freq,cost,b_tree,l_size):
	#the cost of setting each key as root of its own tree is the frequency of itself
	#cost is the matrix of the cost 
	#b_tree is the matrix of index of the appropriate key to use from the minimal cost computed in the matrix cost
	for i in xrange(0,l_size):
		cost[i][i]=freq[i]
		b_tree[i][i]=i

	for i in xrange(2,l_size+1):
		for j in xrange(0,(l_size-i+1)):
			k = j+i-1
			cost[j][k] = sys.maxint
			for l in xrange(j,k+1):
				c= cost[j][l-1]
				if (l+1)<l_size: c+=cost[l+1][k]
				c+=sumL(freq, j, k,l_size)
				if(cost[j][k]>c): 
					cost[j][k]=c
					b_tree[j][k] = l
	return cost[0][l_size-1]


#create the binary tree using the index matrix b_tree
#starting from the root return above, get the left and right children (i,k-1 and k+1,j respectively for root at i,j)
def tree(i,j,b_tree,key):
	#verify i and j are not out of bounds of the array and the diagoanl chains
	if (i>=len(b_tree) or j>=len(b_tree) or ((len(b_tree)-i)<(len(b_tree)-j))): return None
	k = b_tree[i][j]
	if k == -1: return None
	left = right = None
	if k>0:left = tree(i,k-1,b_tree,key)
	right = tree(k+1,j,b_tree,key)
	p = (key[k],left,right)
	return p
	
#search for a given key starting with the root node, recursively check left or right child depeding on value of key
def opt_binary_search(root_node,item):
	found = False
	if(root_node==None): 
		return found
	r=root_node[0]
	if(r==item):
		found=True
	elif(item<r):
		found = opt_binary_search(root_node[1],item)
	elif(item>r):
		found = opt_binary_search(root_node[2],item)
	return found

#regular binary search, splits list into two and returns the index of key or False if not found
def binary_search(value, items, low=0, high=None):

    high = len(items) if high is None else high
    pos = low + (high - low) / len(items)

    if pos == len(items):
        return False
    elif items[pos] == value:
        return pos
    elif high == low:
        return False
    elif items[pos] < value:
        return binary_search(value, items, pos + 1, high)
    elif items[pos] > value:
        return binary_search(value, items, low, pos)



def tests():
	key_count={}
	keys=[]
	freq=[]
	#generate random numbers between 0 and 20 and keep frequencies
	for j in xrange(0,1000000):
		i = randint(0,100)
		if i in key_count: key_count[i]+=1
		else: key_count[i]=1
	#create sorted list of generated numbers and their frequencies	
	for key in key_count:
		keys.append(key)
		freq.append(key_count[key])
	l_size= len(keys)
	cost = [[0 for x in range(l_size)] for y in range(l_size)]
	b_tree = [[0 for x in range(l_size)] for y in range(l_size)]
	keys.sort()
	#build an optimal binary search tree from the sorted keys
	randcost=opt_search_tree(freq,cost,b_tree,l_size)
	randroot=tree(0,l_size-1,b_tree,keys)

	#search for each in the sorted list using binary search
	start_time = time.time()
	for i in xrange(0,l_size):
		for j in xrange(0,freq[i]):
			binary_search(keys[i],keys)
	print("Regular Binary Search--- %s seconds ---" % (time.time() - start_time))

	#search for each key in the sorted list using the optimal tree
	start_time = time.time()
	for i in xrange(0,l_size):
		for j in xrange(0,freq[i]):
			opt_binary_search(randroot,keys[i])
	print("Optimal Binary search--- %s seconds ---" % (time.time() - start_time))

def test_work():
	keys = [3,4,6,7,11,44,2,9]
	freq = [43,12,67,45,23,43,22,12]
	l_size= len(keys)
	cost = [[0 for x in range(l_size)] for y in range(l_size)]
	b_tree = [[0 for x in range(l_size)] for y in range(l_size)]
	keys.sort()
	randcost=opt_search_tree(freq,cost,b_tree,l_size)
	randroot=tree(0,l_size-1,b_tree,keys)

	for b in b_tree:
		print b

	#for i in xrange(0,12):
	#	print(" Searching for %s in optimal tree returns %s " % (i,opt_binary_search(randroot,i)))
	#	print(" Searching for %s in binary tree returns %s \n\n" % (i,binary_search(i,keys)))

test_work()
