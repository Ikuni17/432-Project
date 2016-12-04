# This file will handle driving the experiment, outputting the results and utility functions.
import os
import random
import sys
import math
from timeit import default_timer as timer
import perfection

# Number of times to run the experiment
experimentRuns = 5
# Using a prime number for tableSize helps the hash functions
#tableSize = 17
tableSize = 1049
#tableSize = 100003
# Maximum amount of attempts to "cuckoo" elements
maxLoop = 8
# Divide the table for two hash function mapping to distinct sections
halfTable = int(tableSize / 2)
useHalfTable = False
# Divide the table for four hash function mapping to distinct sections
quarterTable = int(tableSize / 4)
useQuarterTable = False
# A list filled with None to represent an array
hashTable = [None] * tableSize
# A list of values to insert, enough to reach a load factor of 1.0 theoretically
valuesToInsert = random.sample(range(tableSize * 10), tableSize)


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
    # Tests insertion using a perfect hash.
    perfect_hash_table = perfection.make_hash(valuesToInsert)
    params = perfection.hash_parameters(valuesToInsert)
    print("Inserted: ", len(valuesToInsert))
    print("Not Inserted: 0")
    print("Load Factor: ", (len(valuesToInsert) / params.t))
    function = u"\nperfect_hash(i):\n    static r = {}\n    static t = {}\n\n    x = i mod t //({})\n    y = i div t //({})\n    return x + r[y]\n".format(
        params.r, params.t, params.t,
        params.t)
    # print("Perfect Hash Function: ", function)

    # print(hashTable)
    print()


def binTester():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        check = binInsert(valuesToInsert[values])
        # print(binLookup(valuesToInsert[values]))
        if check is True:
            count += 1
        else:
            count2 += 1
            # binDelete(valuesToInsert[values])
    print("Inserted: ", count)
    print("Not Inserted: ", count2)
    print("Load Factor: ", (count / tableSize))


def cuckooTester():
    count = 0
    count2 = 0
    for values in range(len(valuesToInsert)):
        check = cuckooInsert(valuesToInsert[values])
        # print(cuckooLookup(valuesToInsert[values]))
        if check is True:
            count += 1
        else:
            count2 += 1
            # cuckooDelete(valuesToInsert[values])
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
            # if useQuarterTable:
            indexOffset = fourHashFunctions[i](value)
            index = indexOffset + (i * quarterTable)
            # else:
            #    index = fourHashFunctions[i](value)
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
        # if useQuarterTable:
        indexOffset = fourHashFunctions[i](value)
        index = indexOffset + (i * quarterTable)
        # else:
        #    index = fourHashFunctions[i](value)
        if hashTable[index] is value:
            # print("Found: ", value, " at index: ", index, " which is: ", hashTable[index])
            return index
    # print("Value not in table")
    return None


def binDelete(value):
    # Call lookup to find index, if it exists
    index = binLookup(value)
    if index is not None:
        hashTable[index] = None
        return True
    else:
        return False


def cuckooInsert(value):
    # Iterate through all four hash functions until able to insert or return false if not able
    j = 0
    while j < maxLoop:
        for i in range(len(twoHashFunctions)):
            # if useHalfTable:
            indexOffset = twoHashFunctions[i](value)
            index = indexOffset + (i * halfTable)
            # else:
            #    index = twoHashFunctions[i](value)
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
        # if useHalfTable:
        indexOffset = twoHashFunctions[i](value)
        index = indexOffset + (i * halfTable)
        # else:
        #    index = twoHashFunctions[i](value)
        if hashTable[index] is value:
            return index
    # print("Value not in table")
    return None


def cuckooDelete(value):
    # Call lookup to find index, if it exists
    index = cuckooLookup(value)
    if index is not None:
        hashTable[index] = None
        return True
    else:
        return False


