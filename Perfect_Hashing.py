import perfection
import random
import datetime
import timeit
import sys

p = perfection

def initialize():

    # tableSize = 104729
    #table_size = 100003
    table_size = 1049
    day = datetime.date
    time = datetime.time
    print("the time")
    print(sys.maxsize)
    values_to_insert = random.sample(range(table_size*10), table_size)
    values_to_insert.sort()
    print("Insert: {} with table size {}".format(values_to_insert, table_size))
    params = p.hash_parameters(values_to_insert)
    slots = params.slots

    hashtable = p.make_hash(values_to_insert)
    dicttable = p.make_dict('dicttable', values_to_insert)
    function = u"r:{}\nOriginal inputs:{}\nt:{}\noffset:{}\nto_int:{}".format(params.r, params.slots, params.t,
                                                                                   params.offset, params.to_int)


    print(function)
    print("Int(key):Value")
    for e in values_to_insert:
        print("%d:%d" % (e, hashtable(e)))
    print("Load facor: %f" % (table_size/params.t))


initialize()
# print(timeit.timeit(initialize, number=1))
