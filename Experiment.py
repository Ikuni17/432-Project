# This file will handle driving the experiment, outputting the results and utility functions.

import random
import sys
import math
import Cuckoo_Hashing
#import Perfect_Hashing
import Bin_Hashing
import perfection

# Using a prime number for tableSize helps the hash functions
tableSize = 104729
#tableSize = 1000099
quarterTable = int(tableSize / 4)
useQuarterTable = False
# A list filled with None to represent an array
hashTable = [None] * tableSize
# A list of values to insert, enough to reach a load factor of 1.0 theoretically
valuesToInsert = random.sample(range(sys.maxsize), tableSize)
# Shift the hash function to return the correct index in the table
# This is the original C code: shift = 32 - (int)(log(tablesize)/log(2)+0.5);
shift = 64 - int(math.log(tableSize) / math.log(2) + 0.5)

#function = perfection.make_hash(valuesToInsert)
#print(function)

# This function is called to get values for hashFun, and when rehashing for Cuckoo
def initHashList():
    tempList = []
    for i in range(3):
        tempList.append(random.randint(1, sys.maxsize))
    return tempList

# Stores the values used in hashFun
hashList1 = initHashList()
hashList2 = initHashList()

def paghHashFun(hashList, key):
    index = (hashList[0] * key) ^ (hashList[1] * key) ^ (hashList[2] * key)
    index >>= shift
    return index

# Division method
def hashFun1(key):
    if useQuarterTable:
        return key % quarterTable
    else:
        return key % tableSize


# Multiplication method
def hashFun2(key):
    if useQuarterTable:
        return math.floor(key/quarterTable) % quarterTable
    else:
        return math.floor(key / tableSize) % tableSize

# Multiplication method variant
def hashFun3(key):
    A = (math.sqrt(5) - 1) / 2
    if useQuarterTable:
        return math.floor(quarterTable * ((key * A) % 1))
    else:
        return math.floor(tableSize * ((key * A) % 1))

# Folding method
def hashFun4(key):
    r = 0
    while key:
        r, key = r + key % 100, key // 100

    if useQuarterTable:
        return r % quarterTable
    else:
        return r % tableSize

hashFunctions = [hashFun1, hashFun2, hashFun3, hashFun4]

# This was just a test, not actually a perfect hash
def perfectHash(key):
    somePrime = 15485863
    k = 1234
    index = ((k * key) % somePrime) % tableSize
    return index

# Reset hashTable
def clearTable():
    global  hashTable
    hashTable = [None] * tableSize

def test_insert():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        key = paghHashFun(hashList1, valuesToInsert[values])
        if hashTable[key] is None:
            hashTable[key] = valuesToInsert[values]
            count += 1
        else:
            key2 = paghHashFun(hashList2, valuesToInsert[values])
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
        key = perfectHash(valuesToInsert[values])
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

def test_insert3():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        check = Bin_Hashing.insert(valuesToInsert[values])
        #print(Bin_Hashing.lookup(valuesToInsert[values]))
        #Bin_Hashing.delete(valuesToInsert[values])
        if check is True:
            count+=1
        else:
            count2+=1
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))
    #print(hashTable)


print("Table Size: ", tableSize)
print()
print("Pagh Hash Function:")
test_insert()
print()
clearTable()
print("Perfect Hash Function:")
test_insert2()
print()
clearTable()
print("Bin Hashing: ")
test_insert3()
print()
clearTable()