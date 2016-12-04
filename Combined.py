import os
import random
import sys
import math
from timeit import default_timer as timer
import perfection

# Number of times to run the experiment
experimentRuns = 5
# Using a prime number for tableSize helps the hash functions
# tableSize = 17
tableSize = 1049
# tableSize = 100003
# Maximum amount of attempts to "cuckoo" elements
maxLoop = 8
# Divide the table for two hash functions mapping to distinct sections
halfTable = int(tableSize / 2)
useHalfTable = False
# Divide the table for four hash functions mapping to distinct sections
quarterTable = int(tableSize / 4)
useQuarterTable = False
# A list filled with None to represent an empty array
hashTable = [None] * tableSize
# A list of values to insert, enough to reach a load factor of exactly 1.0 theoretically
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


# Lists of Python functions to iterate through
twoHashFunctions = [hashFun1, hashFun2]
fourHashFunctions = [hashFun1, hashFun2, hashFun3, hashFun4]


# Reset hashTable to "empty"
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


# Tests the load factor achieved by Bin Hashing
def binTester():
    inserted = 0
    notInserted = 0
    # Iterate through all integers in the list
    for values in range(len(valuesToInsert)):
        # Try to insert the current integer
        check = binInsert(valuesToInsert[values])
        # Succeed to insert
        if check is True:
            inserted += 1
        # Failed to insert
        else:
            notInserted += 1
    # Print results after the loop terminates
    print("Inserted: ", inserted)
    print("Not Inserted: ", notInserted)
    print("Load Factor: ", (inserted / tableSize))


# Tests the load factor achieved by Cuckoo Hashing
def cuckooTester():
    inserted = 0
    notInserted = 0
    # Iterate through all integers in the list
    for values in range(len(valuesToInsert)):
        # Try to insert the current integer
        check = cuckooInsert(valuesToInsert[values])
        # Succeed to insert
        if check is True:
            inserted += 1
        # Failed to insert
        else:
            notInserted += 1
    # Print results after the loop terminates
    print("Inserted: ", inserted)
    print("Not Inserted: ", notInserted)
    print("Load Factor: ", (inserted / tableSize))


# This will use four hash functions instead of two and theoretically should reach load factor of 0.97 before
# failing to insert. Could potentially reach 0.99 if we map the four functions to a bin of two cells each.
def binInsert(value):
    j = 0
    while j < maxLoop:
        # Iterate through all four hash functions until able to insert without a collision or maxLoop is reached
        for i in range(len(fourHashFunctions)):
            # Hash the value to get the index offset. The index offset is between 0 and quarterTable
            indexOffset = fourHashFunctions[i](value)
            # Since each hash function corresponds to a unique section of the hash table, 'i' will correspond to
            # the section. For example, presume our indexOffset was 3 and our tableSize is 100. Each hash function
            # corresponds to 25 indices, so if we were using hash function 2: i = 2. The correct index would then be
            # index = 3 + (2 * 25) = 53
            index = indexOffset + (i * quarterTable)
            # If the index is empty insert the element and break the loops by returning
            if hashTable[index] is None:
                hashTable[index] = value
                return True
            # Otherwise a collision occured, swap the element currently in the table with the one we're trying to insert
            # When we return to the top of the loop, the element we removed will be hashed with the next function and
            # attempted to be inserted
            else:
                hashTable[index], value = value, hashTable[index]
        j += 1
    # If we reach this point a cycle has occurred and the element failed to insert
    return False


# Return the index of a value if it is in the table
def binLookup(value):
    # Iterate through all four hash functions searching for the value
    for i in range(len(fourHashFunctions)):
        # Refer to binInsert comments to understand this logic
        indexOffset = fourHashFunctions[i](value)
        index = indexOffset + (i * quarterTable)
        if hashTable[index] is value:
            # print("Found: ", value, " at index: ", index, " which is: ", hashTable[index])
            return index
    # print("Value not in table")
    return None


# Remove an element from the hash table
def binDelete(value):
    # Call lookup to find index, if it exists
    index = binLookup(value)
    # If index is any number, the lookup was successful so set the value to None to delete it and return success
    if index is not None:
        hashTable[index] = None
        return True
    # Otherwise the value is not in the table so return failed
    else:
        return False


def cuckooInsert(value):
    j = 0
    while j < maxLoop:
        # Iterate through two hash functions until able to insert or return false if not able
        for i in range(len(twoHashFunctions)):
            # Refer to binInsert comments to understand this logic
            indexOffset = twoHashFunctions[i](value)
            index = indexOffset + (i * halfTable)
            if hashTable[index] is None:
                hashTable[index] = value
                return True
            else:
                hashTable[index], value = value, hashTable[index]
        j += 1
    return False


# Return the index of a value if it is in the table
def cuckooLookup(value):
    for i in range(len(twoHashFunctions)):
        indexOffset = twoHashFunctions[i](value)
        index = indexOffset + (i * halfTable)
        if hashTable[index] is value:
            return index
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
        print("\nStarting iteration: ", i + 1)
        print("Clearing hash table and generating a new input set\n")
        clearTable()

        # Generate the input set and save it to an external text file
        valuesToInsert = random.sample(range(tableSize * 10), tableSize)
        sInputSet = "Results\\inputSet" + str(i + 1) + ".txt"
        inputSetFile = open(sInputSet, "w")
        for j in range(len(valuesToInsert)):
            inputSetFile.write(str(valuesToInsert[j]) + "\n")
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
            insertCheck = binInsert(valuesToInsert[values])
            end = timer()
            insertTime = end - start
            insertFile.write(str(loadFactor) + " " + str(insertTime) + "\n")
            if insertCheck is True:
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
        print("Load factor achieved: ", loadFactor)

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
            insertCheck = cuckooInsert(valuesToInsert[values])
            end = timer()
            insertTime = end - start
            insertFile.write(str(loadFactor) + " " + str(insertTime) + "\n")
            if insertCheck is True:
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
        print("Load factor achieved: ", loadFactor)

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
    # perfectTester()
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


#main()
runExperiment()
