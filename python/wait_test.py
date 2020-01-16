from __future__ import print_function
from random import random
import threading
import time
import sys

progress = 0
result = None
result_available = threading.Event()

def background_calculation():
    try:
        # here goes some long calculation
        global progress
        for i in range(100):
            time.sleep(random() * 3)
            progress = i + 1

        # when the calculation is done, the result is stored in a global variable
        global result
        result = 42
        result_available.set()

        # do some more work before exiting the thread
        time.sleep(10)
    except KeyboardInterrupt:
        result_available.set()
        pass

def main():
    thread = threading.Thread(target=background_calculation)
    thread.start()

    try:
        # wait here for the result to be available before continuing
        while not result_available.wait(timeout=5):
            print('\r{}% done...'.format(progress), end='') #, flush=True)
            sys.stdout.flush() #py2
        print('\r{}% done...'.format(progress))

        print('The result is', result)
    except KeyboardInterrupt:
        result_available.set()
        pass

if __name__ == '__main__':
    main()