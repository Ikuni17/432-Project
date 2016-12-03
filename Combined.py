# This file will handle driving the experiment, outputting the results and utility functions.

import random
import sys
import math

# Using a prime number for tableSize helps the hash functions
tableSize = 1049
#tableSize = 100003
halfTable = int(tableSize / 2)
quarterTable = int(tableSize / 4)
useHalfTable = False
useQuarterTable = False
maxLoop = 10000
# A list filled with None to represent an array
hashTable = [None] * tableSize
# A list of values to insert, enough to reach a load factor of 1.0 theoretically
valuesToInsert = random.sample(range(sys.maxsize), tableSize)
# Shift the hash function to return the correct index in the table
# This is the original C code: shift = 32 - (int)(log(tablesize)/log(2)+0.5);
shift = 64 - int(math.log(tableSize) / math.log(2) + 0.5)


# function = perfection.make_hash(valuesToInsert)
# print(function)

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
    elif useHalfTable:
        return key % halfTable
    else:
        return key % tableSize


# Multiplication method
def hashFun2(key):
    if useQuarterTable:
        return math.floor(key / quarterTable) % quarterTable
    elif useHalfTable:
        return math.floor(key / halfTable) % halfTable
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


twoHashFunctions = [hashFun1, hashFun2]
fourHashFunctions = [hashFun1, hashFun2, hashFun3, hashFun4]


# This was just a test, not actually a perfect hash
def perfectHash(key):
    somePrime = 15485863
    k = 1234
    index = ((k * key) % somePrime) % tableSize
    return index


# Reset hashTable
def clearTable():
    global hashTable
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
                # print("Double Collision moving to next element")
                count2 += 1

    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))
    # print(hashTable)


def test_insert2():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        key = perfectHash(valuesToInsert[values])
        if hashTable[key] is None:
            hashTable[key] = valuesToInsert[values]
            count += 1
        else:
            # print("Collision moving to next element")
            count2 += 1
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))
    # print(hashTable)


def test_insert3():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        check = bin_insert(valuesToInsert[values])
        # print(Bin_Hashing.lookup(valuesToInsert[values]))
        # Bin_Hashing.delete(valuesToInsert[values])
        if check is True:
            count += 1
        else:
            count2 += 1
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))
    # print(hashTable)

def test_insert4():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        check = cuckoo_insert(valuesToInsert[values])
        # print(Bin_Hashing.lookup(valuesToInsert[values]))
        # Bin_Hashing.delete(valuesToInsert[values])
        if check is True:
            count += 1
        else:
            count2 += 1
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))

# This will use four hash functions instead of two and theoretically should reach load factor of 0.97 before
# failing to insert. Could potentially reach 0.99 if we map the four functions to a bin of two cells each.

# Above 8 appears to make no difference in the load factor achieved
def bin_insert(value):
    # Iterate through all four hash functions until able to insert or return false if not able
    j = 0
    while j < maxLoop:
        for i in range(len(fourHashFunctions)):
            if useQuarterTable:
                indexOffset = fourHashFunctions[i](value)
                index = indexOffset + i * quarterTable
            else:
                index = fourHashFunctions[i](value)
            if hashTable[index] is None:
                hashTable[index] = value
                return True
            # This else statement actually fails to insert at a lower load factor
            else:
                # There is an element in the index so swap them. This is the Cuckoo step and previous value will try to be hashed
                hashTable[index], value = value, hashTable[index]
        j += 1
    # print("Unable to insert")
    return False

def cuckoo_insert(value):
    # Iterate through all four hash functions until able to insert or return false if not able
    j = 0
    while j < maxLoop:
        for i in range(len(twoHashFunctions)):
            if useHalfTable:
                indexOffset = twoHashFunctions[i](value)
                index = indexOffset + i * halfTable
            else:
                index = twoHashFunctions[i](value)
            if hashTable[index] is None:
                hashTable[index] = value
                return True
            # This else statement actually fails to insert at a lower load factor
            else:
                # There is an element in the index so swap them. This is the Cuckoo step and previous value will try to be hashed
                hashTable[index], value = value,hashTable[index]
        j += 1
    # print("Unable to insert")
    return False


print("Table Size: ", tableSize)
# print()
# print("Pagh Hash Function:")
# test_insert()
# print()
# clearTable()
# print("Perfect Hash Function:")
# test_insert2()
# print()
clearTable()
useQuarterTable = True
useHalfTable = False
print("Bin Hashing: ")
test_insert3()
print()
# print(hashTable)
clearTable()
useQuarterTable = False
useHalfTable = True
print("Cuckoo Hashing: ")
test_insert4()
print()
# print(hashTable)
clearTable()
