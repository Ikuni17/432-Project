import perfection
import random
import datetime
import timeit
import sys

p = perfection
tableSize = 1049
hashTable = [None] * tableSize
values_to_insert = random.sample(range(tableSize*10), tableSize)

def initialize():

    # tableSize = 104729
    #table_size = 100003
    table_size = 1049

    values_to_insert = random.sample(range(table_size*10), table_size)
    values_to_insert.sort()
    print("Insert: {} values with table size {}".format(len(values_to_insert), table_size))
    params = p.hash_parameters(values_to_insert)
    function = p.make_hash(values_to_insert)

    list_r = []
    for item in params.r:
        if item is not None:
            list_r.append(item)



    second_test = [None] * table_size
    resultsss = []
    for i in values_to_insert:
        val = i + params.offset
        x = val % params.t
        y = val // params.t
        result = x + list_r[y]
        print("{}:{}".format(i, result))
        resultsss.append(result)

    resultsss.sort()
    for r in resultsss:
        print(r)

    hashtable = p.make_hash(values_to_insert)
    dicttable = p.make_dict('dicttable', values_to_insert)
    test = []
    for e in params.r:
        if e is not None:
            test.append(e)

    test.sort()
    print("sorted r: {}".format(test))
    function = u"r:{}\nOriginal inputs:{}\nt:{}\noffset:{}\nto_int:{}".format(params.r, len(params.slots), params.t,
                                                                                   params.offset, params.to_int)


    print(function)
    print("Int(key):Value")
    #for e in values_to_insert:
        #print("%d:%d" % (e, hashtable(e)))
    print("Load facor: %f" % (table_size/params.t))




#initialize()
# print(timeit.timeit(initialize, number=1))

def hashFun1(key):
    return key % tableSize

def chainedInsert(value):
    index = hashFun1(value)
    if hashTable[index] is None:
        hashTable[index] = [value]
        # print("Inserted {} on index {}".format(value, index))
    else:
        hashTable[index].append(value)
        # print("Appended {} on index {}".format(value, index))

def chainedDelete(value):
    index = chainedLookup(value)
    if hashTable[index] is not None:
        for item in hashTable[index]:
            if item is value:
                hashTable[index].remove(value)
    else:
        return None

def chainedLookup(value):
    index = hashFun1(value)
    if hashTable[index] is not None:
        for item in hashTable[index]:
            if item is value:
                return index
    else:
        return None

def clearTable():
    global hashTable
    hashTable = [None] * tableSize

def chainedTest():
    clearTable()
    for n in values_to_insert:
        chainedInsert(n)

    for n in range(len(hashTable)):
        a = 1
        print("{}:{}".format(n, hashTable[n]))

    for i in range(100):
        check = chainedLookup(i)
        if check is not None:
            print("Found {} at index {}, with value(s) {}".format(i, check, hashTable[i]))
            chainedDelete(i)
            print("Removed {}. New value(s) {}".format(i, hashTable[i]))
        else:
            print("Did not find {}".format(i))

chainedTest()