def runExperiment():
    global useHalfTable
    global useQuarterTable
    global valuesToInsert
    global hashTable

    # Create a results folder if needed
    resultsDir = (".\Results")
    if not os.path.isdir(resultsDir):
        os.makedirs(resultsDir)
        print("Results folder created")

    # File Names
    sPerfectHashInsert = "Results\\perfectHashInsert.txt"
    sPerfectHashLookup = "Results\\perfectHashLookup.txt"
    sPerfectHashDelete = "Results\\perfectHashDelete.txt"
    sBinHashInsert = "Results\\binHashInsert.txt"
    sBinHashLookupSuc = "Results\\binHashLookupSuccess.txt"
    sBinHashLookupFail = "Results\\binHashLookupFail.txt"
    sBinHashDelete = "Results\\binHashDelete.txt"
    sCuckooHashInsert = "Results\\cuckooHashInsert.txt"
    sCuckooHashLookupSuc = "Results\\cuckooHashLookupSuccess.txt"
    sCuckooHashLookupFail = "Results\\cuckooHashLookupFail.txt"
    sCuckooHashDelete = "Results\\cuckooHashDelete.txt"

    print("Starting experiment with table size: ", tableSize, "\n")

    for i in range(experimentRuns):
        print("\nStarting iteration: ", i+1)
        print("Clearing hash table and generating a new input set\n")
        clearTable()
        valuesToInsert = random.sample(range(tableSize * 10), tableSize)
        sInputSet = "Results\\inputSet" + str(i+1) +".txt"
        inputSetFile = open(sInputSet, "w")
        for j in range(len(valuesToInsert)):
            inputSetFile.write(str(valuesToInsert[j])+ "\n")
        inputSetFile.close()

        print("Performing Bin Hashing insert and lookup")
        insertSuccess = 0
        useHalfTable = False
        useQuarterTable = True
        insertFile = open(sBinHashInsert, "a")
        lookupSucFile = open(sBinHashLookupSuc, "a")
        lookupFailFile = open(sBinHashLookupFail, "a")
        for values in range(len(valuesToInsert)):
            loadFactor = insertSuccess / tableSize

            start = timer()
            deleteCheck = binInsert(valuesToInsert[values])
            end = timer()
            deleteTime = end - start
            insertFile.write(str(loadFactor) + " " + str(deleteTime) + "\n")
            if deleteCheck is True:
                insertSuccess += 1

            start = timer()
            lookupCheck = binLookup(valuesToInsert[values])
            end = timer()
            lookupTime = end - start
            if lookupCheck is None:
                lookupFailFile.write(str(loadFactor) + " " + str(lookupTime) + "\n")
            else:
                lookupSucFile.write(str(loadFactor) + " " + str(lookupTime) + "\n")

        insertFile.close()
        lookupSucFile.close()
        lookupFailFile.close()

        print("Performing Bin Hashing delete")
        deleteFile = open(sBinHashDelete, "a")
        for values in range(len(valuesToInsert)):
            loadFactor = insertSuccess / tableSize

            start = timer()
            deleteCheck = binDelete(valuesToInsert[values])
            end = timer()
            deleteTime = end - start
            deleteFile.write(str(loadFactor) + " " + str(deleteTime) + "\n")
            if deleteCheck is True:
                insertSuccess -= 1

        deleteFile.close()
        print("Clearing hash table\n")
        clearTable()

        print("Performing Cuckoo Hashing insert and lookup")
        insertSuccess = 0
        useHalfTable = True
        useQuarterTable = False
        insertFile = open(sCuckooHashInsert, "a")
        lookupSucFile = open(sCuckooHashLookupSuc, "a")
        lookupFailFile = open(sCuckooHashLookupFail, "a")
        for values in range(len(valuesToInsert)):
            loadFactor = insertSuccess / tableSize

            start = timer()
            deleteCheck = cuckooInsert(valuesToInsert[values])
            end = timer()
            deleteTime = end - start
            insertFile.write(str(loadFactor) + " " + str(deleteTime) + "\n")
            if deleteCheck is True:
                insertSuccess += 1

            start = timer()
            lookupCheck = cuckooLookup(valuesToInsert[values])
            end = timer()
            lookupTime = end - start
            if lookupCheck is None:
                lookupFailFile.write(str(loadFactor) + " " + str(lookupTime) + "\n")
            else:
                lookupSucFile.write(str(loadFactor) + " " + str(lookupTime) + "\n")

        insertFile.close()
        lookupSucFile.close()
        lookupFailFile.close()

        print("Performing Cuckoo Hashing delete")
        deleteFile = open(sCuckooHashDelete, "a")
        for values in range(len(valuesToInsert)):
            loadFactor = insertSuccess / tableSize

            start = timer()
            deleteCheck = cuckooDelete(valuesToInsert[values])
            end = timer()
            deleteTime = end - start
            deleteFile.write(str(loadFactor) + " " + str(deleteTime) + "\n")
            if deleteCheck is True:
                insertSuccess -= 1

        deleteFile.close()


def main():
    global useQuarterTable
    global useHalfTable

    print("Table Size: ", tableSize, "\n")
    print("Perfect Hashing:")
    #perfectTester()
    # print(hashTable)
    # print()
    # clearTable()
    useQuarterTable = True
    useHalfTable = False
    print("Bin Hashing: ")
    binTester()
    # print(hashTable)
    print()
    clearTable()
    useQuarterTable = False
    useHalfTable = True
    print("Cuckoo Hashing: ")
    cuckooTester()
    # print(hashTable)
    print()


main()
#runExperiment()
