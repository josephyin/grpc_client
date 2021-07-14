import time
from threading import Thread


def bench(func, count=1):
    threads = []
    for i in range(count):
        threads.append(Thread(target=func, args=(i,)))

    start = time.time()
    print('!! Started at %s, running %s times' % (start, count))

    # start
    for i in range(count):
        threads[i].start()

    # wait until finish
    for i in range(count):
        threads[i].join()

    end = time.time()
    print('!! Ended at %s' % end)

    print('!! Duration is %ss' % (end - start))
