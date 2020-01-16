import threading
import time

class MyThread (threading.Thread):
    die = False
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run (self):
        while not self.die:
            time.sleep(1)
            print (self.name)

    def join(self,timeout=None):
        self.die = True
        super(threading.Thread,self).join(timeout)

if __name__ == '__main__':
    f = MyThread('first')
    f.start()
    s = MyThread('second')
    s.start()
    try:
        f.join()
        s.join()
    except KeyboardInterrupt:
       quit()