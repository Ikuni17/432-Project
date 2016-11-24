import perfection
#import Experiment
import random
import timeit


def testFun():
    tableSize = 1000003
    valuesToInsert = random.sample(range(10000000), tableSize)
    function = perfection.make_hash(valuesToInsert)
    print(function)

print(timeit.timeit(testFun, number=1))