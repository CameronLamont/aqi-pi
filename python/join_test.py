from random import random
import threading
import time

result = None

def background_calculation():
    # here goes some long calculation
    time.sleep(random() * 5 * 60)

    # when the calculation is done, the result is stored in a global variable
    global result
    result = 42

def main():
    try:
        thread = threading.Thread(target=background_calculation)
        thread.start()

    
        # while True:
        #     time.sleep(2)
    except KeyboardInterrupt:
        # wait here for the result to be available before continuing
        thread.join()
    finally:
        print('The result is', result)

if __name__ == '__main__':
    main()