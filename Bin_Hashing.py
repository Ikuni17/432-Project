# This will use four hash functions instead of two and theoretically should reach load factor of 0.97 before
# failing to insert. Could potentially reach 0.99 if we map the four functions to a bin of two cells each.

import Experiment

maxLoop = 1

def insert(value):
    # Iterate through all four hash functions until able to insert or return false if not able
    j = 0
    while j < maxLoop:
        for i in range(len(Experiment.hashFunctions)):
            #indexOffset = Experiment.hashFunctions[i](value)
            #realIndex = indexOffset + i * Experiment.quarterTable
            realIndex = Experiment.hashFunctions[i](value)
            if Experiment.hashTable[realIndex] is None:
                Experiment.hashTable[realIndex] = value
                return True
            # This else statement actually fails to insert at a lower load factor
            else:
                # There is an element in the index so swap them. This is the Cuckoo step and previous value will try to be hashed
                Experiment.hashTable[realIndex], value = value, Experiment.hashTable[realIndex]
        j+=1
    #print("Unable to insert")
    return False

# Return the index of a value if it is in the table
def lookup(value):
    # Iterate through all four hash functions searching for the value
    for i in range(len(Experiment.hashFunctions)):
        index = Experiment.hashFunctions[i](value)
        if Experiment.hashTable[index] is value:
            return index
    print("Value not in table")
    return None

def delete(value):
    # Call lookup to find index, if it exists
    index = lookup(value)
    if index is not None:
        Experiment.hashTable[index] = None