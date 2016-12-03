import Experiment

# Above 8 appears to make no difference in the load factor achieved
maxLoop = 8


def cuckoo_insert(value):
    # Iterate through all four hash functions until able to insert or return false if not able
    j = 0
    while j < maxLoop:
        for i in range(len(Experiment.twoHashFunctions)):
            if Experiment.useHalfTable:
                indexOffset = Experiment.twoHashFunctions[i](value)
                index = indexOffset + i * Experiment.halfTable
            else:
                index = Experiment.twoHashFunctions[i](value)
            if Experiment.hashTable[index] is None:
                Experiment.hashTable[index] = value
                return True
            # This else statement actually fails to insert at a lower load factor
            else:
                # There is an element in the index so swap them. This is the Cuckoo step and previous value will try to be hashed
                Experiment.hashTable[index], value = value, Experiment.hashTable[index]
        j += 1
    # print("Unable to insert")
    return False


# Return the index of a value if it is in the table
def lookup(value):
    # Iterate through all four hash functions searching for the value
    for i in range(len(Experiment.twoHashFunctions)):
        if Experiment.useHalfTable:
            indexOffset = Experiment.twoHashFunctions[i](value)
            index = indexOffset + i * Experiment.halfTable
        else:
            index = Experiment.twoHashFunctions[i](value)
        if Experiment.hashTable[index] is value:
            return index
    print("Value not in table")
    return None


def delete(value):
    # Call lookup to find index, if it exists
    index = lookup(value)
    if index is not None:
        Experiment.hashTable[index] = None
