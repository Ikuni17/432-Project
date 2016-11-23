# This file will handle driving the experiment, outputting the results and utility functions.

import random
import sys
import math

tableSize = 104729
# A list filled with None to represent an array
hashTable = [None] * tableSize
# A list of values to insert, enough to reach a load factor of 1.0 theoretically
valuesToInsert = random.sample(range(sys.maxsize), tableSize)
# Stores the values used in hash functions
hashList1 = []
hashList2 = []
# Shift the hash function to return the correct index in the table
shift = 64 - int(math.log(tableSize) / math.log(2) + 0.5)


# print(shift)
# This is the original C code: shift = 32 - (int)(log(tablesize)/log(2)+0.5);

# This function is called to get values for the hash functions, and when rehashing for Cuckoo
def initHashList():
    tempList = []
    for i in range(3):
        tempList.append(random.randint(1, sys.maxsize))
    return tempList


# print(valuesToInsert)
# print(hashTable)

def hashFun(hashList, key):
    index = (hashList[0] * key) ^ (hashList[1] * key) ^ (hashList[2] * key)
    index >>= shift
    return index

def hashFun2(key):
    index = key % tableSize
    return index

hashList1 = initHashList()
hashList2 = initHashList()

# print("Original Value:", end=" ")
# print(valuesToInsert[0])
# key = hashFun(hashList1, valuesToInsert[0])
# print("Index:", end=" ")
# print(key)
def test_insert():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        key = hashFun(hashList1, valuesToInsert[values])
        if hashTable[key] is None:
            hashTable[key] = valuesToInsert[values]
            count += 1
        else:
            key2 = hashFun(hashList2, valuesToInsert[values])
            if hashTable[key2] is None:
                hashTable[key2] = valuesToInsert[values]
                count += 1
            else:
                #print("Double Collision moving to next element")
                count2 += 1

    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count/tableSize))
    #print(hashTable)

def test_insert2():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        key = hashFun2(valuesToInsert[values])
        if hashTable[key] is None:
            hashTable[key] = valuesToInsert[values]
            count += 1
        else:
            #print("Collision moving to next element")
            count2 += 1
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))
    #print(hashTable)

print("Table Size: ", tableSize)
print()
print("Pagh Hash Function:")
test_insert()
print()
hashTable = [None] * tableSize
print("Simple Hash Function:")
test_insert2()