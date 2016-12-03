# This file will handle driving the experiment, outputting the results and utility functions.

import random
import sys
import math

# Using a prime number for tableSize helps the hash functions
tableSize = 1049
# tableSize = 100003
# Maximum amount of attempts to "cuckoo" elements
maxLoop = 1000
# Divide the table for two hash function mapping to distinct sections
halfTable = int(tableSize / 2)
useHalfTable = False
# Divide the table for four hash function mapping to distinct sections
quarterTable = int(tableSize / 4)
useQuarterTable = False
# A list filled with None to represent an array
hashTable = [None] * tableSize
# A list of values to insert, enough to reach a load factor of 1.0 theoretically
valuesToInsert = random.sample(range(sys.maxsize), tableSize)


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


def perfectTester():
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


def binTester():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        check = binInsert(valuesToInsert[values])
        #print(binLookup(valuesToInsert[values]))
        if check is True:
            count += 1
        else:
            count2 += 1
        #binDelete(valuesToInsert[values])
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))


def cuckooTester():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        check = cuckooInsert(valuesToInsert[values])
        #print(cuckooLookup(valuesToInsert[values]))
        if check is True:
            count += 1
        else:
            count2 += 1
        #cuckooDelete(valuesToInsert[values])
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))


# This will use four hash functions instead of two and theoretically should reach load factor of 0.97 before
# failing to insert. Could potentially reach 0.99 if we map the four functions to a bin of two cells each.

def binInsert(value):
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


# Return the index of a value if it is in the table
def binLookup(value):
    # Iterate through all four hash functions searching for the value
    for i in range(len(fourHashFunctions)):
        if useQuarterTable:
            indexOffset = fourHashFunctions[i](value)
            index = indexOffset + i * quarterTable
        else:
            index = fourHashFunctions[i](value)
        if hashTable[index] is value:
            return index
    print("Value not in table")
    return None


def binDelete(value):
    # Call lookup to find index, if it exists
    index = binLookup(value)
    if index is not None:
        hashTable[index] = None


def cuckooInsert(value):
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
                hashTable[index], value = value, hashTable[index]
        j += 1
    # print("Unable to insert")
    return False


# Return the index of a value if it is in the table
def cuckooLookup(value):
    # Iterate through all four hash functions searching for the value
    for i in range(len(twoHashFunctions)):
        if useHalfTable:
            indexOffset = twoHashFunctions[i](value)
            index = indexOffset + i * halfTable
        else:
            index = twoHashFunctions[i](value)
        if hashTable[index] is value:
            return index
    print("Value not in table")
    return None


def cuckooDelete(value):
    # Call lookup to find index, if it exists
    index = cuckooLookup(value)
    if index is not None:
        hashTable[index] = None

def main():
    print("Table Size: ", tableSize)
    #print("Perfect Hash Function:")
    #perfectTester()
    #print(hashTable)
    #print()
    #clearTable()
    useQuarterTable = True
    useHalfTable = False
    print("Bin Hashing: ")
    binTester()
    #print(hashTable)
    print()
    clearTable()
    useQuarterTable = False
    useHalfTable = True
    print("Cuckoo Hashing: ")
    cuckooTester()
    #print(hashTable)
    print()

main()
