import heapq
from bitstring import BitArray,BitStream


hCode_dict={} #dictionary to hold each character as key and the binary code as value
last_byte_length = 0 #number of bits in the byte when encoding out of 8, ignore the remaining when decoding
root_tuple = () #root node for the trie

#read through the file and create a tuple of characters and frequencies ie ((5,'c'),(7,'d')...etc)
def get_frequency(i_file):
	f_dict = {}
	f = open(i_file,'r')
	while True:
		c= f.read(1)
		if not c:
			break
		if c in f_dict:
			f_dict[c]+=1
		else:
			f_dict[c]=1
	f.close()
	tuple_list = []
	for key in f_dict:
		tuple_list.append((f_dict[key], key))
	return tuple_list

#turn the tuple of characters into a min heap.
#rebuild the heap using two tuples (nodes) at a time until all character nodes are leaf node and return the root of the new heap 
#only leaf nodes have two members, the character and freq, other nodes have three - (the sum of the two child nodes, the left node and the right node), in that order 
def gen_huff_tree(tuple_list):
	heapq.heapify(tuple_list)
	l=len(tuple_list)
	for x in xrange(1,l):
		left = heapq.heappop(tuple_list)
		right= heapq.heappop(tuple_list)
		node= (left[0]+right[0],left,right)
		heapq.heappush(tuple_list,node)
	return tuple_list[0]

#starting from the root of the tuple, traverse the tree and create binary prefix for each character, a "0" for the left node to the prefix and "1" for the right node 
def encode_from_tree(tuple_n,prefix=''):
	if len(tuple_n) == 2:
		hCode_dict[tuple_n[1]]=prefix
		print(tuple_n[1] + " is " + prefix)
	else:
		encode_from_tree(tuple_n[1], prefix+'0')
		encode_from_tree(tuple_n[2], prefix+'1')

#write the given input file to a binary file (o_file)
#first open the input file, create a string of each char replaced with the corresponding huff code ('0's and '1's)
#take the remainder in 8, size of byte of the length of the string and convert binary string to binary and save
def code_to_file(o_file,i_file):
	f = open(i_file,'r')
	coded_string=""
	while True:
		c = f.read(1)
		if not c:
			break
		coded_string+=hCode_dict[c]
	#encode code string as binary and write to file
	f.close()
	f = open(o_file,'wb')
	last_byte_length=len(coded_string)%8
	b=BitArray(bin=coded_string)
	f.write(b.tobytes())
	f.close()

#using BitArray, decode file and write to console
def decode_file(i_file,root_tuple):
	b=BitArray(filename=i_file)
	#read by byte, ignore all bits beyond last_byte_length in the last byte
	codes=b.bin
	i=0
	byteChars=len(codes)-last_byte_length
	current_node=root_tuple
	while i < byteChars:
		if len(current_node)==2:
			print current_node[1],
			current_node=root_tuple
		elif codes[i]=="0":
			current_node=current_node[1]
			i+=1
		elif codes[i] == "1":
			current_node=current_node[2]
			i+=1


raven = "theraven.txt"
oraven = "ravbinnew.bin"
root_tuple=gen_huff_tree(get_frequency(raven))
encode_from_tree(root_tuple)
code_to_file(oraven,raven)
decode_file(oraven,root_tuple)


