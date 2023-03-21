from concurrent.futures import ThreadPoolExecutor
from common.logger import Logger
from time import sleep
import random

logger = Logger("Test")

def print_variable(a='', b='', c=''):
    # sleep(int(1))
    print( "Test [A] : " + str(a) + " [B] : " + str(b) + " [C] : " + str(c))

poc = 10

pool_executor = ThreadPoolExecutor(10)


for i in range(10):
    test = int(random.random() * 10 + 1)
    pool = pool_executor.map(print_variable, 'A', str(test),  str(test))

    # if pool.done():
    #     logger.info(pool.result())
    # else:
    #     logger.info("Not Yet " + str(i) + " " + str(test))

