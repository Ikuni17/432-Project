import perfection
#import Experiment
import random
import timeit


def testFun():
    tableSize = 104729
    valuesToInsert = random.sample(range(500000), tableSize)
    function = perfection.make_hash(valuesToInsert)
    print(function)

print(timeit.timeit(testFun, number=1))