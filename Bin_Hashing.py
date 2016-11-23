# This will use four hash functions instead of two and theoretically should reach load factor of 0.97 before
# failing to insert. Could potentially reach 0.99 if we map the four functions to a bin of two cells each.

import Experiment

def insert(value):
    # Iterate through all four hash functions until able to insert or return false if not able
    for i in range(len(Experiment.hashFunctions)):
        index = Experiment.hashFunctions[i](value)
        if Experiment.hashTable[index] is None:
            Experiment.hashTable[index] = value
            return True
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